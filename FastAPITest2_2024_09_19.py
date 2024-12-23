'''
Author: xudawu
Date: 2024-09-19 20:12:48
LastEditors: xudawu
LastEditTime: 2024-10-10 16:03:16
'''
import fastapi
import fastapi.templating
import uvicorn

app = fastapi.FastAPI()

# 初始化 Jinja2 模板引擎
templates = fastapi.templating.Jinja2Templates(directory='templates')

@app.get('/')
def index(request: fastapi.Request):
    message = 'this is home page'
    books = ['book1', 'book2', 'book3']
    test_age = 16
    return templates.TemplateResponse(
        'test.html', 
        {   
            'request':request,
            'html_message': message,
            'book': books,
            'age': test_age
         }
        )

if __name__ == '__main__':
    # 启动服务器
    uvicorn.run(app='FastAPITest2_2024_09_19:app', host='127.0.0.1', port=8000, reload=True)
