from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select,and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from database import get_database
from models import User, Book, Sale, Bill
from auth import get_current_user

router = APIRouter(prefix="/sale", tags=["销售管理"])

# 购买书籍接口
@router.post("/book")
async def book_sale(
    isbn: str = Query(max_length=20, description="书籍编号"),
    quantity: int = Query(ge=1,description="购买数量"),
    current_user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_database)
):
    # 判断登录状态
    operator = await db.get(User, current_user_id)
    if not operator:
        raise HTTPException(status_code=401, detail="用户不存在或未登录")

    if isbn is None:
        raise HTTPException(status_code=400, detail="isbn不能为空")

    # 获取图书
    result = await db.execute(select(Book).where(Book.isbn == isbn))
    book = result.scalars().first()
    if book is None:
        raise HTTPException(status_code=404,detail="书籍不存在")

    if book.price is None:
        raise HTTPException(status_code=400,detail="该书尚未定价，无法购买")

    if quantity > book.stock_quantity:
        raise HTTPException(status_code=400,detail=f"库存不足，当前库存仅 {book.stock_quantity} 本")

    # 更改库存数
    book.stock_quantity -= quantity

    # 加入Sale表
    sale_data={
        "book_id":book.book_id,
        "sale_price":book.price,
        "sale_quantity":quantity,
        "user_id":current_user_id
    }
    new_sale = Sale(**sale_data)
    db.add(new_sale)
    await db.flush()

    # 加入Bill表
    bill_data={
        "bill_type":"income",
        "amount":book.price * quantity,
        "related_id":new_sale.sale_id
    }
    new_bill = Bill(**bill_data)
    db.add(new_bill)

    # 提交数据
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500,detail=f"数据库写入异常：{str(e)}")

    return {
        "message":"购买成功",
        "isbn":isbn,
        "title":book.title,
        "quantity":quantity,
        "amount":book.price * quantity,
    }

# 销售退货接口
@router.put("/return")
async def book_return(
        sale_id: int = Query(ge=1,description="销售记录号"),
        current_user_id: int = Depends(get_current_user),
        db: AsyncSession = Depends(get_database)
):
    # 判断登录状态
    operator = await db.get(User,current_user_id)
    if not operator:
        raise HTTPException(status_code=401, detail="用户不存在或未登录")

    # 查询订单
    results = await db.execute(select(Sale).where(Sale.sale_id == sale_id))
    sales =  results.scalars().first()

    if sales is None:
        raise HTTPException(status_code=404,detail="销售记录不存在")
    if sales.sale_status != "completed":
        raise HTTPException(status_code=400,detail="该订单无法退货")

    book = await db.get(Book,sales.book_id)
    if book is None:
        raise HTTPException(status_code=404,detail="书籍不存在")

    # 增加库存和修改状态
    book.stock_quantity += sales.sale_quantity
    sales.sale_status = "returned"
    bill_data={
        "bill_type":"refund",
        "amount":book.price * sales.sale_quantity,
        "related_id":sales.sale_id
    }
    new_bill = Bill(**bill_data)
    db.add(new_bill)

    # 提交数据
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500,detail=f"数据库写入异常：{str(e)}")

    return {
        "message":"退货成功"
    }

# 查询售卖号
@router.get("/search")
async def sale_search(
        sale_id: int = Query(ge=1,description="销售记录号"),
        current_user_id: int = Depends(get_current_user),
        db: AsyncSession = Depends(get_database)
):
    # 判断登录状态
    operator = await db.get(User,current_user_id)
    if not operator:
        raise HTTPException(status_code=401, detail="用户不存在或未登录")

    # 查询订单
    results = await db.execute(select(Sale).where(Sale.sale_id == sale_id))
    sales =  results.scalars().first()

    if sales is None:
        raise HTTPException(status_code=404,detail="销售记录不存在")

    book_result = await db.execute(select(Book).where(Book.book_id == sales.book_id))
    books= book_result.scalars().first()
    # 一般来说因为book_id是外键，不可能发送，但以防万一加上判断
    if books is None:
        raise HTTPException(status_code=404,detail="书籍不存在")

    return {
        "sale_id":sales.sale_id,
        "book_id":books.book_id,
        "title":books.title,
        "sale_price":sales.sale_price,
        "sale_quantity":sales.sale_quantity,
        "sold_at":sales.sold_at,
        "sale_status": sales.sale_status
    }

# 查询指定时间内的售卖单（超级管理员查看所有的，普通管理员只查看自己的）
@router.get("/search/time")
async def sale_time_search(
        first_time:datetime = Query(description="开始时间"),
        last_time:datetime = Query(description="结束时间"),
        current_user_id: int = Depends(get_current_user),
        db: AsyncSession = Depends(get_database)
):
    # 判断登录状态
    operator = await db.get(User,current_user_id)
    if not operator:
        raise HTTPException(status_code=401, detail="用户不存在或未登录")
    
    # 检查指定时间范围内的订单
    if operator.user_role == "super_admin":
        results = await db.execute(select(Sale,Book.isbn,Book.title)
                                   .join(Book,Sale.book_id == Book.book_id)
                                   .where(Sale.sold_at.between(first_time,last_time)))
    else:
        results = await db.execute(select(Sale,Book.isbn,Book.title)
                                   .join(Book,Sale.book_id == Book.book_id)
                                   .where(and_(Sale.sold_at.between(first_time,last_time),
                                          Sale.user_id == operator.user_id)))

    sales = results.all()
    if sales is None:
        raise HTTPException(status_code=404,detail=f"{first_time}到{last_time}不存在订单")
    
    return [
    {
        "sale_id": sale.Sale.sale_id,
        "isbn": sale.isbn,
        "title": sale.title,
        "sale_price": sale.Sale.sale_price,
        "sale_quantity": sale.Sale.sale_quantity,
        "sold_at": sale.Sale.sold_at,
        "user_id": sale.Sale.user_id,
        "sale_status": sale.Sale.sale_status
    }
    for sale in sales
]

# 查询所有售卖单（只超级管理员可用）
@router.get("/search/all")
async def sale_all_search(
        current_user_id: int = Depends(get_current_user),
        db: AsyncSession = Depends(get_database)
):
    # 判断登录状态
    operator = await db.get(User,current_user_id)
    if not operator:
        raise HTTPException(status_code=401, detail="用户不存在或未登录")
    
    # 超级管理员权限判断
    if operator.user_role != "super_admin":
        raise HTTPException(status_code=403,detail="不是超级管理员，无法查看")
    
    results = await db.execute(select(Sale,Book.isbn,Book.title).join(Book,Sale.book_id == Book.book_id))
    sales = results.all()
    if sales is None:
        raise HTTPException(status_code=404,detail="没有售卖单子")
    
    return [
    {
        "sale_id": sale.Sale.sale_id,
        "isbn": sale.isbn,
        "title": sale.title,
        "sale_price": sale.Sale.sale_price,
        "sale_quantity": sale.Sale.sale_quantity,
        "sold_at": sale.Sale.sold_at,
        "user_id": sale.Sale.user_id,
        "sale_status": sale.Sale.sale_status
    }
    for sale in sales
]
