import pandas as pd
import sqlite3 as sql
path = 'FT_logs.db'

conn = sql.connect(path)

#df1 = pd.read_sql_query("Select * from FTT_clean",conn) 
#one way to read from sql to data frame
df1 = pd.read_parquet('FTT_clean.parquet')


print(df1['signup_date'].info())
print(df1.info())
df1['cohort_month'] = df1['signup_date'].dt.to_period('M').dt.to_timestamp()
df1['txn_month'] = df1['txn_timestamp'].dt.to_period('M').dt.to_timestamp()
#print(df1['txn_timestamp'].head())
#print(df1['cohort_month'].head())

def get_year_month(df,column):
    return df[column].dt.year,df[column].dt.month

s_yr,s_mon = get_year_month(df1,'signup_date')
t_yr,t_mon = get_year_month(df1,'txn_timestamp')

df1['month_index'] = (t_yr - s_yr) * 12 + (t_mon - s_mon)

df1[df1['month_index'] >=0]

print(df1['month_index'].value_counts())
print(len(df1))

#x = list(df1['month_index'] >0)
#print(len(x))
