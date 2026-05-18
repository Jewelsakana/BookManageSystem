from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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
