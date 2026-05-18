from decimal import Decimal
from typing import Optional, Literal
from pydantic import BaseModel, Field

# 用户登录
class UserLogin(BaseModel):
    username: str = Field(default="", max_length=30, description="用户名")
    password: str = Field(default="", max_length=40, description="密码")

# 用户注册
class UserRegister(BaseModel):
    username: str = Field(default="", max_length=30, description="用户名")
    password: str = Field(default="", max_length=40, description="密码")
    real_name: str = Field(default="", max_length=30, description="真实姓名")
    age: Optional[int] = Field(default=None, ge=0, le=120, description="年龄")
    gender: Literal['male', 'female'] = Field(description="性别")

# 用户更新
class UserUpdate(BaseModel):
    target_user_id: int = Field(description="想要修改的目标用户ID")
    username: Optional[str] = Field(default=None, max_length=30, description="用户名")
    old_password: Optional[str] = Field(default=None, max_length=40, description="旧密码")
    password: Optional[str] = Field(default=None, max_length=40, description="新密码")
    real_name: Optional[str] = Field(default=None, max_length=30, description="真实姓名")
    age: Optional[int] = Field(default=None, ge=0, le=120, description="年龄")
    gender: Optional[Literal['male', 'female']] = Field(default=None, description="性别")

# 图书更新
class BookUpdate(BaseModel):
    book_id: Optional[int] = Field(default=None, description="书籍编号")
    title: Optional[str] = Field(default=None, max_length=70, description="书名")
    publisher: Optional[str] = Field(default=None, max_length=50, description="出版社")
    author: Optional[str] = Field(default=None, max_length=50, description="作者")
    price: Optional[Decimal] = Field(default=None, ge=0.00, description="价格")

# 进货添加
class PurchaseAdd(BaseModel):
    isbn: str = Field(max_length=20, description="书籍编号")
    buy_price: Decimal = Field(ge=0.00, description="购买价格")
    purchase_quantity: int = Field(ge=0, description="进货数量")
    title: Optional[str] = Field(default=None, max_length=70, description="书名")
    publisher: Optional[str] = Field(default=None, max_length=50, description="出版社")
    author: Optional[str] = Field(default=None, max_length=50, description="作者")
