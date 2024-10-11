'''
Author: xudawu
Date: 2024-09-20 09:11:00
LastEditors: xudawu
LastEditTime: 2024-10-11 15:15:47
'''
import secrets
import uvicorn
from fastapi import FastAPI, Depends, Cookie, HTTPException, Response, status
from pydantic import BaseModel
from fastapi import Request
from fastapi.templating import Jinja2Templates
import fastapi
import typing
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
import pathlib
import passlib.context
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# 初始化FastAPI应用
app = FastAPI()

# 设置JWT密钥和算法
jwt_secret_key_str = "74701188166a9ee01a13cfa21de9532d4aa94a2f7a921500a3ad0b64e250461a"
algorithm_str = "HS256"
# 设置令牌的过期时间
access_token_expire_minutes_int = 15
# 设置cookie的过期时间
cookie_expire_minutes_int = 10

# 获得文件夹路径
BASE_PATH = pathlib.Path(__file__).resolve().parent
TemplatesJinja2 = Jinja2Templates(directory=str(BASE_PATH / "templates"))

# 用户模型
class User(BaseModel):
    username: str
    password: str
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

class TokenData(BaseModel):
    username: str | None = None


# 设置密码哈希算法为 pbkdf2_sha256
pwd_context = passlib.context.CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 模拟的用户数据库，现在包含5个用户
fake_users_db = {
    "xudawu": {
        "username": "xudawu", 
        "password": "test",
        'hashed_password': '$pbkdf2-sha256$29000$/L/3vndOCaEUQugdo1QK4Q$lvyt1fz9PIH5F8gjdo53Jj2Db./tkTsIYueT5tIYCxM'
        },
    "jane_smith": {"username": "jane_smith", "password": "secret_jane"},
    "alice": {"username": "alice", "password": "secret_alice"},
    "bob": {"username": "bob", "password": "secret_bob"},
    "charlie": {"username": "charlie", "password": "secret_charlie"}
}

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


# 创建访问令牌的函数
def create_access_token(data: dict, expires_delta: typing.Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    # 未设置超时时间，则默认设置为 15 分钟
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    # 生成 JWT 令牌
    encoded_jwt = jwt.encode(to_encode, jwt_secret_key_str, algorithm=algorithm_str)
    return encoded_jwt

# 从Cookie中获取并验证JWT Token
def get_current_user(token: typing.Annotated[str, fastapi.Depends(oauth2_scheme)],session_token: str = Cookie(None)):
    if not session_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing session token")

    try:
        payload = jwt.decode(session_token, jwt_secret_key_str, algorithms=[algorithm_str])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    # 获得当前活动用户信息
    user = fake_users_db.get(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return username

# 用户登录接口
@app.post("/login")
async def login(response: Response, user: User):
    if user.username in fake_users_db and user.password == fake_users_db[user.username]["password"]:
        token_data = {"sub": user.username}
        token = create_access_token(data=token_data, expires_delta=timedelta(minutes=access_token_expire_minutes_int))
        # 设置Cookie超时时间，max_age单位为秒
        response.set_cookie(key="session_token", value=token, httponly=True, max_age=cookie_expire_minutes_int, secure=False)
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
    uvicorn.run("fastapi_security_login_2024_10_10:app", host="127.0.0.1", port=8000, reload=True)
