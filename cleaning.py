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
df_clean = df_clean.dropna(subset=['amount'])
columns_to_fill = ['payment_method','currency','bank_name','category','device_type','kyc_status','user_segment']

for col in columns_to_fill:
    df_clean[col] = df_clean[col].fillna("Unknown")

#df_clean['failure_reason'] = df_clean['failure_reason'].fillna('')
df_clean['referral_code'] = df_clean['referral_code'].fillna('Organic')
#df_clean['cashback_applied'] = pd.to_numeric(df_clean['cashback_applied'],errors = 'coerce')
df_clean['cashback_applied'] = df_clean['cashback_applied'].astype(bool)
df_clean['cashback_aplied'] = df_clean['cashback_applied'].fillna(False)

df_clean['transaction_fee'] = df_clean['transaction_fee'].fillna(0)
df_clean['processing_time_ms'] = df_clean['processing_time_ms'].fillna(df_clean['processing_time_ms'].mean())
df_clean['retry_count'] = df_clean['retry_count'].fillna(0)

df_clean['flag_suspicious'] = df_clean['flag_suspicious'].fillna(0).astype(bool)
df_clean['status'] = df['status'].str .lower()

df_clean.loc[(df_clean['status']=='success') & df_clean['failure_reason'].isna(),'failure_reason'] = 'None'

df_clean.loc[(df_clean['status'] == 'failed') & df_clean['failure_reason'].isna(),'failure_reason'] = 'System Error'

df_clean.loc[(df_clean['status'] == 'pending') & df_clean['failure_reason'].isna(),'failure_reason'] = 'Awaiting Gateway'

df_clean['failure_reason'] = df_clean['failure_reason'].fillna("unknown")

df['currency'] = df['currency'].str.lower()
df.loc[(df['amount'].isna()) & ((df['currency'] == 'inr') | (df['currency'] == 'rs')),'amount'] = 0 

df.dropna(subset = ['amount' , 'currency'] , how = 'all' ,inplace = True)

df.loc[(df['amount'].notna()) & (df['currency'].isna()) , 'currecny'] = 'inr'

df.loc[(df['amount'].notna()) & ((df['currency'] == 'inr') | (df['currency'] == 'rs' )),'currency'] = 'inr'


l1 = list(df_clean.columns)
print(l1)
print(len(l1))
df_clean.info()

print(df_clean[['status','failure_reason']])
#l2 = list(df_clean.dtypes)

#print(l2)
print(df_clean['failure_reason'].value_counts())
print(len(df_clean))

conn.close()