from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
import pyodbc
from template import TemplatesJinja2SuperSearch  # 保持模板导入

router = APIRouter()

# 数据库连接
def get_db_connection():
    database_url = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;PORT=1433;DATABASE=jxgl_all;UID=sa;PWD=sicau_jwc_sqlserver123;Encrypt=no;TrustServerCertificate=yes'
    return pyodbc.connect(database_url)

# 数据模型
class TableColumn(BaseModel):
    column_name: str
    data_type: str

class Table(BaseModel):
    table_name: str
    columns: List[TableColumn]

# 首页渲染
@router.get("/super_search", response_class=HTMLResponse)
async def super_search_page(request: Request):
    return TemplatesJinja2SuperSearch.TemplateResponse("super_search.html", {"request": request})

# 搜索表接口
@router.get("/search")
async def search_tables(query: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    # 查询匹配的列名及所属表
    cursor.execute("SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE COLUMN_NAME LIKE ?", f"%{query}%")
    result = cursor.fetchall()

    # 存储匹配的表格和列
    tables = {}
    for table_name, column_name in result:
        if table_name not in tables:
            tables[table_name] = []
        tables[table_name].append(column_name)

    # 查询所有表名，确保即使没有匹配的列也返回这些表
    cursor.execute("SELECT DISTINCT TABLE_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME LIKE ?", f"%{query}%")
    table_names = cursor.fetchall()

    # 对于没有匹配列的表格，依然显示它们，但不添加列信息
    for (table_name,) in table_names:
        if table_name not in tables:
            tables[table_name] = []

    conn.close()

    return {"tables": [{"table_name": table_name, "columns": columns} for table_name, columns in tables.items()]}

# 查看表列接口
@router.get("/table/{table_name}/columns")
async def get_table_columns(table_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ?", table_name)
    result = cursor.fetchall()

    columns = [{"column_name": row[0], "data_type": row[1]} for row in result]
    conn.close()

    return {"table_name": table_name, "columns": columns}

# 获取表数据接口（分页）
@router.get("/table/{table_name}/data")
async def get_table_data(table_name: str, page: int = 1, limit: int = 10):
    conn = get_db_connection()
    cursor = conn.cursor()

    # 获取表的总数据量
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    total_records = cursor.fetchone()[0]

    # 分页查询表的数据
    cursor.execute(f"SELECT * FROM {table_name} ORDER BY (SELECT NULL) OFFSET ? ROWS FETCH NEXT ? ROWS ONLY", (page - 1) * limit, limit)
    result = cursor.fetchall()

    # 获取表的列名
    columns = [desc[0] for desc in cursor.description]

    # 生成返回的表数据
    data = [dict(zip(columns, row)) for row in result]
    total_pages = (total_records + limit - 1) // limit  # 计算总页数

    conn.close()

    return {"table_name": table_name, "data": data, "total_pages": total_pages}

# 获取字段匹配的值
@router.get("/table/{table_name}/fields")
async def get_field_matches(table_name: str, query: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [desc[0] for desc in cursor.description]
    result = cursor.fetchall()

    matches = []
    for row in result:
        for i, value in enumerate(row):
            if value and query in str(value):
                matches.append({
                    "table_name": table_name,
                    "column_name": columns[i],
                    "match_value": value
                })

    conn.close()

    return {"fields": matches}
