'''
Author: xudawu
Date: 2024-09-29 11:21:28
LastEditors: xudawu
LastEditTime: 2024-09-30 16:11:18
'''

import databases
import sqlalchemy
import fastapi
import pydantic
import typing


## Postgres Database
# 数据库类型://用户名:密码@主机名:端口号/数据库名
database_url = 'postgresql://postgres:123@127.0.0.1:5432/test_2024_09_29'
DataBaseEngine = sqlalchemy.create_engine(database_url)

app = fastapi.FastAPI()

@app.get("/")
async def find_all_users():
    list_info = [(1,2),(3,4),(1,'中文测试')]
    # 使用SQL语句查询数据
    # with DataBaseEngine.connect() as DataBaseConnection:
    DataBaseConnection = DataBaseEngine.connect()
    select_sql_str = 'SELECT * FROM student'
    result_set = DataBaseConnection.execute(sqlalchemy.text(select_sql_str))
    await list_info = result_set.fetchall()
    # for row in result_set:
    #     # print(row,row._get_by_key_impl_mapping('name'))
    #     # print(row[1],row.name)

    #     list_info.append(row)

    print(list_info)

    DataBaseConnection.close()

    return {"message": "Hello World", "data": list_info}

    # return 'List all user'

if __name__ == "__main__":
    import uvicorn
    # 启动服务器
    uvicorn.run(app='main:app', host="127.0.0.1", port=8000,reload=True)