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
async def get_table_data(table_name: str, page: int = 1, limit: int = 10, filter: str = ''):
    conn = get_db_connection()
    cursor = conn.cursor()

    # 获取表的列名
    cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ?", table_name)
    columns = [row[0] for row in cursor.fetchall()]

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
    
    cursor.execute(query, params)  # 执行查询，传入参数
    total_records = cursor.fetchone()[0]
    total_pages = (total_records + limit - 1) // limit

    # 获取当前页的数据
    query = f"SELECT * FROM {table_name}"
    if where_condition:
        query += f" WHERE {where_condition}"

    query += f" ORDER BY (SELECT NULL) OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
    params.append((page - 1) * limit)  # 页码偏移量
    params.append(limit)  # 每页条数

    cursor.execute(query, params)  # 执行查询，传入参数
    rows = cursor.fetchall()

    # 获取表结构信息，columns 必须从表的元数据中获取
    columns = [col[0] for col in cursor.description]  # 从描述中提取列名

    # 将结果转换为字典形式
    data = []
    for row in rows:
        row_dict = dict(zip(columns, row))  # 将列名和行数据配对成字典
        data.append(row_dict)

    conn.close()

    return {"table_name": table_name, "data": data, "columns": columns, "total_pages": total_pages}



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
