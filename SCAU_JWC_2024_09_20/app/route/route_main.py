'''
Author: xudawu
Date: 2024-10-15 10:29:13
LastEditors: xudawu
LastEditTime: 2024-10-18 14:49:32
'''
from fastapi import APIRouter, Cookie, Request
from fastapi.responses import HTMLResponse
from app.template import TemplatesJinja2Login, TemplatesJinja2Public
from app.model import user

router = APIRouter()

# 登录注册页
@router.get("/", response_class=HTMLResponse)
async def read_login_page(request: Request, session_token: str = Cookie(None)):
    route_user = user.cookie_tokens_dict.get(session_token)
    context = {"request": request, "user": route_user}
    return TemplatesJinja2Login.TemplateResponse("login.html", context)

# 主页面
@router.get("/main", response_class=HTMLResponse)
async def login_success_page(request: Request, session_token: str = Cookie(None)):
    route_user = user.cookie_tokens_dict.get(session_token)
    context = {"request": request, "user": route_user}
    return TemplatesJinja2Public.TemplateResponse("main.html", context)

