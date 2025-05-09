# 使用官方 Python 輕量映像檔
FROM python:3.10-slim

# 設定容器工作目錄
WORKDIR /app

# 複製應用程式進入容器
COPY . .

# 安裝基本 Web 顯示與資料查詢所需套件
RUN pip install --no-cache-dir -r requirements.txt

# 開放 Flask 對外連線 port
EXPOSE 5000

# 預設執行 Web 應用程式
CMD ["python", "show_data.py"]
