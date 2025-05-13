import os
import pymysql
from flask import Flask, render_template_string


# 資料庫連線設定
DB_CONFIG = {
    
    "host": os.environ.get("MYSQL_HOST", "localhost"),
    "port": int(os.environ.get("MYSQL_PORT", 3306)),
    "user": os.environ.get("MYSQL_USER", "root"),
    "password": os.environ.get("MYSQL_PASSWORD", "P@ssw0rd"),
    "database": os.environ.get("MYSQL_DATABASE", "my_titanic")

    # "host": "localhost",
    # "port": 3306,
    # "user": "root",
    # "password": "P@ssw0rd",
    # "database": "my_titanic"
}

app = Flask(__name__)

@app.route('/')
def index():
    try:
        # 連接 MySQL
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 查詢欄位名稱
        cursor.execute("DESCRIBE full_passengers")
        columns = [col[0] for col in cursor.fetchall()]

        # 查詢所有資料
        cursor.execute("SELECT * FROM full_passengers")
        rows = cursor.fetchall()

        conn.close()
    except Exception as e:
        columns, rows = []
        print("資料庫錯誤：", e)

    # HTML 模板，使用 Jinja2 語法做迴圈渲染
    html = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Titanic Viewer</title>
    <!-- Bootstrap + DataTables CDN -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdn.datatables.net/1.13.6/css/dataTables.bootstrap5.min.css">
</head>

<body class="p-4">
    <h2 class="mb-3">Titanic Passenger Explorer</h2>

    <!-- Quick sex filter -->
    <div class="mb-2">
        <select id="sexFilter" class="form-select w-auto d-inline">
            <option value="">All Genders</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
        </select>
    </div>

    <table id="titanic" class="table table-striped table-hover" style="width:100%">
        <thead>
            <tr>
                <th>ID</th>
                <th>Survived</th>
                <th>Class</th>
                <th>Name</th>
                <th>Sex</th>
                <th>Age</th>
                <th>SibSp</th>
                <th>Parch</th>
                <th>Ticket</th>
                <th>Fare</th>
                <th>Cabin</th>
                <th>Embarked</th>
            </tr>
        </thead>
    </table>

    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.6/js/dataTables.bootstrap5.min.js"></script>
    <script>
        const table = $('#titanic').DataTable({
            ajax: { url: '/api/data', dataSrc: 'data' },
            columns: [
                { data: 'PassengerId' }, { data: 'Survived' }, { data: 'Pclass' },
                { data: 'Name' }, { data: 'Sex' }, { data: 'Age' }, { data: 'SibSp' },
                { data: 'Parch' }, { data: 'Ticket' }, { data: 'Fare' },
                { data: 'Cabin' }, { data: 'Embarked' }
            ],
            pageLength: 25,
            order: [[0, 'asc']]
        });

        $('#sexFilter').on('change', function () {
            table.ajax.url('/api/data?sex=' + this.value).load();
        });
    </script>
</body>

</html>


    
"""
# <!doctype html>
# <html>
# <head>
#     <title>Titanic Data</title>
#     <style>
#         table { border-collapse: collapse; width: 100%%; font-size: 14px; }
#         th, td { border: 1px solid black; padding: 4px; text-align: left; }
#         th { background-color: #f2f2f2; }
#     </style>
# </head>
# <body>
#     <h2>Andy Testing for Titanic Data</h2>
#     <table>
#         <tr>
#             {% for col in columns %}
#             <th>{{ col }}</th>
#             {% endfor %}
#         </tr>
#         {% for row in rows %}
#         <tr>
#             {% for item in row %}
#             <td>{{ item }}</td>
#             {% endfor %}
#         </tr>
#         {% endfor %}
#     </table>
# </body>
# </html>

    return render_template_string(html, rows=rows, columns=columns) # , rows=rows, columns=columns

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)