from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_database
from models import User, Book, Purchase
from schemas import BookUpdate
from auth import get_current_user

router = APIRouter(prefix="/book", tags=["图书管理"])

# 查询书籍接口
@router.get("/search")
async def search_books(
    book_id:int = Query(None, description="书籍编号"),
    isbn:str = Query(None, max_length=20, description="ISBN号"),
    title:str = Query(None, max_length=70, description="书名"),
    author:str = Query(None, max_length=50, description="作者"),
    publisher:str = Query(None, max_length=50, description="出版社"),
    current_user_id:int = Depends(get_current_user),
    db: AsyncSession = Depends(get_database)
):
    # 判断登录状态
    operator = await db.get(User,current_user_id)
    if not operator:
        raise HTTPException(status_code=401, detail="用户不存在或未登录")

    # 条件处理
    conditions = []
    if book_id is not None:
        conditions.append(Book.book_id == book_id)
    if isbn is not None:
        conditions.append(Book.isbn == isbn)
    if title is not None:
        conditions.append(Book.title.like(f"%{title}%"))
    if author is not None:
        conditions.append(Book.author.like(f"%{author}%"))
    if publisher is not None:
        conditions.append(Book.publisher.like(f"%{publisher}%"))

    if not conditions:
        raise  HTTPException(status_code=400,detail="至少输入一种查询值")

    # 查询
    result = await db.execute(select(Book).where(and_(*conditions)))
    books = result.scalars().all()

    if not books:
        raise HTTPException(status_code=404,detail="没有找到书籍")

    return books

# 图书修改接口
@router.put("/update")
async def update_books(
    book_update:BookUpdate,
    current_user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_database)
):
    # 判断登录状态
    operator = await db.get(User,current_user_id)
    if not operator:
        raise HTTPException(status_code=401, detail="用户不存在或未登录")

    # 判断查询条件
    if book_update.book_id is None:
        raise HTTPException(status_code=400,detail="需要输入book_id进行修改")

    result = await db.get(Book,book_update.book_id)
    if not result:
        raise HTTPException(status_code=404,detail="没有找到书籍")

    if book_update.author is not None:
        result.author = book_update.author
    if book_update.title is not None:
        result.title = book_update.title
    if book_update.publisher is not None:
        result.publisher = book_update.publisher
    if book_update.price is not None:
        if book_update.price < 0:
            raise HTTPException(status_code=400,detail="价格不能为负数")
        result.price = book_update.price

    # 提交数据
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500,detail=f"数据库写入异常：{str(e)}")
    return {
        "message":"书籍更新成功"
    }

# 添加书籍接口
@router.put("/add")
async def add_book(
    order_id: int = Query(ge=0, description="订单号"),
    price:Decimal =Query(ge=0,description="零售价"),
    current_user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_database)
):
    # 判断登录状态
    operator = await db.get(User,current_user_id)
    if not operator:
        raise HTTPException(status_code=401, detail="用户不存在或未登录")

    # 获取订单
    result = await db.get(Purchase,order_id)
    if result is None:
        raise HTTPException(status_code=404,detail="订单号不存在")

    # 判断图书是否已付款
    if result.book_status != "paid":
        raise HTTPException(status_code=400,detail="图书未付款，不可加入")

    # 判断是否已经入过库了
    if result.is_stocked == "True":
        raise HTTPException(status_code=400,detail="该订单已入库")

    # 获取书籍
    book = await db.get(Book,result.book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="书籍不存在")

    # 增加库存，更新零售价，更新订单状态
    result.is_stocked = "True"
    stock_quantity = book.stock_quantity+result.purchase_quantity
    book.stock_quantity = stock_quantity
    if price < result.buy_price:
        raise HTTPException(status_code=400,detail="零售价要大于进货价")
    book.price = price

    # 提交数据
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500,detail=f"数据库写入异常：{str(e)}")

    return {
        "message":"添加成功",
        "isbn":book.isbn,
        "title":book.title,
        "stock_quantity":stock_quantity,
        "price":price
    }
