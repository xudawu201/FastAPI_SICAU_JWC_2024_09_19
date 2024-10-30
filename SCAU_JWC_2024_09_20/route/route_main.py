'''
Author: xudawu
Date: 2024-10-15 10:29:13
LastEditors: xudawu
LastEditTime: 2024-10-30 12:59:16
'''
from fastapi import APIRouter, Cookie, Request
from fastapi.responses import HTMLResponse
from model import user
from template import TemplatesJinja2Login
from template import TemplatesJinja2Public

router = APIRouter()

# 主页面
@router.get("/main", response_class=HTMLResponse)
async def login_success_page(request: Request, session_token: str = Cookie(None)):
    route_user = user.cookie_tokens_dict.get(session_token)
    context = {"request": request, "user": route_user}
    return TemplatesJinja2Public.TemplateResponse("main.html", context)

# 登录注册页
@router.get("/", response_class=HTMLResponse)
async def read_login_page(request: Request, session_token: str = Cookie(None)):
    route_user = user.cookie_tokens_dict.get(session_token)
    context = {"request": request, "user": route_user}
    return TemplatesJinja2Login.TemplateResponse("login.html", context)
