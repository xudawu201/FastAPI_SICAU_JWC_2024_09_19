'''
Author: xudawu
Date: 2024-09-29 17:54:42
LastEditors: xudawu
LastEditTime: 2024-10-11 15:58:53
'''
from fastapi import Depends, FastAPI, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordRequestForm
import passlib.context
from pydantic import BaseModel


# 假设的用户数据库
fake_users_db = {
    "xudawu": {
        "username": "xudawu",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$pbkdf2-sha256$29000$/L/3vndOCaEUQugdo1QK4Q$lvyt1fz9PIH5F8gjdo53Jj2Db./tkTsIYueT5tIYCxM",
        "disabled": False,
    }
}

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

# 设置密码哈希算法为 pbkdf2_sha256
pwd_context = passlib.context.CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

app = FastAPI()
 
# 验证密码和哈希密码
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 获得哈希密码
def get_password_hash(password):
    return pwd_context.hash(password)

# 获得用户信息
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

# 验证用户
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "Login successful"}

if __name__ == '__main__':
    # 启动服务器
    import uvicorn
    uvicorn.run(app='Temtest01_2024_09_29:app', host='127.0.0.1', port=8000, reload=True)
