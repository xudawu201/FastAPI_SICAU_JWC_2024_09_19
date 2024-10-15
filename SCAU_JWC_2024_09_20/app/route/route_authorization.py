'''
Author: xudawu
Date: 2024-10-15 10:29:05
LastEditors: xudawu
LastEditTime: 2024-10-15 16:50:50
'''
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response
from app.security.password_utils import verify_password, get_password_hash
from app.model.user import User, fake_users_db, active_tokens
from pydantic import BaseModel
import secrets

router = APIRouter()

# 设置Cookie的过期时间，单位为秒
cookie_token_expire_second_int = 60*60*7

# 获取当前用户
def get_current_user(session_token: str = Cookie(None)):
    user = active_tokens.get(session_token)
    if user:
        return user
    return None

# 登录验证
@router.post("/login")
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

# 注册验证
@router.post("/register")
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

# 登出验证
@router.post("/logout")
async def logout(response: Response, session_token: str = Cookie(None)):
    """
    清除客户端的 session_token cookie，实现用户退出登录
    """
    if session_token in active_tokens:
        del active_tokens[session_token]  # 从active_tokens中移除用户
    response.delete_cookie("session_token")  # 删除session_token cookie
    return {"message": "Logout successful."}

# 验证cookie有效性
@router.get("/verify_cookie")
async def verify_cookie(user: str = Depends(get_current_user)):
    if user:
        return {"message": f"Welcome back, {user}!"}
    raise HTTPException(status_code=401, detail="Invalid session token")
