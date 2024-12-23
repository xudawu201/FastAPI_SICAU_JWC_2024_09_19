import secrets
import uvicorn
from fastapi import FastAPI, Depends, Cookie, HTTPException, Response
from pydantic import BaseModel
from fastapi import Request
from fastapi.templating import Jinja2Templates
import pathlib
import passlib.context

app = FastAPI()

# 获得文件夹路径
BASE_PATH = pathlib.Path(__file__).resolve().parent
TemplatesJinja2 = Jinja2Templates(directory=str(BASE_PATH / "templates"))

# 设置密码哈希算法为 pbkdf2_sha256
pwd_context = passlib.context.CryptContext(schemes=["pbkdf2_sha256"])

# 验证密码和哈希密码
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 获得哈希密码
def get_password_hash(password):
    return pwd_context.hash(password)

# 用户模型
class User(BaseModel):
    username: str
    password: str

# 模拟的用户数据库，包含哈希密码
fake_users_db = {
    "xudawu": {
        "username": "xudawu", 
        "hashed_password": '$pbkdf2-sha256$29000$aw3BuNf6H8MYQ8j5X0tJ6Q$8nX0D7HpWq34L.GctNkUgqx9iI1DQWbBW4MMlqMj4jo'
        # "hashed_password": get_password_hash("test")
        },
    # "jane_smith": {"username": "jane_smith", "hashed_password": get_password_hash("secret_jane")},
    # "alice": {"username": "alice", "hashed_password": get_password_hash("secret_alice")},
    # "bob": {"username": "bob", "hashed_password": get_password_hash("secret_bob")},
    # "charlie": {"username": "charlie", "hashed_password": get_password_hash("secret_charlie")}
}

# 假设这是存储token与其对应用户的简单字典
active_tokens = {}

def get_current_user(session_token: str = Cookie(None)):
    """
    验证Cookie中的session_token是否有效，这里是简化的版本，实际应用中应该有更安全的验证机制。
    """
    user = active_tokens.get(session_token)
    if user is not None:
        return user
    else:
        raise HTTPException(status_code=401, detail="Invalid session token")

@app.post("/login")
async def login(response: Response, user: User):
    if user.username in fake_users_db:
        stored_user = fake_users_db[user.username]
        # 验证密码是否正确
        if verify_password(user.password, stored_user["hashed_password"]):
            token = secrets.token_hex(16)
            active_tokens[token] = user.username  # 将生成的token与用户名关联起来
            print("active_tokens:", active_tokens)
            # 设置cookie的有效时间，max_age的秒数
            response.set_cookie(key="session_token", value=token, max_age=10, httponly=True)
            return {
                "username": user.username,
                "token": token,
                "active_tokens": active_tokens,
                "message": f"Login successful for user {user.username}"
            }
    raise HTTPException(status_code=401, detail="Incorrect username or password")

@app.get("/protected-route")
async def protected_route(user: str = Depends(get_current_user)):
    """
    受保护的路由，只有携带有效Cookie的请求才能访问
    """
    return {"message": f"Welcome back, {user}!"}

from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
async def read_login_page(request: Request):
    context = {"request": request, "cookies": request.cookies}
    return TemplatesJinja2.TemplateResponse("login_test_2024_10_10.html", context)

# 返回成功登录的页面
@app.get("/login_success", response_class=HTMLResponse)
async def login_success_page(request: Request):
    context = {"request": request, "cookies": request.cookies}
    return TemplatesJinja2.TemplateResponse("login_sucess_test_2024_10_10.html", context)

@app.get("/verify-token")
async def verify_token(user: str = Depends(get_current_user)):
    """
    验证 session_token 是否有效。
    如果有效，返回 200 状态码；如果无效，返回 401。
    """
    return {"message": "Token is valid."}

# 退出登录接口
@app.post("/logout")
async def logout(response: Response):
    """
    清除客户端的 session_token cookie，实现用户退出登录
    """
    response.delete_cookie("session_token")  # 删除session_token cookie
    return {"message": "Logout successful."}

# 主函数，用于启动FastAPI应用程序
if __name__ == "__main__":
    # debug 模式
    uvicorn.run("fastapi_security_login_2024_10_10:app", host="127.0.0.1", port=8000, reload=True)
