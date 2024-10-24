'''
Author: xudawu
Date: 2024-10-15 08:52:34
LastEditors: xudawu
LastEditTime: 2024-10-24 17:50:37
'''
# 引入文件目录设置
import sys
import os
# 添加项目文件根目录到系统路径
module_path = os.path.abspath('SCAU_JWC_2024_09_20')
sys.path.append(module_path)

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from route import route_authorization, route_main

# 引入业务路由模块
from app.score_visualization.route import route_score


# 创建 FastAPI 应用
app = FastAPI()


# 获得文件夹路径
BASE_PATH = Path(__file__).resolve().parent

# 挂载静态文件路径,公共静态文件路径
app.mount("/public_static_path", StaticFiles(directory= module_path +"\\frontend\\static"))

# 业务模块静态文件路径
app.mount("/login_static_path", StaticFiles(directory=module_path +"\\app\\login\\frontend\\static"))
app.mount("/score_visualization_static_path", StaticFiles(directory=module_path +"\\app\\score_visualization\\frontend\\static"))

# 包含路由模块
app.include_router(route_authorization.router)
app.include_router(route_main.router)

# 成绩可视化模块
app.include_router(route_score.router)

# 主函数启动应用程序
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="app.main:app", host="0.0.0.0", port=8000, reload=True)
    # uvicorn.run(app, host="0.0.0.0", port=8000)