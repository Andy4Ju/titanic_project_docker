# TODO: 顯示 Titanic 資料
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "尚未實作 show_data.py，請開發者補上顯示邏輯"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)