'''
Author: xudawu
Date: 2024-10-15 10:29:13
LastEditors: xudawu
LastEditTime: 2024-10-15 15:23:04
'''
from fastapi import APIRouter, Cookie, Request
from fastapi.responses import HTMLResponse
from app.template import TemplatesJinja2Login, TemplatesJinja2Public
from app.model.user import active_tokens

router = APIRouter()

# 登录注册页
@router.get("/", response_class=HTMLResponse)
async def read_login_page(request: Request, session_token: str = Cookie(None)):
    user = active_tokens.get(session_token)
    context = {"request": request, "user": user}
    return TemplatesJinja2Login.TemplateResponse("login.html", context)

# 主页面
@router.get("/main", response_class=HTMLResponse)
async def login_success_page(request: Request, session_token: str = Cookie(None)):
    user = active_tokens.get(session_token)
    context = {"request": request, "user": user}
    return TemplatesJinja2Public.TemplateResponse("main.html", context)

