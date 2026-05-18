from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_database
from models import User, Book, Purchase, Bill
from schemas import PurchaseAdd
from auth import get_current_user

router = APIRouter(prefix="/purchase", tags=["进货管理"])


# 进货接口
@router.post("/add")
async def add_purchase(
        purchaseadd:PurchaseAdd,
        current_user_id: int = Depends(get_current_user),
        db: AsyncSession = Depends(get_database)
):
    # 判断登录状态
    operator = await db.get(User,current_user_id)
    if not operator:
        raise HTTPException(status_code=401, detail="用户不存在或未登录")

    # 查找是否当前的书在Book中
    result = await db.execute(select(Book).where(Book.isbn == purchaseadd.isbn))
    book = result.scalars().first()
    # 不在则插入新的book
    if not book:
        if purchaseadd.isbn is None:
            raise HTTPException(status_code=400,detail="ISBN号必须为不为空")
        if purchaseadd.title is None:
            raise HTTPException(status_code=400,detail="书名不能为空")
        book_data = purchaseadd.model_dump()
        book_data.pop("buy_price")
        book_data.pop("purchase_quantity")
        new_book = Book(**book_data)
        db.add(new_book)
        await db.flush() # 立刻获取book_id
        book = new_book #更新book变量

    # 添加到Purchase表中
    add_data = {
        "book_id": book.book_id,
        "buy_price": purchaseadd.buy_price,
        "purchase_quantity": purchaseadd.purchase_quantity,
        "user_id": current_user_id
    }
    new_purchase = Purchase(**add_data)
    db.add(new_purchase)
    await db.flush()
    order_id = new_purchase.order_id
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"数据库写入异常：{str(e)}")
    return {
        "message":"进货成功",
        "order_id":order_id,
        "isbn":book.isbn,
        "title":book.title,
        "buy_price":purchaseadd.buy_price,
        "purchase_quantity": purchaseadd.purchase_quantity
    }

# 付款接口
@router.post("/pay")
async def pay_purchase(
        order_id:int = Query(ge=0,description="订单号"),
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

    # 判断图书是否可付款
    if result.book_status != "unpaid":
        raise HTTPException(status_code=400, detail="图书不可付款")

    # 图书付款
    result.book_status = "paid"

    #计入账单
    bill_data={
        "bill_type":"expense",
        "amount":result.buy_price*result.purchase_quantity,
        "related_id":order_id
    }
    new_bill = Bill(**bill_data)
    db.add(new_bill)
    await db.flush()
    bill_id = new_bill.bill_id
    amount = new_bill.amount

    # 提交数据
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500,detail=f"数据库写入异常：{str(e)}")
    return {
        "message":"付款成功",
        "bill_id":bill_id,
        "bill_type":"expense",
        "amount":amount
    }

# 退货接口
@router.put("/return")
async def return_purchase(
        order_id:int = Query(ge=0,description="订单号"),
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

    # 判断图书是否可退货
    if result.book_status != "unpaid":
        raise HTTPException(status_code=400,detail="图书不可退货")

    # 将图书退货
    result.book_status = "returned"

    # 提交数据
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500,detail=f"数据库写入异常：{str(e)}")
    return {
        "message":"退货成功"
    }
