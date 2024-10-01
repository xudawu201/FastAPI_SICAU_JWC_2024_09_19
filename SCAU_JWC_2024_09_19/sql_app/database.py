'''
Author: xudawu
Date: 2024-09-30 14:11:27
LastEditors: xudawu
LastEditTime: 2024-09-30 15:17:51
'''
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

## Postgres Database
# 数据库类型+数据库驱动://用户名:密码@主机名:端口号/数据库名
database_url = 'postgresql+psycopg2://postgres:123@127.0.0.1:5432/test_2024_09_29'

# 创建 SQLAlchemy 引擎
DataBaseEngine = sqlalchemy.create_engine(database_url)
# 创建一个SessionLocal类
SessionLocal = sqlalchemy.orm.sessionmaker(autocommit=False, autoflush=False, bind=DataBaseEngine)

# 创建一个Base类
Base = declarative_base()