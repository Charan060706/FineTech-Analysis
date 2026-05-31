import numpy as np
import pandas as pd
import sqlite3
conn = sqlite3.connect('FT_logs.db')
df = pd.read_sql_query("Select * from FTT",conn)

#print(df.head())
#list of columns before dropping 
l = list(df.columns)
print(len(l))
print(l)
to_drop = [
    'txn_date', 'created_at_epoch', 
    'request_id', 'server_node', 'gateway_code', 
    'raw_response_code', 'trace_id', 'batch_id', 
    'idempotency_key', 'session_token', 'app_version',
    'ip_address', 'device_id'
]
df_clean = df.drop(columns = to_drop)
if 'city_x' in df_clean.columns and 'city_y' in df_clean.columns:
    df_clean['city'] = df_clean['city_x'].fillna(df_clean['city_y'])
    df_clean.drop(['city_x','city_y'],axis = 1,inplace = True)

df_clean['txn_timestamp'] = pd.to_datetime(df_clean['txn_timestamp'])
df_clean['amount'] = pd.to_numeric(df_clean['amount'],errors = 'coerce')
l1 = list(df_clean.columns)
print(l1)
print(len(l1))
df_clean.info()
#l2 = list(df_clean.dtypes)

#print(l2)

conn.close()