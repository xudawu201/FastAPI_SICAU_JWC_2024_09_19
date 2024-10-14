'''
Author: xudawu
Date: 2024-09-19 20:12:48
LastEditors: xudawu
LastEditTime: 2024-10-14 16:46:17
'''
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.templating import Jinja2Templates
import fastapi
import pathlib



app = FastAPI()

# 设置模板和静态文件的目录
# 获得文件夹路径
BASE_PATH = pathlib.Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_PATH)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # 假设这是从数据库或其他来源获取的数据
    user_data = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25},
        {"name": "Charlie", "age": 35}
    ]
    context = {
        "request": request,
        "message": "Hello, World!",
        "users": user_data  # 传递用户数据到模板
    }
    return templates.TemplateResponse("FastAPITest_2024_10_14.html", context)

# 新的 API 路由，处理按钮点击后的数据请求
@app.get("/get_data", response_class=JSONResponse)
async def get_data():
    # 返回一些动态生成的数据
    response_context_dict = {
        "status": "success",
        "users": [
            {"name": "David", "age": 28},
            {"name": "Eva", "age": 32}
        ]
    }
    return response_context_dict


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
