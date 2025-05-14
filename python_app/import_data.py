import time
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# 設定連線參數
DB_URI = 'mysql+pymysql://root:root@mysql:3306/titanic_db'

# 最多重試次數
MAX_RETRIES = 10
WAIT_TIME = 3  # 秒

# 重試機制
for attempt in range(MAX_RETRIES):
    try:
        engine = create_engine(DB_URI)
        with engine.connect() as conn:
            print("成功連上 MySQL")
            break
    except OperationalError as e:
        print(f"第 {attempt+1} 次連線失敗，3 秒後重試... ({e})")
        time.sleep(WAIT_TIME)
else:
    print("無法連接 MySQL，請確認服務已啟動")
    exit(1)

# 繼續執行匯入
data = pd.read_csv('./csv/titanic.csv')
data.to_sql('passengers', engine, chunksize=100000, index=None)
print("資料匯入成功！")