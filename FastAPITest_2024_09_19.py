'''
Author: xudawu
Date: 2024-09-19 20:12:48
LastEditors: xudawu
LastEditTime: 2024-09-20 10:41:20
'''
import fastapi
import uvicorn

app = fastapi.FastAPI()

# 添加首页,装饰器定义访问的路径
@app.get('/')
def index():
    return 'hello world'

# 添加user页面,装饰器定义访问的路径
@app.get('/user')
def user():
    return 'user'

if __name__ == '__main__':
    # 启动服务器
    uvicorn.run(app='FastAPITest_2024_09_19:app', host='127.0.0.1', port=8000, reload=True)
