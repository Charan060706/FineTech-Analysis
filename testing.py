import pandas as pd
import sqlite3 as db
pathe = 'FT_logs.db'
conn = db.connect(pathe)
df = pd.read_csv('FTT.csv')
df.to_sql(name="FTT",con = conn,if_exists = "replace",index = False)
print(df.head())
print(df.columns)
conn.commit()
conn.close()
