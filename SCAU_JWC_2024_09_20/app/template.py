'''
Author: xudawu
Date: 2024-10-15 15:11:37
LastEditors: xudawu
LastEditTime: 2024-10-15 15:22:19
'''
from fastapi.templating import Jinja2Templates

# 定义模板目录

# 登录注册页模板
TemplatesJinja2Login = Jinja2Templates(directory="SCAU_JWC_2024_09_20\\app\\login\\frontend\\template")
# 公共页面模板
TemplatesJinja2Public = Jinja2Templates(directory="SCAU_JWC_2024_09_20\\frontend\\template")