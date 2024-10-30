'''
Author: xudawu
Date: 2024-09-20 09:11:00
LastEditors: xudawu
LastEditTime: 2024-10-30 08:51:47
'''
from fastapi import FastAPI, Cookie, HTTPException
from fastapi.responses import RedirectResponse

app = FastAPI()

# 模拟一个简单的用户会话存储
session_tokens = {"valid_token": "user1"}  # 示例有效的 token

@app.get("/verify_cookie")
async def verify_cookie(token: str = Cookie(None)):
    if token in session_tokens:
        return {"status": "valid"}  # 返回有效状态
    else:
        # 如果 session 无效，重定向到登录页面
        return RedirectResponse(url="/login", status_code=302)

@app.get("/login")
async def login():
    return {"message": "Please log in."}

@app.get("/main")
async def main():
    return {"message": "Welcome to the main page!"}

# 主函数启动应用程序
if __name__ == "__main__":
    import uvicorn
    # 绑定到所有可用的网络接口,可以被任何 IP 地址访问
    uvicorn.run(app, host="0.0.0.0", port=8000)