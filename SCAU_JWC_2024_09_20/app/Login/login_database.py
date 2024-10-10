from datetime import datetime, timedelta
from typing import Annotated
import jwt
from fastapi import Depends, FastAPI, HTTPException, status, Cookie, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
import passlib.context
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

# 创建用于 JWT 令牌签名的随机密钥。
jwt_secret_key_str = "74701188166a9ee01a13cfa21de9532d4aa94a2f7a921500a3ad0b64e250461a"
# 创建指定 JWT 令牌签名算法的变量
algorithm_str = "HS256"
# 设置令牌过期时间
access_token_expire_minutes_int = 60  # 设置为60分钟

# 模拟用户数据库
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

# 静态文件和模板配置
# app.mount("/frotend/template", StaticFiles(directory="/frotend/template"), name="static")
templates = Jinja2Templates(directory="templates")


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
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
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
    response: Response
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=access_token_expire_minutes_int)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    # 设置 HttpOnly 的 cookie，过期时间为 1 小时
    response.set_cookie(key="session_token", value=access_token, max_age=3600, httponly=True)
    return Token(access_token=access_token, token_type="bearer")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("login_test_2024_10_10.html", {"request": request})

@app.get("/success")
async def login_success(request: Request):
    return templates.TemplateResponse("login_sucess_test_2024_10_10.html", {"request": request})

@app.get("/verify-token")
async def verify_token(response: Response, session_token: str = Cookie(None)):
    """
    验证 session_token 是否有效。
    如果有效，返回 200 状态码；如果无效，返回 401。
    """
    if session_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No valid session token found.")
    
    try:
        payload = jwt.decode(session_token, jwt_secret_key_str, algorithms=[algorithm_str])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session token.")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session token.")
    
    return {"message": "Token is valid."}

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

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='login:app', host='127.0.0.1', port=8000, reload=True)
