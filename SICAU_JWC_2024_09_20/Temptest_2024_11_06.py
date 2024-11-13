'''
Author: xudawu
Date: 2024-11-06 16:28:23
LastEditors: xudawu
LastEditTime: 2024-11-13 17:15:10
'''
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates
import os
import asyncio

app = FastAPI()

# 设置模板目录为当前工作目录
templates = Jinja2Templates(directory=os.path.abspath("."))

# WebSocket连接管理器
class WebSocketConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("TempTest_2024_11_05.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    manager = WebSocketConnectionManager()
    await manager.connect(websocket)
    try:
        # 接收来自客户端的消息，可以用于触发后端操作
        data = await websocket.receive_text()
        if data == "start":
            for i in range(20):
                await websocket.send_text(f"Step {i + 1}: {i}")
                # 等待0.1秒，模拟时间延迟
                await asyncio.sleep(0.1) 
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# 主函数启动应用程序
if __name__ == "__main__":
    import uvicorn
    # 绑定到所有可用的网络接口,可以被任何 IP 地址访问
    uvicorn.run(app="Temptest_2024_11_06:app", host="0.0.0.0", port=8000, reload=True)