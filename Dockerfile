FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

# 設置容器啟動時運行 Jupyter Notebook，並將工作目錄掛載
CMD ["sh", "-c", "tensorboard --logdir=/app/logs --bind_all & jupyter notebook --ip=0.0.0.0 --allow-root --no-browser --NotebookApp.token=''"]


# 開放 Jupyter 和 TensorBoard 使用的端口
EXPOSE 8888 6006
