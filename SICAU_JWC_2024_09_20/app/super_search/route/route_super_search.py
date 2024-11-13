from fastapi import APIRouter, Request,WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pypinyin import pinyin, Style
# 保持模板导入
from template import TemplatesJinja2SuperSearch
# 引入数据库模块
from database import database_connection
import asyncio

router = APIRouter()

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

# 首页渲染
@router.get("/super_search", response_class=HTMLResponse)
async def super_search_page(request: Request):
    return TemplatesJinja2SuperSearch.TemplateResponse("super_search.html", {"request": request})

# 搜索表接口
@router.get("/search")
async def search_tables(query: str):
    # 获取数据库连接和游标
    DatabaseConnection,DatabaseCursor = database_connection.get_database_connection_cursor()

    # 查询匹配的列名及所属表
    DatabaseCursor.execute("SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE COLUMN_NAME LIKE ?", f"%{query}%")
    result = DatabaseCursor.fetchall()

    # 存储匹配的表格和列
    tables = {}
    for table_name, column_name in result:
        if table_name not in tables:
            tables[table_name] = []
        tables[table_name].append(column_name)

    # 查询所有表名，确保即使没有匹配的列也返回这些表
    DatabaseCursor.execute("SELECT DISTINCT TABLE_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME LIKE ?", f"%{query}%")
    table_names = DatabaseCursor.fetchall()

    # 对于没有匹配列的表格，依然显示它们，但不添加列信息
    for (table_name,) in table_names:
        if table_name not in tables:
            tables[table_name] = []

    # 关闭游标和连接
    DatabaseCursor.close()
    DatabaseConnection.close()

    # 按第一个字的拼音顺序对表名进行排序
    sorted_tables = dict(sorted(tables.items(), key=lambda item: pinyin(item[0][0], style=Style.NORMAL)[0][0]))

    response_dict={"tables": sorted_tables}

    return response_dict

# 查看表列接口
@router.get("/table/{table_name}/columns")
async def get_table_columns(table_name: str):
    # 获取数据库连接和游标
    DatabaseConnection,DatabaseCursor = database_connection.get_database_connection_cursor()

    DatabaseCursor.execute("SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ?", table_name)
    result = DatabaseCursor.fetchall()

    columns = [{"column_name": row[0], "data_type": row[1]} for row in result]

    # 关闭游标和连接
    DatabaseCursor.close()
    DatabaseConnection.close()

    return {"table_name": table_name, "columns": columns}

# 获取表数据接口（分页）
@router.get("/table/{table_name}/data")
async def get_table_data(table_name: str, page: int = 1, limit: int = 10, filter: str = ''):
    # 获取数据库连接和游标
    DatabaseConnection,DatabaseCursor = database_connection.get_database_connection_cursor()

    # 获取表的列名
    DatabaseCursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ?", table_name)
    columns = [row[0] for row in DatabaseCursor.fetchall()]

    # 构建查询条件，逐列查询
    where_clauses = []
    params = []

    if filter:  # 如果有筛选条件
        for column in columns:
            where_clauses.append(f"{column} LIKE ?")  # 每列条件使用 LIKE
            params.append(f"%{filter}%")  # 对每列使用筛选条件
        where_condition = " OR ".join(where_clauses)
    else:
        where_condition = ""  # 没有筛选条件时，不加 WHERE

    # 获取表的总数据量，根据筛选条件进行查询
    query = f"SELECT COUNT(*) FROM {table_name}"
    if where_condition:
        query += f" WHERE {where_condition}"
    
    DatabaseCursor.execute(query, params)  # 执行查询，传入参数
    total_records = DatabaseCursor.fetchone()[0]
    total_pages = (total_records + limit - 1) // limit

    # 获取当前页的数据
    query = f"SELECT * FROM {table_name}"
    if where_condition:
        query += f" WHERE {where_condition}"

    query += f" ORDER BY (SELECT NULL) OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
    params.append((page - 1) * limit)  # 页码偏移量
    params.append(limit)  # 每页条数

    DatabaseCursor.execute(query, params)  # 执行查询，传入参数
    rows = DatabaseCursor.fetchall()

    # 获取表结构信息，columns 必须从表的元数据中获取
    columns = [col[0] for col in DatabaseCursor.description]  # 从描述中提取列名

    # 将结果转换为字典形式
    data = []
    for row in rows:
        row_dict = dict(zip(columns, row))  # 将列名和行数据配对成字典
        data.append(row_dict)

    # 关闭游标和连接
    DatabaseCursor.close()
    DatabaseConnection.close()

    return {"table_name": table_name, "data": data, "columns": columns, "total_pages": total_pages}

