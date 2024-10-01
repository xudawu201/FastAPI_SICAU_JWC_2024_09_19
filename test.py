'''
Author: xudawu
Date: 2024-09-23 09:26:13
LastEditors: xudawu
LastEditTime: 2024-09-30 13:29:18
'''
from fastapi import FastAPI
import psycopg2

# 连接数据库
DataBaseConnect = psycopg2.connect(database="test_2024_09_29", user="postgres", password="123", host="localhost", port="5432")

# 创建一个游标对象
with DataBaseConnect.cursor() as DataBaseCursor:
    select_sql_str = 'SELECT * FROM student'
    DataBaseCursor.execute(select_sql_str)
    rows = DataBaseCursor.fetchall()

    for row in rows:
        print(row,)

app = FastAPI()


@app.get("/")
async def read_root():
    conn = psycopg2.connect(database="test_2024_09_29", user="postgres", password="123", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.execute("SELECT * FROM student")
    rows = cur.fetchall()
    conn.close()
    return {"message": "Hello World", "data": rows}

if __name__ == "__main__":
    import uvicorn
    # 启动服务器
    uvicorn.run(app='test:app', host="127.0.0.1", port=8000,reload=True)