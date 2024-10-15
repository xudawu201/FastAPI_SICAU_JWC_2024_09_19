'''
Author: xudawu
Date: 2024-10-09 13:42:12
LastEditors: xudawu
LastEditTime: 2024-10-15 10:33:19
'''
import secrets
import uvicorn
from fastapi import Depends, Cookie, HTTPException, Response
from pydantic import BaseModel
from fastapi import Request
from fastapi.templating import Jinja2Templates
import pathlib
import passlib.context
from fastapi.staticfiles import StaticFiles
import fastapi

app = fastapi.FastAPI()

# 获得文件夹路径
BASE_PATH = pathlib.Path(__file__).resolve().parent

# 挂载静态文件路径
# SCAU_JWC_2024_09_20\frontend\template
app.mount("/login_static_path", StaticFiles(directory=BASE_PATH / "login/frontend/static"))
app.mount("/public_static_path", StaticFiles(directory='SCAU_JWC_2024_09_20/frontend/static'))

# 使用 Jinja2 模板渲染 HTML 文件
TemplatesJinja2Login = Jinja2Templates(directory=BASE_PATH / "login/frontend/template")
TemplatesJinja2Public = Jinja2Templates(directory='SCAU_JWC_2024_09_20/frontend/template')

# 设置密码哈希算法为 pbkdf2_sha256
pwd_context = passlib.context.CryptContext(schemes=["pbkdf2_sha256"])

# 设置Cookie的过期时间，单位为秒
cookie_token_expire_second_int = 10

# 验证密码和哈希密码
def verify_password(plain_password, hashed_password):
    # 验证密码是否正确
    is_correct = pwd_context.verify(plain_password, hashed_password)
    # 检查密码是否需要更新
    if is_correct and pwd_context.needs_update(hashed_password):
        print("Password hash needs to be updated")
        # 这里可以选择将新哈希存入数据库
    
    return is_correct

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
    }
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
        # raise HTTPException(status_code=401, detail="Invalid session token")
        return None  # 修改为返回None而不是抛出异常

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
            response.set_cookie(key="session_token", value=token, max_age=cookie_token_expire_second_int, httponly=True)
            return {
                "username": user.username,
                "token": token,
                "active_tokens": active_tokens,
                "message": f"Login successful for user {user.username}"
            }
    raise HTTPException(status_code=401, detail="Incorrect username or password")

@app.get("/", response_class=fastapi.responses.HTMLResponse)
async def read_login_page(request: Request,session_token: str = Cookie(None)):
    user = active_tokens.get(session_token)
    context = {"request": request, "user": user}  # 传递用户信息到模板
    return TemplatesJinja2Login.TemplateResponse("login.html", context)

# 返回成功登录的页面
@app.get("/main", response_class=fastapi.responses.HTMLResponse)
async def login_success_page(request: Request,session_token: str = Cookie(None)):
    user = active_tokens.get(session_token)
    context = {"request": request, "user": user}  # 传递用户信息到模板
    return TemplatesJinja2Public.TemplateResponse("main.html", context)

# 验证 cookie 接口
@app.get("/verify-token")
async def verify_token(user: str = Depends(get_current_user)):
    """
    验证 session_token 是否有效。
    如果有效，返回 200 状态码；如果无效，返回 401。
    """
    if user:
        return {"message": f"Welcome back, {user}!"}
    raise HTTPException(status_code=401, detail="Invalid session token")

# 退出登录接口
@app.post("/logout")
async def logout(response: Response,session_token: str = Cookie(None)):
    """
    清除客户端的 session_token cookie，实现用户退出登录
    """
    if session_token in active_tokens:
        del active_tokens[session_token]  # 从active_tokens中移除用户
    response.delete_cookie("session_token")  # 删除session_token cookie
    return {"message": "Logout successful."}

# 注册接口
@app.post("/register")
async def register(user: User):
    """
    注册新用户，存储用户名和哈希密码。
    """
    # 初始化回应字典
    response_context_dict = {
            "username": '',
            'already_name_flag': '',
            "message": '',
            }
    # 检查用户名是否已存在
    if user.username in fake_users_db:
        response_context_dict['already_name_flag'] = 'true'
        response_context_dict["message"] = "username already registered"
        return response_context_dict

    # 用户名没有重复，注册新用户
    hashed_password = get_password_hash(user.password)
    # 将新用户名和哈希密码添加到数据库中
    fake_users_db[user.username] = {
        "username": user.username,
        "hashed_password": hashed_password
    }

    response_context_dict['username'] = user.username
    response_context_dict['already_name_flag'] = 'false'
    response_context_dict["message"] = "registration successful"
    return response_context_dict

# 主函数，用于启动FastAPI应用程序
if __name__ == "__main__":
    # debug 模式
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
