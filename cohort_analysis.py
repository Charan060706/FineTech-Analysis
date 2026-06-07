import pandas as pd
import sqlite3 as sql
from matplotlib import pyplot as plt

path = 'FT_logs.db'

conn = sql.connect(path)

#df1 = pd.read_sql_query("Select * from FTT_clean",conn) 
#one way to read from sql to data frame
df1 = pd.read_parquet('FTT_clean.parquet')


#print(df1['signup_date'].info())
#print(df1.info())
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
#print(len(df1))

#x = list(df1['month_index'] >0)
#print(len(x))

#letss goo some deep 
print(df1['cohort_month'].min())
print(df1['cohort_month'].max())

cohort_counts = df1.groupby(['cohort_month','month_index'])['user_id'].nunique().reset_index()

retention_matrix = cohort_counts.pivot(index = 'cohort_month',columns = 'month_index' ,values='user_id')

cohort_sizes = retention_matrix.iloc[:,0]

retention_pct = retention_matrix.divide(cohort_sizes,axis = 0).round(4)*100

print(retention_pct.head())
print(cohort_counts)
#print(df1['user_id'].nunique())

#print(df1['device_type'].value_counts())
avg_retention = retention_pct.mean(axis = 0)
print(avg_retention)
plt.figure(figsize=(10,10))
avg_retention.plot(kind = 'line',marker = 's' ,color = '#00ff88')
plt.title("Average User Retention Curve")
plt.xlabel("Months Since Signed-up")
plt.ylabel("Average Retention Rate (%)")
plt.grid(True,linestyle = '--',alpha = 0.6)
plt.savefig('avg_user_ret_curve.png')
plt.close()

def get_ret_by_segment(df,segment_col):
    segments = df[segment_col].unique()
    segment_retention = {}

    for val in segments:
        if pd.isna(val) or val == 'unknown' : continue

        subset = df[df[segment_col] == val]
        counts = subset.groupby(['cohort_month','month_index'])['user_id'].nunique().reset_index()
        pivot = counts.pivot(index = 'cohort_month',columns = 'month_index',values = 'user_id')

        avg_ret = pivot.divide(pivot.iloc[:,0],axis = 0).mean(axis = 0) * 100
        segment_retention[val] = avg_ret

    return pd.DataFrame(segment_retention)

payment_Segmentation  = get_ret_by_segment(df1,'payment_method')
payment_Segmentation.plot(figsize = (12,6),marker = 'o',title = 'Retention curve by payment method',grid = True)
plt.savefig('retention_curve_payment_method')

device_segmention = get_ret_by_segment(df1,'device_type')

device_segmention.plot(figsize = (12,8),marker = 's',title = 'Retention curve by device type',grid = True)
plt.savefig('retention_curve_device_type')

plt.show()