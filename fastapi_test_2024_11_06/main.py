'''
Author: xudawu
Date: 2024-09-30 15:33:46
LastEditors: xudawu
LastEditTime: 2024-11-07 08:58:01
'''
from fastapi import FastAPI, Query, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import pyodbc
from typing import List, Dict, Any
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

# 设置模板目录
templates = Jinja2Templates(directory="templates")

# 连接数据库
def get_db_connection():

    database_url = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;PORT=1433;DATABASE=jxgl_all;UID=sa;PWD=sicau_jwc_sqlserver123;Encrypt=no;TrustServerCertificate=yes'

    DatabaseConnection = pyodbc.connect(database_url)

    return DatabaseConnection

# 数据模型
class TableColumn(BaseModel):
    column_name: str
    data_type: str

class Table(BaseModel):
    table_name: str
    columns: List[TableColumn]

# 首页，渲染搜索页面
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 搜索表格接口
@app.get("/search")
async def search_tables(query: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 查询与搜索词相关的表名和列名
    cursor.execute(f"SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE COLUMN_NAME LIKE '%{query}%'")
    result = cursor.fetchall()
    
    tables = {}
    for table_name, column_name in result:
        if table_name not in tables:
            tables[table_name] = []
        tables[table_name].append(column_name)
    
    return {"tables": [{"table_name": table_name, "columns": columns} for table_name, columns in tables.items()]}

# 获取表格数据
@app.get("/table/{table_name}")
async def get_table_data(table_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 获取表格的所有数据
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    
    data = []
    for row in rows:
        data.append(dict(zip(columns, row)))
    
    return {"table_name": table_name, "data": data}

# 获取相关表格
@app.get("/related_tables/{table_name}")
async def get_related_tables(table_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 获取与指定表格相关的其他表格（通过外键关系）
    cursor.execute(f"""
        SELECT 
            fk.name AS FK_name,
            tp.name AS Table_Name
        FROM 
            sys.foreign_keys AS fk
        INNER JOIN 
            sys.tables AS tp ON fk.referenced_object_id = tp.object_id
        WHERE 
            fk.parent_object_id = OBJECT_ID('{table_name}')
    """)
    related_tables = cursor.fetchall()
    
    return {"table_name": table_name, "related_tables": [table[1] for table in related_tables]}


# 主函数启动应用程序
if __name__ == "__main__":
    # 绑定到所有可用的网络接口,可以被任何 IP 地址访问
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)

