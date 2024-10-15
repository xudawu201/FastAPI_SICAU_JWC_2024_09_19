'''
Author: xudawu
Date: 2024-10-15 10:30:23
LastEditors: xudawu
LastEditTime: 2024-10-15 10:34:46
'''
import passlib.context

# 设置密码哈希算法为 pbkdf2_sha256
pwd_context = passlib.context.CryptContext(schemes=["pbkdf2_sha256"])

# 验证密码和哈希密码
def verify_password(plain_password, hashed_password):
    is_correct = pwd_context.verify(plain_password, hashed_password)
    if is_correct and pwd_context.needs_update(hashed_password):
        print("Password hash needs to be updated")
    return is_correct

# 获得哈希密码
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)