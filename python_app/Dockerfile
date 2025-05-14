# 使用官方 Python 輕量映像檔
FROM python:3.10-slim

# 設定容器內的工作目錄
WORKDIR /app

# 複製當前目錄的檔案進入容器
COPY import_data.py .

# 安裝需要的套件（可由協作者自行補充）
# 這裡列出常見的匯入用套件 pandas + pymysql
RUN pip install --no-cache-dir pandas pymysql sqlalchemy

# 預設啟動程式
CMD ["python", "import_data.py"]