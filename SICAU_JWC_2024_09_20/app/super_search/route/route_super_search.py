'''
Author: xudawu
Date: 2024-10-24 14:45:08
LastEditors: xudawu
LastEditTime: 2024-11-06 17:47:42
'''
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

# 引入自定义文件
from template import TemplatesJinja2SuperSearch

router = APIRouter()

# 配置超参数信息

# 成绩可视化页
@router.get("/super_search", response_class=HTMLResponse)
async def super_search(request: Request):
    
    context = {
        "request": request,
        "message": "Hello, World!",
    }
    return TemplatesJinja2SuperSearch.TemplateResponse("super_search.html", context)