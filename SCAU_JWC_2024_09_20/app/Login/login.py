'''
Author: xudawu
Date: 2024-10-09 13:42:12
LastEditors: xudawu
LastEditTime: 2024-10-10 17:22:22
'''

from datetime import datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status,Cookie
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
import passlib.context
from pydantic import BaseModel

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


# to get a string like this run:
# 创建用于 JWT 令牌签名的随机密钥。
# jwt_secret_key_str = secrets.token_hex(32)
jwt_secret_key_str = "74701188166a9ee01a13cfa21de9532d4aa94a2f7a921500a3ad0b64e250461a"
# 创建指定 JWT 令牌签名算法的变量 ALGORITHM，本例中的值为 "HS256"
algorithm_str = "HS256"
# 创建设置令牌过期时间的变量
access_token_expire_minutes_int = 10

# 密码test
fake_users_db = {
    "xudawu": {
        "username": "xudawu",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$pbkdf2-sha256$29000$/L/3vndOCaEUQugdo1QK4Q$lvyt1fz9PIH5F8gjdo53Jj2Db./tkTsIYueT5tIYCxM",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str

# 设置密码哈希算法为 pbkdf2_sha256
pwd_context = passlib.context.CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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


# 创建访问令牌
def create_access_token(data: dict, expires_delta: timedelta | None = None):
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

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, jwt_secret_key_str, algorithms=[algorithm_str])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        # 验证当前活动用户是否是之前登录获得令牌的用户
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    # 获得当前活动用户信息
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=access_token_expire_minutes_int)
    # 获得访问令牌
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]

# 获得用户登录的cookie
class Cookies(BaseModel):
    model_config = {"extra": "forbid"}
    
    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None


@app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookie()]):
    return cookies

if __name__ == '__main__':
    # 启动服务器
    import uvicorn
    uvicorn.run(app='login:app', host='127.0.0.1', port=8000, reload=True)