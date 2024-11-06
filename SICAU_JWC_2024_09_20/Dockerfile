# 使用官方的 Python镜像作为基础镜像
FROM python:3.12.6

# 设置工作目录
WORKDIR /scau_jwc

# 安装 unixODBC 和sqlserver驱动, 并清理缓存
RUN apt-get update && \
    apt-get install -y curl && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 mssql-tools unixodbc-dev && \
    rm -rf /var/lib/apt/lists/*

# 安装 unixODBC 和 PostgreSQL ODBC 驱动
# RUN apt-get update && \
#     apt-get install -y unixodbc unixodbc-dev odbc-postgresql && \
#     rm -rf /var/lib/apt/lists/*


# 将 requirements.txt 文件复制到工作目录
COPY requirements.txt .

# 安装项目依赖
# 在容器中执行 pip install 命令，安装 requirements.txt 中列出的所有依赖包。
# --no-cache-dir 参数用于避免在安装时缓存包，从而减小镜像体积。
# -i https://pypi.tuna.tsinghua.edu.cn/simple使用清华大学的镜像源
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 将项目代码复制到工作目录
# 第一次参数是相对于Dockerfile的路径，第二次参数是相对于WORKDIR的路径
COPY . /scau_jwc

# 创建数据存储目录
RUN mkdir -p /scau_jwc/data

# 声明容器在运行时将使用的端口
EXPOSE 8000

# 启动 FastAPI 应用，使用 uvicorn 作为 ASGI 服务器
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]