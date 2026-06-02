from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
df1 = pd.read_parquet('FTT_clean.parquet')
device_counts = df1['device_type'].value_counts()
#print(df1.info())

#df1['device_type'].value_counts().plot.pie(autopct='%1.1f%%',startangle = 90)


device_counts.plot.pie(autopct='%1.1f%%',startangle = 90)
plt.title('Distribution of device types-PIE')
plt.ylabel('')
plt.tight_layout()
plt.savefig('Distr_device_types_pie.png')
plt.close()


sns.set_theme(style="whitegrid")


device_counts.plot(kind='barh',color = sns.color_palette("Blues_r",len(device_counts)))

plt.ylabel('Device Type',fontsize=12)
plt.xlabel('No of users',fontsize = 12)
plt.title('Distribution of device types',fontsize = 14,fontweight = 'bold',pad = 15)
plt.tight_layout()
plt.savefig('Distr_device_types_barh.png')
