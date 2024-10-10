'''
Author: xudawu
Date: 2024-10-09 17:00:32
LastEditors: xudawu
LastEditTime: 2024-10-09 17:10:46
'''

import passlib.context

# 初始化加密上下文
pwd_context = passlib.context.CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# 定义密码
password = "test"

# 生成哈希
hashed_password_1 = pwd_context.hash(password)
# hashed_password_1 = '$pbkdf2-sha256$29000$bW1tzTlnDIHwHgOg1JrTeg$ks6k90wAUBC8QyeBUU9T6B77y2XMlQx.yxQw9FFtQMo'
hashed_password_2 = pwd_context.hash(password)
# hashed_password_2 = '$pbkdf2-sha256$29000$r3WOkZLynlOq9T6n1Nobww$1ksVePSQ65NS4UQy/gkNHL2MqBQN4Nd/zS4nh1k5s4I'

# 打印不同的哈希值
print(f"哈希值 1: {hashed_password_1}")
print(f"哈希值 2: {hashed_password_2}")

# 验证密码
is_correct_1 = pwd_context.verify(password, hashed_password_1)
is_correct_2 = pwd_context.verify(password, hashed_password_2)

print(f"密码匹配哈希 1: {is_correct_1}")  # True
print(f"密码匹配哈希 2: {is_correct_2}")  # True
