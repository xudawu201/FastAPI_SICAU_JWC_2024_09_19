'''
Author: xudawu
Date: 2024-09-20 09:11:00
LastEditors: xudawu
LastEditTime: 2024-10-11 08:44:50
'''
import secrets
import uvicorn
from fastapi import FastAPI, Depends, Cookie, HTTPException, Response
from pydantic import BaseModel
from fastapi import Request
from fastapi.templating import Jinja2Templates
import pathlib


app = FastAPI()

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
    if user.username in fake_users_db and user.password == fake_users_db[user.username]["password"]:
        token = secrets.token_hex(16)
        active_tokens[token] = user.username  # 将生成的token与用户名关联起来
        print("active_tokens:", active_tokens)
        # 设置cookie的有效时间，max_age的秒数
        # httponly=True: 这个标志意味着 cookie 只能在服务器端访问，不能被 JavaScript 读取，增加了安全性。
        response.set_cookie(key="session_token", value=token, max_age=10,httponly=True)
        return {"username": user.username,
                "password": user.password,
                "token": token,
                "active_tokens": active_tokens,
                "message": f"Login successful for user {user.username}"}
 
    else:
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
    context={"request": request, "cookies": request.cookies}
    return TemplatesJinja2.TemplateResponse("login_sucess_test_2024_10_10.html", context)

@app.get("/verify-token")
async def verify_token(user: str = Depends(get_current_user)):
    """
    验证 session_token 是否有效。
    如果有效，返回 200 状态码；如果无效，返回 401。
    """
    return {"message": "Token is valid."}


# 主函数，用于启动FastAPI应用程序
if __name__ == "__main__":
    
    # debug 模式
    uvicorn.run("fastapi_cookie_session_2024_10_10:app", host="127.0.0.1", port=8000, reload=True)