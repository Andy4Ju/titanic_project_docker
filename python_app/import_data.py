import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:root@mysql/titanic_db')
data = pd.read_csv('./csv/titanic.csv')
data.to_sql('passengers',engine,chunksize=100000,index=None)
print('存入成功!')
