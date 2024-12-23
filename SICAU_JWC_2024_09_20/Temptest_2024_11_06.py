'''
Author: xudawu
Date: 2024-11-06 16:28:23
LastEditors: xudawu
LastEditTime: 2024-12-19 10:24:31
'''
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import asyncio

app = FastAPI()

@app.get("/")
async def get():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>WebSocket Reconnect Example</title>
    </head>
    <body>
        <h2>WebSocket Test</h2>
        <div id="messageBox"></div>
        <script>
            const socket = new WebSocket("ws://localhost:8000/ws");

            socket.onopen = () => {
                document.getElementById("messageBox").innerHTML += "WebSocket Connected!<br/>";
            };

            socket.onmessage = (event) => {
                document.getElementById("messageBox").innerHTML += "Received: " + event.data + "<br/>";
            };

            socket.onerror = (error) => {
                console.error("WebSocket Error: ", error);
            };

            socket.onclose = (event) => {
                document.getElementById("messageBox").innerHTML += "WebSocket Closed, attempting to reconnect...<br/>";
                setTimeout(() => {
                    console.log("Attempting to reconnect...");
                    connectWebSocket();
                }, 5000);
            };

            function connectWebSocket() {
                const newSocket = new WebSocket("ws://localhost:8000/ws");

                newSocket.onopen = () => {
                    document.getElementById("messageBox").innerHTML += "Reconnected to WebSocket!<br/>";
                };

                newSocket.onmessage = (event) => {
                    document.getElementById("messageBox").innerHTML += "Received: " + event.data + "<br/>";
                };

                newSocket.onerror = (error) => {
                    console.error("WebSocket Error: ", error);
                };

                newSocket.onclose = (event) => {
                    console.log("Reconnection failed, retrying...");
                    setTimeout(() => connectWebSocket(), 5000);
                };
            }
        </script>
    </body>
    </html>
    """)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_text("Hello, this is a message from server!")
            await asyncio.sleep(3)  # Sending message every 3 seconds
    except WebSocketDisconnect:
        print("Client disconnected")


# 主函数启动应用程序
if __name__ == "__main__":
    import uvicorn
    # 绑定到所有可用的网络接口,可以被任何 IP 地址访问
    uvicorn.run(app="Temptest_2024_11_06:app", host="0.0.0.0", port=8000, reload=True)