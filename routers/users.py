import secrets
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from database import get_database
from models import User
from schemas import UserLogin, UserRegister, UserUpdate
from auth import get_current_user, get_current_token, get_md5, token_storage, token_time

router = APIRouter(prefix="/user", tags=["用户管理"])

# 用户登录接口
@router.post('/login')
async def user_login(user_login: UserLogin, db: AsyncSession = Depends(get_database)):
    # 根据用户名查询用户
    result = await db.execute(select(User).where(User.username == user_login.username))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=400, detail="用户或密码名错误")

    # 对输入的明文密码进行MD5加密，然后与数据库中的密文相比
    if user.user_password != get_md5(user_login.password):
        raise HTTPException(status_code=400, detail="用户或密码名错误")

    user_token = secrets.token_urlsafe(32)
    token_storage[user_token] = user.user_id
    token_time[user_token] = datetime.now()

    # 验证成功，返回用户信息与权限
    return {
        "message": "登录成功",
        "token": user_token,
        "user_id": user.user_id,
        "username": user.username,
        "user_role": user.user_role,
        "real_name": user.real_name,
        "age": user.age,
        "gender": user.gender
    }

# 用户创建接口
@router.post('/register')
async def user_register(user_register:UserRegister,
                        current_user_id:int = Depends(get_current_user),
                        db:AsyncSession = Depends(get_database)):
    # 判断登录状态
    op_result = await db.execute(select(User).where(User.user_id == current_user_id))
    op_user = op_result.scalars().first()
    if not op_user :
        raise HTTPException(status_code=401,detail="用户不存在或未登录")
    if op_user.user_role != "super_admin":
        raise HTTPException(status_code=403,detail="不是超级管理员，权限不足")

    # 判断用户名是否已存在
    result = await db.execute(select(User).where(User.username == user_register.username))
    user = result.scalars().first()
    if user:
        raise HTTPException(status_code=400,detail="用户名已经存在")

    # 注册用户
    try:
        # 用户数据的处理，加密
        user_data = user_register.model_dump()
        user_data["user_password"] = get_md5(user_data["password"])
        user_data.pop("password")
        user_data["user_role"] = "common_admin"

        # 添加到数据库
        new_user = User(**user_data)
        db.add(new_user)
        await db.commit()

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500,detail=f"数据库写入异常：{str(e)}")

    return {
        "message": "注册用户成功"
    }

# 修改用户信息接口
@router.put("/update")
async def user_update(user_update:UserUpdate,
                      current_user_id:int = Depends(get_current_user),
                      db:AsyncSession = Depends(get_database)):
    # 判断登录状态
    operator = await db.get(User,current_user_id)
    if not operator :
        raise HTTPException(status_code=401,detail="用户不存在或未登录")

    # 普通管理员只能修改自己的信息
    if operator.user_role == "common_admin":
        if current_user_id != user_update.target_user_id:
            raise HTTPException(status_code=403,detail="普通管理员不能修改别人的信息")

    # 获取需要修改的用户
    user = await db.get(User,user_update.target_user_id)
    if not user:
        raise HTTPException(status_code=404,detail="修改的用户不存在")

    # 用户信息的修改
    if user_update.username is not None:
        if user_update.username != user.username:
            user_result = await db.execute(select(User).where(User.username == user_update.username))
            if user_result.scalars().first():
                raise HTTPException(status_code=400,detail="用户名已经被其他用户占用")
        user.username = user_update.username

    if user_update.password is not None:
        if user_update.old_password is None:
            raise HTTPException(status_code=400,detail="旧密码为空")
        if user.user_password != get_md5(user_update.old_password):
            raise HTTPException(status_code=400,detail="旧密码必须正确")
        user.user_password = get_md5(user_update.password)

    if user_update.real_name is not  None:
        user.real_name = user_update.real_name

    if user_update.gender is not  None:
        user.gender = user_update.gender

    if user_update.age is not None:
        user.age = user_update.age
    # 提交数据
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500,detail=f"数据库写入异常：{str(e)}")
    return {
        "message":"用户数据修改成功"
    }

# 用户查看信息接口
@router.get("/view")
async def user_view(current_user_id:int = Depends(get_current_user),
                    target_user_id: int = Query(None,description="查看的目标用户ID"),
                    all_user: bool = Query(False,description="是否查看所有用户信息"),
                    db:AsyncSession = Depends(get_database)):
    # 判断登录状态
    operator = await db.get(User,current_user_id)
    if not operator:
        raise HTTPException(status_code=401, detail="用户不存在或未登录")

    # 所有用户信息查阅
    if all_user:
        if operator.user_role != "super_admin":
            raise HTTPException(status_code=403,detail="只有超级管理员可以查看所有用户")
        result = await db.execute(select(User))
        users =result.scalars().all()
        user_list = []
        for u in users:
            user_list.append({
                "user_id": u.user_id,
                "user_name": u.username,
                "user_role": u.user_role,
                "real_name": u.real_name,
                "age": u.age,
                "gender": u.gender
            })
        return user_list

    if target_user_id is None:
        raise HTTPException(status_code=404,detail="缺少目标用户ID参数")

    # 权限查阅
    if operator.user_role == "common_admin":
        if current_user_id != target_user_id :
            raise HTTPException(status_code=403, detail="普通管理员不能查看别人的信息")

    # 单个信息查阅
    user = await db.get(User,target_user_id)
    if not user:
        raise HTTPException(status_code=404,detail="用户不存在")

    return {
        "user_id": user.user_id,
        "user_name": user.username,
        "user_role": user.user_role,
        "real_name": user.real_name,
        "age": user.age,
        "gender": user.gender
    }

# 用户登出接口
@router.get("/logout")
async def user_logout(current_user_token:str =Depends(get_current_token),
                      current_user_id:int = Depends(get_current_user),
                      db:AsyncSession = Depends(get_database)):
    # 判断登录状态
    operator = await db.get(User,current_user_id)
    if not operator:
        raise HTTPException(status_code=401, detail="用户不存在或未登录")

    token_storage.pop(current_user_token)
    token_time.pop(current_user_token)
    return {
        "message":"登出成功"
    }

