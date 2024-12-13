FROM minlag/mermaid-cli

# 设置工作目录
WORKDIR /app

# 安装 Python 和 Flask
RUN apk add --no-cache python3 py3-pip
RUN pip3 install flask

# 复制项目文件
COPY main.py /app/
COPY puppeteer-config.json /app/
COPY config.json /app/

# 创建数据目录
RUN mkdir -p /app/data

# 暴露端口
EXPOSE 5002

# 启动服务
CMD ["python3", "main.py"]
