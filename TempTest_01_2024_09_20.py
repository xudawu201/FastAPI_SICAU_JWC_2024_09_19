import fastapi
from fastapi.responses import HTMLResponse

app = fastapi.FastAPI()

@app.post("/login")
async def login(request: fastapi.Request):
    request_data = await request.json()
    username = request_data.get("username")
    password = request_data.get("password")
    if username == "xudawu":
        print("测试成功")
        response_content_dict = {
            "username": username,
            "flag": '中文测试'
        }
        return response_content_dict

@app.post("/click")
async def click_handler():
    return {"response": "你点击了div！"}

@app.post("/filter")
async def filter_handler():
    return {"response": "你选择了筛选框选项！"}

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
            <div id="clickable-div" style="width: 200px; height: 100px; background-color: lightblue; text-align: center; line-height: 100px; cursor: pointer;">
                点击这里
            </div>
            <p id="div-response"></p>
            
            <select id="filter-select" style="margin-top: 20px; cursor: pointer;">
                <option value="">选择一个选项</option>
                <option value="option1">选项 1</option>
                <option value="option2">选项 2</option>
            </select>
            <p id="filter-response"></p>

            <iframe src="/iframe" width="100%" height="300" style="border: none;"></iframe>

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
                        body: JSON.stringify({ username, password })
                    });

                    const result = await response.json();
                    if (result.flag === '中文测试') {
                        alert('前后端通信成功')
                    }
                };

                document.getElementById('clickable-div').onclick = async () => {
                    const response = await fetch('/click', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });

                    const result = await response.json();
                    document.getElementById('div-response').innerText = result.response;
                };

                document.getElementById('filter-select').onchange = async (e) => {
                    const response = await fetch('/filter', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });

                    const result = await response.json();
                    document.getElementById('filter-response').innerText = result.response;
                };
            </script>
        </body>
    </html>
    """

# iframe页面，嵌入前端代码
@app.get("/iframe", response_class=HTMLResponse)
async def read_iframe():
    return """
    <html>
        <body>
            <h2>Login (Iframe)</h2>
            <form id="iframe-login-form">
                <input type="text" id="iframe-username" placeholder="Username" required>
                <input type="password" id="iframe-password" placeholder="Password" required>
                <button type="submit">Login</button>
            </form>

            <p id="iframe-response"></p>
            <div id="iframe-clickable-div" style="width: 200px; height: 100px; background-color: lightblue; text-align: center; line-height: 100px; cursor: pointer;">
                点击这里 (Iframe)
            </div>
            <p id="iframe-div-response"></p>
            
            <select id="iframe-filter-select" style="margin-top: 20px; cursor: pointer;">
                <option value="">选择一个选项</option>
                <option value="option1">选项 1</option>
                <option value="option2">选项 2</option>
            </select>
            <p id="iframe-filter-response"></p>

            <script>
                document.getElementById('iframe-login-form').onsubmit = async (e) => {
                    e.preventDefault();
                    const username = document.getElementById('iframe-username').value;
                    const password = document.getElementById('iframe-password').value;

                    const response = await fetch('/login', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ username, password })
                    });

                    const result = await response.json();
                    if (result.flag === '中文测试') {
                        alert('前后端通信成功 (Iframe)')
                    }
                };

                document.getElementById('iframe-clickable-div').onclick = async () => {
                    const response = await fetch('/click', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });

                    const result = await response.json();
                    document.getElementById('iframe-div-response').innerText = result.response;
                };

                document.getElementById('iframe-filter-select').onchange = async (e) => {
                    const response = await fetch('/filter', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });

                    const result = await response.json();
                    document.getElementById('iframe-filter-response').innerText = result.response;
                };
            </script>
        </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
