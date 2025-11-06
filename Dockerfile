FROM python:3.10-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 创建必要的目录
RUN mkdir -p logs templates static services

# 暴露端口
EXPOSE 5000

# 时区配置
ENV TZ=Asia/Shanghai

# 启动应用
CMD ["python", "run.py"]
