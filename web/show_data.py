from flask import Flask, render_template, jsonify, request
import pandas as pd
import os
import pymysql
import time

app = Flask(__name__)

# 資料庫連線設定
DB_CONFIG = {
    "host": os.environ.get("MYSQL_HOST", "mysql"),
    "port": int(os.environ.get("MYSQL_PORT", 3306)),
    "user": os.environ.get("MYSQL_USER", "root"),
    "password": os.environ.get("MYSQL_PASSWORD", "root"),
    "database": os.environ.get("MYSQL_DATABASE", "titanic_db")
}

# 預設空資料
df = pd.DataFrame()

# 加入 retry 機制：等待 MySQL 啟動完成
MAX_RETRY = 10
for i in range(MAX_RETRY):
    try:
        print(f"第 {i+1} 次嘗試連線到資料庫...")
        conn = pymysql.connect(**DB_CONFIG)
        df = pd.read_sql("SELECT * FROM passengers", conn)
        conn.close()
        print(f"成功載入資料，共 {len(df)} 筆")
        break
    except Exception as e:
        print("資料庫連線失敗：", e)
        time.sleep(3)
else:
    print("無法連接資料庫，df 將保持空")

# 首頁載入 HTML 頁面
@app.route('/')
def home():
    return render_template('index23.html')  # 這個模板請放在 /templates/index23.html

# AJAX 用 API，支援篩選
@app.route('/api/data')
def get_data():
    sex = request.args.get('sex', '')
    pclass = request.args.get('pclass', '')
    print(f"🔍 篩選條件: sex={sex}, pclass={pclass}")

    filtered_df = df.copy()

    if sex:
        filtered_df = filtered_df[filtered_df['Sex'].str.lower() == sex.lower()]

    if pclass:
        filtered_df = filtered_df[filtered_df['Pclass'].astype(str) == pclass]

    filtered_df = filtered_df.fillna("")
    return jsonify({'data': filtered_df.to_dict(orient='records')})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)