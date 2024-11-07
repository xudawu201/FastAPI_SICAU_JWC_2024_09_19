# 基础镜像（选择适合你需要的镜像）
FROM python:3.12.6

# 复制本地的 .deb 文件到 Docker 容器中的 /tmp/ 目录
COPY ./mysql-connector-odbc_9.1.0-1debian12_amd64.deb /tmp/

# 安装 MySQL ODBC 驱动程序并自动修复依赖
RUN dpkg -i /tmp/mysql-connector-odbc_9.1.0-1debian12_amd64.deb || apt-get install -y -f \
    && rm /tmp/mysql-connector-odbc_9.1.0-1debian12_amd64.deb

# 清理并安装相关依赖项
RUN apt-get update \
    && apt-get install -y \
    unixodbc \
    && apt-get clean