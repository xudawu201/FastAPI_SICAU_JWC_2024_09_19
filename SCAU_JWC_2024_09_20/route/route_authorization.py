'''
Author: xudawu
Date: 2024-10-15 10:29:05
LastEditors: xudawu
LastEditTime: 2024-11-04 16:43:09
'''
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response
from security.password_utils import verify_password, get_password_hash
from model import user
from service import service_user
import secrets
import fastapi

router = APIRouter()

# 设置Cookie的过期时间，单位为秒
cookie_token_expire_second_int = 60*60*7

# 获取当前用户
def get_current_user(session_token: str = Cookie(None)):
    auth_user = user.cookie_tokens_dict.get(session_token)
    if auth_user:
        return auth_user
    return None

# 登录验证
# request 参数用于接收客户端的请求，而 response 参数允许修改响应的属性，如状态码或头信息
@router.post("/login")
async def login(request: fastapi.Request,response: Response):
    """
    处理登录请求，验证用户名和密码，并设置session_token cookie。
    """
    # 获取请求体中的 JSON 数据
    request_data = await request.json()
    username_str = request_data.get("username")
    password_str = request_data.get("password")
    # 初始化回应字典
    response_context_dict = {
            "username": '',
            "token": None,
            "active_tokens": None,
            'login_flag': '',
            "have_user": 'true',
            }
    # 根据用户名查询数据库中是否有匹配的数据
    rows = service_user.get_user_by_employee_no(username_str)
    # 如果查询结果不为空，则用户名存在
    if len(rows) != 0 :
        # 从查询结果中获取用户信息
        UserInfo = rows[0]
        # 验证密码是否正确
        if verify_password(password_str, UserInfo.哈希密码):
            token = secrets.token_hex(16)
            user.cookie_tokens_dict[token] = username_str  # 将生成的token与用户名关联起来
            # print("active_tokens:", user.cookie_tokens_dict)
            # 设置cookie的有效时间，max_age的秒数
            response.set_cookie(key="session_token", value=token, max_age=cookie_token_expire_second_int, httponly=True)
            # 返回登录成功的信息
            response_context_dict['username']= username_str
            response_context_dict['token']= token
            response_context_dict['active_tokens']= user.cookie_tokens_dict
            response_context_dict['login_flag']= 'true'
            return response_context_dict
        else:
            response_context_dict['login_flag']= 'false'
            return response_context_dict
    else:
        # 用户名不存在
        response_context_dict['have_user']= 'false'
        return response_context_dict

# 注册验证
@router.post("/register")
async def register(request: fastapi.Request):
    """
    注册新用户，存储用户名和哈希密码。
    """
    # 获取请求体中的 JSON 数据
    request_data = await request.json()
    username_str = request_data.get("username")
    password_str = request_data.get("password")

    # 初始化回应字典
    response_context_dict = {
            "username": '',
            'already_name_flag': '',
            "message": '',
            }
    # 检查用户名是否已存在
    if username_str in user.users_db:
        response_context_dict['already_name_flag'] = 'true'
        response_context_dict["message"] = "username already registered"
        return response_context_dict

    # 用户名没有重复，注册新用户
    hashed_password = get_password_hash(password_str)
    # 将新用户名和哈希密码添加到数据库中
    user.users_db[username_str] = {
        "username": username_str,
        "hashed_password": hashed_password
    }

    response_context_dict['username'] = username_str
    response_context_dict['already_name_flag'] = 'false'
    response_context_dict["message"] = "registration successful"
    print("register user:", user.users_db[username_str])
    
    # 返回注册成功的信息
    return response_context_dict

# 登出验证
@router.post("/logout")
async def logout(response: Response, session_token: str = Cookie(None)):
    """
    清除客户端的 session_token cookie，实现用户退出登录
    """
    if session_token in user.cookie_tokens_dict:
        del user.cookie_tokens_dict[session_token]  # 从active_tokens中移除用户
    response.delete_cookie("session_token")  # 删除session_token cookie
    return {"message": "Logout successful."}

# 登录页验证cookie有效性
@router.get("/verify_cookie_login")
async def verify_cookie_login(ver_user: str = Depends(get_current_user)):
    if ver_user:
        return fastapi.responses.RedirectResponse(url="/main")
    else:
        HTTPException(status_code=401, detail="Invalid session token")

# 其他页面验证cookie有效性
@router.get("/verify_cookie")
async def verify_cookie(ver_user: str = Depends(get_current_user)):
    if ver_user:
        return {"message": f"Welcome back, {ver_user}!"}
    else:
        return fastapi.responses.RedirectResponse(url="/")