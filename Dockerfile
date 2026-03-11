# 使用官方Python镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /workspace/projects

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    cron \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 创建日志目录
RUN mkdir -p logs

# 设置环境变量
ENV PYTHONPATH=/workspace/projects
ENV COZE_WORKSPACE_PATH=/workspace/projects

# 设置crontab
RUN echo "0 9 * * * cd /workspace/projects && python scripts/daily_notification.py >> /workspace/projects/logs/daily_notification.log 2>&1" | crontab -

# 启动cron
CMD ["cron", "-f"]
