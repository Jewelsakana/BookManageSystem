from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_database
from models import User, Bill
from auth import get_current_user

router = APIRouter(prefix="/bill", tags=["账单管理"])

# 查看订单接口
@router.get("/check")
async def check_bill(
    first_time:datetime = Query(description="开始时间"),
    last_time:datetime = Query(description="结束时间"),
    current_user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_database)
):
    # 判断登录状态
    operator = await db.get(User,current_user_id)
    if not operator:
        raise HTTPException(status_code=401, detail="用户不存在或未登录")

    result = await db.execute(select(Bill).where(Bill.billed_at.between(first_time,last_time)))
    bills = result.scalars().all()
    if bills is None:
        raise HTTPException(status_code=404,detail=f"{first_time}到{last_time}不存在订单")

    return bills

# 查看所有订单的接口（只有SuperAdmin才能查看）
@router.get("/checkall")
async def check_all_bil(
    current_user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_database)
):
    # 判断登录状态
    operator = await db.get(User,current_user_id)
    if not operator:
        raise HTTPException(status_code=401, detail="用户不存在或未登录")
    
    if operator.user_role != "super_admin":
        raise HTTPException(status_code=403,detail="不是超级管理员，无法查看")

    results =await db.execute(select(Bill))
    bills = results.scalars().all()

    if bills is None:
        raise HTTPException(status_code=404,detail="没有订单")

    return bills
        


