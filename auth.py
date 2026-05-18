import hashlib
import secrets
import datetime
from fastapi import HTTPException, Header


#存储token->user_id
token_storage = {}
#存储token->time
token_time = {}
max_time = datetime.timedelta(seconds=3600)

# 将密码转换为md5格式
def get_md5(password: str) -> str:
    return hashlib.md5(password.encode('utf-8')).hexdigest()

# 依赖项：从token中获取到当前用户的ID
async def get_current_user(token: str = Header(..., alias="Authorization")):
    # 去掉可能存在的"Bearer" 前缀
    if token.lower().startswith("bearer "):
        token = token[7:]
    if token not in token_storage:
        raise HTTPException(status_code=401, detail="无效的token")
    if datetime.datetime.now() - token_time[token] >= max_time:
        token_storage.pop(token)
        token_time.pop(token)
        raise HTTPException(status_code=401,detail="过期的token")
    return token_storage[token]

# 依赖项：从token中获取到当前用户的ID
async def get_current_token(token: str = Header(..., alias="Authorization")):
    # 去掉可能存在的"Bearer" 前缀
    if token.lower().startswith("bearer "):
        token = token[7:]
    if token not in token_storage:
        raise HTTPException(status_code=401, detail="无效的token")
    if datetime.datetime.now() - token_time[token] >= max_time:
        token_storage.pop(token)
        token_time.pop(token) 
        raise HTTPException(status_code=401,detail="过期的token")
    return token
