import os
import pymysql
from flask import Flask, render_template_string


# 資料庫連線設定
DB_CONFIG = {
    #"host": "localhost",
    # "port": 3306,
    # "user": "root",
    # "password": "P@ssw0rd",
    # "database": "titanic_db"

    "host": os.environ.get("MYSQL_HOST", "localhost"),
    "port": int(os.environ.get("MYSQL_PORT", 3306)),
    "user": os.environ.get("MYSQL_USER", "root"),
    "password": os.environ.get("MYSQL_PASSWORD", ""),
    "database": os.environ.get("MYSQL_DATABASE", "titanic_db")
}

app = Flask(__name__)

@app.route('/')
def index():
    try:
        # 連接 MySQL
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 查詢欄位名稱
        cursor.execute("DESCRIBE passengers")
        columns = [col[0] for col in cursor.fetchall()]

        # 查詢所有資料
        cursor.execute("SELECT * FROM passengers")
        rows = cursor.fetchall()

        conn.close()
    except Exception as e:
        columns, rows = []
        print("資料庫錯誤：", e)

    # HTML 模板，使用 Jinja2 語法做迴圈渲染
    html = """
<!doctype html>
<html>
<head>
    <title>Titanic Data</title>
    <style>
        table { border-collapse: collapse; width: 100%%; font-size: 14px; }
        th, td { border: 1px solid black; padding: 4px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h2>Andy Testing for Titanic Data</h2>
    <table>
        <tr>
            {% for col in columns %}
            <th>{{ col }}</th>
            {% endfor %}
        </tr>
        {% for row in rows %}
        <tr>
            {% for item in row %}
            <td>{{ item }}</td>
            {% endfor %}
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

    return render_template_string(html, rows=rows, columns=columns)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)