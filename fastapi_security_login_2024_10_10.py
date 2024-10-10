'''
Author: xudawu
Date: 2024-09-20 09:11:00
LastEditors: xudawu
LastEditTime: 2024-10-10 17:59:54
'''
import secrets
import uvicorn
from fastapi import FastAPI, Depends, Cookie, HTTPException, Response, status
from pydantic import BaseModel
from fastapi import Request
from fastapi.templating import Jinja2Templates
from typing import Optional
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
import pathlib

# 初始化FastAPI应用
app = FastAPI()

# 设置JWT密钥和算法
jwt_secret_key_str = "74701188166a9ee01a13cfa21de9532d4aa94a2f7a921500a3ad0b64e250461a"
algorithm_str = "HS256"
# 设置令牌的过期时间
access_token_expire_minutes_int = 15

# 获得文件夹路径
BASE_PATH = pathlib.Path(__file__).resolve().parent
TemplatesJinja2 = Jinja2Templates(directory=str(BASE_PATH / "templates"))

# 用户模型
class User(BaseModel):
    username: str
    password: str

# 模拟的用户数据库，现在包含5个用户
fake_users_db = {
    "xudawu": {"username": "xudawu", "password": "test"},
    "jane_smith": {"username": "jane_smith", "password": "secret_jane"},
    "alice": {"username": "alice", "password": "secret_alice"},
    "bob": {"username": "bob", "password": "secret_bob"},
    "charlie": {"username": "charlie", "password": "secret_charlie"}
}

# 创建访问令牌的函数
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, jwt_secret_key_str, algorithm=algorithm_str)
    return encoded_jwt

# 从Cookie中获取并验证JWT Token
def get_current_user(session_token: str = Cookie(None)):
    if not session_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing session token")

    try:
        payload = jwt.decode(session_token, jwt_secret_key_str, algorithms=[algorithm_str])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = fake_users_db.get(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return username

# 用户登录接口
@app.post("/login")
async def login(response: Response, user: User):
    if user.username in fake_users_db and user.password == fake_users_db[user.username]["password"]:
        token_data = {"sub": user.username}
        token = create_access_token(data=token_data, expires_delta=timedelta(seconds=access_token_expire_minutes_int))
        # 设置Cookie超时时间，max_age单位为秒
        response.set_cookie(key="session_token", value=token, httponly=True, max_age=10, secure=False)
        return {
            "username": user.username,
            "message": f"Login successful for user {user.username}",
        }
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

# 受保护的路由
@app.get("/protected-route")
async def protected_route(user: str = Depends(get_current_user)):
    return {"message": f"Welcome back, {user}!"}

# 验证Token是否有效
@app.get("/verify-token")
async def verify_token(user: str = Depends(get_current_user)):
    return {"message": "Token is valid."}

# 退出登录接口
@app.post("/logout")
async def logout(response: Response):
    """
    清除客户端的 session_token cookie，实现用户退出登录
    """
    response.delete_cookie("session_token")  # 删除session_token cookie
    return {"message": "Logout successful."}

# 返回登录页面
@app.get("/")
async def login_page(request: Request):
    context = {"request": request, "cookies": request.cookies}
    return TemplatesJinja2.TemplateResponse("login_test_2024_10_10.html", context)

# 返回登录成功页面
@app.get("/login_success")
async def login_success_page(request: Request):
    context={"request": request, "cookies": request.cookies}
    return TemplatesJinja2.TemplateResponse("login_sucess_test_2024_10_10.html", context)

# 主函数，用于启动FastAPI应用程序
if __name__ == "__main__":
    uvicorn.run("FastAPITest_2024_09_19:app", host="127.0.0.1", port=8000, reload=True)
