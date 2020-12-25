#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import tushare as ts
from time import sleep
import os
pro = ts.pro_api('7d1f3465439683e262b5b06a8aaefa886ea48aafe2cda73c130beb97')
#df = pro.trade_cal(exchange='', start_date='20180101', end_date='20181231')
#data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
#df = pro.daily(ts_code='000001.SZ,600000.SH', start_date='20180701', end_date='20180718')
#df = pro.daily(trade_date='20180810')

#2020年8月后创业板开通20%涨幅，算法要改，目前是20%算作2个板来计算最高板，卖法未完善，待改进




#不显示科学计数法
np.set_printoptions(suppress=True)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

trade_day = pro.trade_cal(exchange='', start_date='20150101', end_date='20201231')
trade_day = trade_day.loc[trade_day['is_open']==1,:]
trade_days = list(trade_day['cal_date'])

def get_limit(day):
    df = pro.daily(trade_date=day)
    df = df.loc[df['pct_chg']>9.9,:]
    return df


# In[2]:


trade_days.index('20200824')


# In[3]:


def get_limit_amount_for_twenty_percent(series):
#取得15天日线
    df = pro.daily(ts_code=series['ts_code'], end_date=series['trade_date']).head(15)
    #print(df)
    #print("\n")
    count = 0
    flag = 0
    #print('ts_code:',row['ts_code'])
 
    for index, row in df.iterrows():
        #print('ts_code:',row['ts_code'])
        #print("date:",row['trade_date'])
        if row['pct_chg']<9.93 or row['close']!=row['high']:
            #print('未涨停，count=',count)
            return count
        else:
            if row['vol']>30000 and (row['close']==row['high']):
                if row['pct_chg']>19:
                    count = count + 2 + flag
                    #print('有量，且涨停20个点,count=count+2+flag=',count)
                else:
                    count = count + 1 + flag
                    #print('有量，且涨停10个点,count=count+1+flag=',count)

            elif row['vol']<3000 and row['close']==row['high']:
                if row['pct_chg']<19:
                    flag = flag + 1
                    #print('无量涨停，一字板，10个点，flag=flag+1=',flag)
                else:
                    flag = flag + 2
                    #print('无量涨停，一字板，20个点，flag=flag+2=',flag)
            
    #print("count=",count)
    return count
   
    


# In[4]:


strong_table_for20 = pd.DataFrame(columns=['ts_code','name','limit_amount','trade_date','open','high','low',                                     'close','pre_close','change','pct_chg','vol','amount','industry'])
top_table_for20 = pd.DataFrame(columns=['ts_code','name','limit_amount','trade_date','open','high','low',                                     'close','pre_close','change','pct_chg','vol','amount','industry'])


# In[5]:


for day in trade_days[1430:1454]:
    print(day,end=',')
    df = get_limit(day)
    df['limit_amount'] = df.apply(get_limit_amount_for_twenty_percent,axis=1)
    df = df.loc[df['limit_amount']>1,:]

    #sleep(5)
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,name,industry')
    df2 = pd.merge(df,data,on='ts_code',how='inner')
    df2 = df2[['ts_code','name','limit_amount','trade_date','open','high','low','close','pre_close','change',               'pct_chg','vol','amount','industry']]

    df3 = df2.copy()
    df3 = df3.loc[df3['limit_amount']==df3['limit_amount'].max(),:]
   # print(df2)
   # print("___________")
    strong_table_for20 = strong_table_for20.append(df2)
    top_table_for20 = top_table_for20.append(df3)
    #count += 1
   # print(strong_table)
    #print("***********")
    
    


# In[6]:


os.chdir("C:\\Users\\Administrator\\stock_test\\zhucezhi")

strong_table_for20['vol'] = strong_table_for20['vol'].astype(int)
top_table_for20['vol'] = top_table_for20['vol'].astype(int)
unique_table_for20 = top_table_for20.drop_duplicates(subset='trade_date',keep=False)

strong_table_for20 = strong_table_for20.reset_index(drop=True)
if os.path.exists('strong_table_for20.csv'):
    strong_table_for20.to_csv('strong_table_for20.csv',encoding='utf_8_sig',mode='a',header=False) 
else:
    strong_table_for20.to_csv('strong_table_for20.csv',encoding='utf_8_sig',mode='a',header=True) 
#strong_table_for20.to_excel(year + 'strong_table_for20.xlsx',encoding='utf_8_sig') 

top_table_for20 = top_table_for20.reset_index(drop=True)
if os.path.exists('top_table_for20.csv'):
    top_table_for20.to_csv('top_table_for20.csv',encoding='utf_8_sig',mode='a',header=False) 
else:
    top_table_for20.to_csv('top_table_for20.csv',encoding='utf_8_sig',mode='a',header=True) 
#top_table_for20.to_excel(year + 'top_table_for20.xlsx',encoding='utf_8_sig') 

unique_table_for20 = unique_table_for20.reset_index(drop=True)
if os.path.exists('unique_table_for20.csv'):
    unique_table_for20.to_csv('unique_table_for20.csv',encoding='utf_8_sig',mode='a',header=False) 
else:
    unique_table_for20.to_csv('unique_table_for20.csv',encoding='utf_8_sig',mode='a',header=True) 
#unique_table_for20.to_excel(year + 'unique_table_for20.xlsx',encoding='utf_8_sig')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




