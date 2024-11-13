'''
Author: xudawu
Date: 2024-09-30 15:33:46
LastEditors: xudawu
LastEditTime: 2024-11-13 15:43:48
'''
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates
from pypinyin import pinyin, Style
import os
import asyncio

app = FastAPI()

import pyodbc

# DRIVER:驱动名称,SERVER:服务器url,DATABASE:数据库名称,UID:用户名,PWD:密码,Encrypt=no不使用加密连接
# database_url = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=SICAU_JWC;UID=sa;PWD=sicau_jwc_sqlserver123;Encrypt=no;TrustServerCertificate=yes'
# 使用sqlserver本地调试数据库
# database_url = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=127.0.0.1;PORT=1433;DATABASE=jxgl_all;UID=sa;PWD=sicau_jwc_sqlserver123;Encrypt=no'

# 使用sqlserver容器部署数据库
database_url = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=172.18.0.1;PORT=1433;DATABASE=jxgl_all;UID=sa;PWD=sicau_jwc_sqlserver123;Encrypt=no'

# 使用信教中心sqlserver容器部署数据库
# database_url = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=10.99.84.138;PORT=32120;DATABASE=jxgl_all;UID=sa;PWD=sicau_jwc_sqlserver123;Encrypt=no'

# 使用postgres本地调试数据库
# database_url = 'DRIVER={PostgreSQL Unicode(x64)};SERVER=localhost;PORT=5432;DATABASE=SICAU_JWC;UID=postgres;PWD=docker_postgres;'

# 使用postgres部署容器数据库
# database_url = 'DRIVER={PostgreSQL Unicode(x64)};SERVER=postgres17;PORT=5432;DATABASE=SICAU_JWC;UID=postgres;PWD=docker_postgres;'

# 使用mysql本地调试数据库
# database_url = 'DRIVER={MySQL ODBC 9.1 Unicode Driver};SERVER=localhost;PORT=3306;DATABASE=SICAU_JWC;UID=root;PWD=sicau_jwc_mysql123;'

# 连接到数据库
def get_database_connection_cursor():
    try:
        # 获得数据库连接对象
        DatabaseConnection = pyodbc.connect(database_url)
        # pyodbc使用微软的官方驱动ODBC driver对于中文的兼容性好，不需要再额外使用字符编码设置
        # 获得游标对象
        DatabaseCursor = DatabaseConnection.cursor()

        return DatabaseConnection,DatabaseCursor
    except pyodbc.Error as e:
        print(f"Error: {e}")
        return None

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
    return templates.TemplateResponse("index.html", {"request": request})

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
                # await asyncio.sleep(0.1) 
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# 查询整个数据库
@app.websocket("/ws_search_database")
async def database_search(websocket: WebSocket):
    # 连接前端进行实时通信
    manager = WebSocketConnectionManager()
    await manager.connect(websocket)

    # 获取数据库连接和游标
    DatabaseConnection, DatabaseCursor = get_database_connection_cursor()

    # 获取数据库中的所有表
    DatabaseCursor.execute("SELECT table_name FROM information_schema.tables WHERE table_type='BASE TABLE'")
    tables = DatabaseCursor.fetchall()
    # 初始化一个字典来存储匹配的表和列和内容
    select_tables_dict = {}

    # try:
        
    # await websocket.send_text("中文测试1")
    # await websocket.send_text(tables[0][0])

    # 接收来自客户端的消息，可以用于触发后端操作
    search_keyword = await websocket.receive_text()
    search_keyword = "专业"

    # for i in range(20):
    #     await websocket.send_text(f"Step {i + 1}: {i}")
    #     await websocket.send_text("中文测试0")
    #     # 等待0.1秒，模拟时间延迟
    #     await asyncio.sleep(0.1)
    # await websocket.send_text("中文测试1")
    # 遍历每个表并检查是否包含关键词
    
    for table in tables:
        # await websocket.send_text("中文测试2")
        table_name = table[0]
        # 使用方括号包裹表名，以处理特殊字符
        DatabaseCursor.execute(f"SELECT * FROM [{table_name}]")
        columns = [column[0] for column in DatabaseCursor.description]  # 获取列名
        column_types = [column[1] for column in DatabaseCursor.description]  # 获取列的数据类型
        await websocket.send_text("中文测试2-1")
        # 遍历列并检查是否包含关键词
        for column, column_type in zip(columns, column_types):
            await websocket.send_text("中文测试3")
            # 检查列的类型，跳过bytearray类型的列内容
            if str(column_type) == "<class 'bytearray'>":
                print(f"跳过列 {column}，类型为 bytearray")
                continue
            # 使用方括号包裹列名，以处理特殊字符
            # DatabaseCursor.execute(f"SELECT [{column}] FROM [{table_name}] WHERE CAST([{column}] AS NVARCHAR(MAX)) LIKE ?", ('%' + search_keyword + '%',))
            # result = DatabaseCursor.fetchone()
            # 执行查询并实时发送匹配结果
            # DatabaseCursor.execute() 和 fetchone() 是阻塞操作，如果查询需要时间，后端会被阻塞，导致 WebSocket 无法及时发送更新信息
            # 使用 asyncio.to_thread() 将阻塞的数据库查询放到单独的线程中，这样事件循环就可以继续处理其他任务（比如发送 WebSocket 消息）
            try:
                query = f"SELECT [{column}] FROM [{table_name}] WHERE CAST([{column}] AS NVARCHAR(MAX)) LIKE ?"
                results = await asyncio.to_thread(DatabaseCursor.execute, query, ('%' + search_keyword + '%',))
                result = await asyncio.to_thread(DatabaseCursor.fetchone)
            # except Exception as e:
            #     # 如果出现错误，记录并跳过该列
            #     print(f"Error querying column {column} in table {table_name},{column_type}: {e}")
            #     continue

                if result:
                    # print(f"表名: {table_name}, 列名: {column}, 相关内容: {result[0]}")

    #                 # 将匹配的内容发送给前端实时显示
                    # await websocket.send_json({'table_name': table_name,'column': column, 'content': result[0]})
                    await websocket.send_text(f"表名: {table_name}, 列名: {column}, 相关内容: {result[0]}")
                # await websocket.send_text("中文测试4")
    #                 # 将匹配的内容存储到字典中
    #                 select_tables_dict[table_name] = {column: result[0]}
    #                 break  # 每个表只显示第一条相关信息
            except Exception as e:
                # 如果出现错误，记录并跳过该列
                # print(f"Error querying column {column} in table {table_name}: {e}")
                continue

    # # 按第一个字的拼音顺序对表名进行排序
    # sorted_tables = dict(sorted(select_tables_dict.items(), key=lambda item: pinyin(item[0][0], style=Style.NORMAL)[0][0]))
    
    # # 设置返回的字典格式
    # response_dict = {"tables": sorted_tables}
    
    # # 返回查询结束标志
    # await websocket.send_text('search_done')
    
    # # 将字典转换为 JSON 格式并发送给前端
    # await websocket.send_json(response_dict)
    
    # manager.disconnect(websocket)

    # # 关闭游标和连接
    # DatabaseCursor.close()
    # DatabaseConnection.close()


# 主函数启动应用程序
if __name__ == "__main__":
    import uvicorn
    # 绑定到所有可用的网络接口,可以被任何 IP 地址访问
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)