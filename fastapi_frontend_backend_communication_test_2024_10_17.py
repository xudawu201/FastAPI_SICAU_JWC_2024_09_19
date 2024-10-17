'''
Author: xudawu
Date: 2024-09-20 09:11:00
LastEditors: xudawu
LastEditTime: 2024-10-17 18:14:22
'''
import fastapi
from fastapi.responses import HTMLResponse

app = fastapi.FastAPI()


@app.post("/login")
async def login(request: fastapi.Request):
    # 获取请求体中的 JSON 数据
    request_data = await request.json()
    username = request_data.get("username")
    password = request_data.get("password")
    if username == "xudawu":
        print("测试成功")
        response_content_dict={
            "username": username,
            "flag": '中文测试'
        }
        return response_content_dict

# 主页面，嵌入前端代码
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <body>
            <h2>Login</h2>
            <form id="login-form">
                <input type="text" id="username" placeholder="Username" required>
                <input type="password" id="password" placeholder="Password" required>
                <button type="submit">Login</button>
            </form>
            <p id="response"></p>
            <script>
                document.getElementById('login-form').onsubmit = async (e) => {
                    e.preventDefault();
                    const username = document.getElementById('username').value;
                    const password = document.getElementById('password').value;

                    const response = await fetch('/login', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ username, password })  // 只发送必要的字段
                    });

                    const result = await response.json();
                    if (result.flag ==='中文测试'){
                        alert('前后端通信成功')
                    }
                };
            </script>
        </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)