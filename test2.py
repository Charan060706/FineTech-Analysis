import pandas as pd
import sqlite3 as db
#pathe = 'FT_logs.db'
#conn = db.connect(pathe)
df = pd.read_csv('FTT.csv')
#df.to_sql(name="FTT",con = conn,if_exists = "replace",index = False)
print(df.head())
print(df.columns)
print(df['currency'].value_counts())
#conn.commit()
#conn.close()
df['currency'] = df['currency'].str.lower()
df.loc[(df['amount'].isna()) & ((df['currency'] == 'inr') | (df['currency'] == 'rs')),'amount'] = 0 

df.dropna(subset = ['amount' , 'currency'] , how = 'all' ,inplace = True)

df.loc[(df['amount'].notna()) & (df['currency'].isna()) , 'currecny'] = 'inr'

df.loc[(df['amount'].notna()) & ((df['currency'] == 'inr') | (df['currency'] == 'rs' )),'currency'] = 'inr'


print(df['currency'].value_counts())
