'''
Author: xudawu
Date: 2024-10-09 17:21:18
LastEditors: xudawu
LastEditTime: 2024-10-09 17:26:36
'''
import secrets
import jwt
from datetime import datetime, timedelta,timezone

# 使用 secrets 模块生成一个 256-bit (32-byte) 随机密钥
random_secret_key = secrets.token_hex(32)
print(f"随机生成的密钥: {random_secret_key}")

# JWT 的有效期（例如 1 小时）
expire_duration = timedelta(hours=1)

# 中国的时区，UTC+8
china_timezone = timezone(timedelta(hours=8))

# 获取当前的中国时间
current_time = datetime.now(china_timezone)
# 获取当前 UTC 时间
# current_time = datetime.now(timezone.utc)

# 设置过期时间为当前时间加上有效时长
expire_time = current_time + expire_duration

# 创建 JWT 负载（包括发行时间和过期时间）
payload = {
    "sub": "user123",  # 用户 ID
    "name": "John Doe",  # 用户名
    "iat": current_time,  # 发行时间
    "exp": expire_time,   # 过期时间
}

# 使用生成的随机密钥来签名 JWT 令牌
token = jwt.encode(payload, random_secret_key, algorithm="HS256")

print(f"生成的 JWT 令牌: {token}")
