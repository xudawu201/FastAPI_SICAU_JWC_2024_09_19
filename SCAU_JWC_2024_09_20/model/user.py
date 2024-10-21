'''
Author: xudawu
Date: 2024-10-15 10:28:56
LastEditors: xudawu
LastEditTime: 2024-10-21 10:40:53
'''
from pydantic import BaseModel

# 用户模型
class User(BaseModel):
    id: int
    username: str
    password: str
    flag: str

# 模拟的用户数据库，包含哈希密码
users_db = {
    "xudawu": {
        "username": "xudawu",
        "hashed_password": '$pbkdf2-sha256$29000$aw3BuNf6H8MYQ8j5X0tJ6Q$8nX0D7HpWq34L.GctNkUgqx9iI1DQWbBW4MMlqMj4jo'
    }
}

# cookie存储字典，用于验证cookie有效性
cookie_tokens_dict = {}