from template import TemplatesJinja2SuperSearch

from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict, Any
import pyodbc

# app = FastAPI()
router = APIRouter()

# 连接数据库
def get_db_connection():
    database_url = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;PORT=1433;DATABASE=jxgl_all;UID=sa;PWD=sicau_jwc_sqlserver123;Encrypt=no;TrustServerCertificate=yes'
    conn = pyodbc.connect(database_url)
    return conn

# 数据模型
class TableColumn(BaseModel):
    column_name: str
    data_type: str

class Table(BaseModel):
    table_name: str
    columns: List[TableColumn]

# 首页：渲染搜索页面
@router.get("/super_search", response_class=HTMLResponse)
async def super_search(request: Request):
    return TemplatesJinja2SuperSearch.TemplateResponse("super_search.html", {"request": request})

# 搜索相关表格接口
@router.get("/search")
async def search_tables(query: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 查找包含查询词的表和列
    cursor.execute("SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE COLUMN_NAME LIKE ?", f"%{query}%")
    result = cursor.fetchall()
    
    # 组织结果
    tables = {}
    for table_name, column_name in result:
        if table_name not in tables:
            tables[table_name] = []
        tables[table_name].append(column_name)
    
    # 关闭数据库连接
    conn.close()
    
    return {"tables": [{"table_name": table_name, "columns": columns} for table_name, columns in tables.items()]}

# 获取指定表的列名
@router.get("/table/{table_name}/columns")
async def get_table_columns(table_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 获取表的列名和数据类型
    cursor.execute("SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ?", table_name)
    columns = [{"column_name": row[0], "data_type": row[1]} for row in cursor.fetchall()]
    
    conn.close()
    return {"table_name": table_name, "columns": columns}

# 获取指定表的数据
@router.get("/table/{table_name}/data")
async def get_table_data(table_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 获取表的所有数据
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    
    data = []
    for row in rows:
        data.append(dict(zip(columns, row)))
    
    conn.close()
    return {"table_name": table_name, "data": data}

# 获取与指定表相关的表格
@router.get("/related_tables/{table_name}")
async def get_related_tables(table_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 查询该表的相关表格（通过外键关系）
    cursor.execute("""
        SELECT 
            fk.name AS FK_name,
            tp.name AS RelatedTable
        FROM 
            sys.foreign_keys AS fk
        INNER JOIN 
            sys.tables AS tp ON fk.referenced_object_id = tp.object_id
        WHERE 
            fk.parent_object_id = OBJECT_ID(?)
    """, table_name)
    
    related_tables = [row[1] for row in cursor.fetchall()]
    
    conn.close()
    return {"table_name": table_name, "related_tables": related_tables}

# 添加路由到 FastAPI 应用
# app.include_router(router)