# 获取字段匹配的值
@router.get("/table/{table_name}/fields")
async def get_field_matches(table_name: str, query: str):
    # 获取数据库连接和游标
    DatabaseConnection,DatabaseCursor = database_connection.get_database_connection_cursor()

    DatabaseCursor.execute(f"SELECT * FROM {table_name}")
    columns = [desc[0] for desc in DatabaseCursor.description]
    result = DatabaseCursor.fetchall()

    matches = []
    for row in result:
        for i, value in enumerate(row):
            if value and query in str(value):
                matches.append({
                    "table_name": table_name,
                    "column_name": columns[i],
                    "match_value": value
                })

    # 关闭游标和连接
    DatabaseCursor.close()
    DatabaseConnection.close()

    return {"fields": matches}

# 查询整个数据库
@router.websocket("/ws_search_database")
async def database_search(websocket: WebSocket):

    # 连接前端进行实时通信
    manager = WebSocketConnectionManager()
    await manager.connect(websocket)

    # 获取数据库连接和游标
    DatabaseConnection,DatabaseCursor = database_connection.get_database_connection_cursor()

    # 获取数据库中的所有表
    DatabaseCursor.execute("SELECT table_name FROM information_schema.tables WHERE table_type='BASE TABLE'")
    tables = DatabaseCursor.fetchall()

    # 初始化一个字典来存储匹配的表和列和内容
    select_tables_dict= {}

    try:
        # 接收来自客户端的消息，可以用于触发后端操作
        search_keyword = await websocket.receive_text()
        
        # 遍历每个表并检查是否包含关键词
        for table in tables:
            table_name = table[0]
            # 使用方括号包裹表名，以处理特殊字符
            DatabaseCursor.execute(f"SELECT * FROM [{table_name}]")
            columns = [column[0] for column in DatabaseCursor.description]  # 获取列名
            column_types = [column[1] for column in DatabaseCursor.description]  # 获取列的数据类型
            
            # 遍历列并检查是否包含关键词
            for column, column_type in zip(columns, column_types):
                # 检查列的类型，跳过bytearray类型的列内容
                if str(column_type) == "<class 'bytearray'>":
                    # print(f"跳过列 {column}，类型为 bytearray")
                    continue

                try: 
                    # 执行查询并实时发送匹配结果
                    # DatabaseCursor.execute() 和 fetchone() 是阻塞操作，如果查询需要时间，后端会被阻塞，导致 WebSocket 无法及时发送更新信息
                    # 使用 asyncio.to_thread() 将阻塞的数据库查询放到单独的线程中，这样事件循环就可以继续处理其他任务（比如发送 WebSocket 消息）
                    query = f"SELECT [{column}] FROM [{table_name}] WHERE CAST([{column}] AS NVARCHAR(MAX)) LIKE ?"
                    results = await asyncio.to_thread(DatabaseCursor.execute, query, ('%' + search_keyword + '%',))
                    # 只获取第一条相关数据
                    result = await asyncio.to_thread(DatabaseCursor.fetchone)
                    
                    if result:
                        # print(f"表名: {table_name}, 列名: {column}, 相关内容: {result[0]}")

                        # 将匹配的内容发送给前端实时显示
                        await websocket.send_json({'table_name': table_name,'column': column, 'content': result[0]})
                        # await websocket.send_text(f"表名: {table_name}, 列名: {column}, 相关内容: {result[0]}")
                        # 将匹配的内容存储到字典中
                        select_tables_dict[table_name] = {column:result[0]}
                        break  # 每个表只显示第一条相关信息
                except Exception as e:
                    # print(f"错误在表 {table_name}, 列 {column}: {e}")
                    pass

        # 按第一个字的拼音顺序对表名进行排序
        sorted_tables = dict(sorted(select_tables_dict.items(), key=lambda item: pinyin(item[0][0], style=Style.NORMAL)[0][0]))
        # 设置返回的字典格式
        response_dict={"tables": sorted_tables}
        # 返回查询结束标志
        await websocket.send_text('search_done')
        # 将字典转换为 JSON 格式并发送给前端
        await websocket.send_json(response_dict)

    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(websocket)
        
    # 关闭游标和连接
    DatabaseCursor.close()
    DatabaseConnection.close()


if __name__ == '__main__':
    # 引入文件目录设置
    import sys
    import os
    # 添加项目文件根目录到系统路径
    module_path = os.path.abspath('')
    sys.path.append(module_path)

    from template import TemplatesJinja2SuperSearch

    select_tables_dict = get_database('专业')

