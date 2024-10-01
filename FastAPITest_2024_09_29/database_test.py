'''
Author: xudawu
Date: 2024-09-29 17:55:38
LastEditors: xudawu
LastEditTime: 2024-09-29 18:01:31
'''
import sqlalchemy

database_url = 'postgresql://postgres:123@127.0.0.0:5432/test_2024_09_29'
engine = sqlalchemy.create_engine(database_url)
SessinLoacal = sqlalchemy.orm.sessionmaker(autocommit=False,autoflu=False,bind=engine)
Base = sqlalchemy.ext.declarative.declarative_base()