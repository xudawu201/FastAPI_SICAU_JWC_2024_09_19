'''
Author: xudawu
Date: 2024-09-19 20:12:48
LastEditors: xudawu
LastEditTime: 2024-10-10 16:28:41
'''
import fastapi
import fastapi.templating
from fastapi.responses import HTMLResponse
import uvicorn

app = fastapi.FastAPI()

# 初始化 Jinja2 模板引擎
templates = fastapi.templating.Jinja2Templates(directory='templates')

# @app.get('/')
# def index(request: fastapi.Request):
#     message = 'this is home page'
#     books = ['book1', 'book2', 'book3']
#     test_age = 16
#     return templates.TemplateResponse(
#         'test.html', 
#         {   
#             'request':request,
#             'html_message': message,
#             'book': books,
#             'age': test_age
#          }
#         )

# response_class=HTMLResponse：明确声明返回的是 HTML 响应。
# 这不是必须的，因为 TemplateResponse 默认会返回 HTML 响应，但这为代码增加了可读性。
@app.get("/", response_class=HTMLResponse)
async def login_success_page(request: fastapi.Request):
    return templates.TemplateResponse("test.html", {"request": request})

if __name__ == '__main__':
    # 启动服务器
    uvicorn.run(app='FastAPITest2_2024_09_19:app', host='127.0.0.1', port=8000, reload=True)
