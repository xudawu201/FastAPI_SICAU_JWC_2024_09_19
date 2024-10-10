'''
Author: xudawu
Date: 2024-10-09 09:54:46
LastEditors: xudawu
LastEditTime: 2024-10-09 13:31:38
'''
import pyodbc
import fastapi
import pydantic

# DRIVER:驱动名称,SERVER:服务器名称,DATABASE:数据库名称,UID:用户名,PWD:密码
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=JWC_SCAU_2024_10_08;UID=sa;PWD=123')
# pyodbc使用微软的官方驱动ODBC driver对于中文的兼容性好，不需要再额外使用字符编码设置
# 创建游标对象
cursor = cnxn.cursor()

# 执行SQL语句
# select_sql_str ='select * from Student_2024_10_08'
# cursor.execute(select_sql_str)
# print(cursor)
# row = cursor.fetchone()
# print(row)

# cursor.execute(select_sql_str)
# row = cursor.fetchone()
# # 使用索引访问列数据
# print('name:', row[1])
# # 使用列名访问列数据
# print('name:', row.name)

app = fastapi.FastAPI()

class User(pydantic.BaseModel):
    id: int
    name: str | None = None


@app.get("/", response_model=list[User])
async def main():
    list_info = []
    # 执行SQL语句
    select_sql_str ='select * from Student_2024_10_08'
    cursor.execute(select_sql_str)
    print(cursor)
    list_info = cursor.fetchall()
    # print(list_info)

    # FastAPI期望返回的是一个Pydantic模型
    # for i in range(len(list_info)): 
    #     User(id=list_info[i][0],name=list_info[i][1])
    #     list_info.append(User)
    
    items = [User(id=item[0], name=item[1]) for item in list_info]

    return {"message": "Hello World", "data":items}

    # return 'List all user'

if __name__ == "__main__":
    import uvicorn
    # 启动服务器
    uvicorn.run(app='main:app', host="127.0.0.1", port=8000,reload=True)