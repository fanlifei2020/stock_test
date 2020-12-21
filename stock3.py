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
"""
2020年8月后创业板开通20%涨幅，算法要改，目前是20%算作2个板来计算最高板，卖法未完善，待改进
"""



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


def calculate_profit(series):
    
    """问题：停牌的股票也会推后算，这怎么算"""
    df = pro.daily(ts_code=series['ts_code'], start_date=series['trade_date']).tail(16).head(15)
    df.sort_values(by='trade_date',ascending=True,inplace=True)
   # print('\n')
   # print('股票：',series['ts_code'])
   
    buy_flag = 0
    buy_price = 0
    sell_price = 0
    for index, row in df.iterrows():
      #  print('日期：', row['trade_date'])
       # print("**************")   
       
        if buy_flag == 0 :  #没买则买入
           # print('尚未买入')
            if row['open']>row['pre_close']*1.093:#一字开盘没买点，不买
              #  print('一字板开盘，无买点，退出')
                return np.nan
            else:
                buy_price = row['open']#非一字开盘竞价入
              #  print('非一字开盘，有买点，买入价格： ',buy_price)
                buy_flag = 1   #已买
        else:  #如果已买
            #几种情况要分别计算1.跌停不卖 2.跌停卖
          #  print('已经买入')
            #-3卖出
            if row['low']<row['open']*(1-0.03):
               
                sell_price = row['open']*(1-0.03)
              #  print('-3卖出,价格：',sell_price)
                break
            #没有-3
            else:
                if (row["pct_chg"]>9.3) |(row["pct_chg"]<-9.3 ):
                    #print('当天涨停或跌停，继续算下一天的卖点')
                    continue
                else:
                    sell_price = row['close']
                   # print('无-3，无涨停，尾盘卖出,价格：',sell_price)
                    break

    rate = (sell_price-buy_price)/buy_price*100 -2
    rate = round(rate,2)
    #print('盈利率：' ,rate)
    return rate

        


# In[3]:


os.getcwd()


# In[4]:


os.chdir("C:\\Users\\Administrator\\stock_test")


# In[5]:


os.getcwd()


# In[ ]:





# In[6]:


df = pd.read_csv("unique_strong_table.csv")


# In[7]:


df.head()


# In[8]:


unique_strong_table = df.iloc[:,1:]


# In[ ]:





# In[ ]:





# In[9]:


unique_strong_table['profits']=unique_strong_table.apply(calculate_profit,axis=1)


# In[10]:


unique_strong_table


# In[11]:


unique_strong_table['profits'].sum()


# In[12]:


unique_strong_table['sum'] = unique_strong_table['profits'].cumsum()


# In[13]:


unique_strong_table.head()


# In[14]:


unique_strong_table.to_csv("unique_result.csv")


# In[15]:


import matplotlib.pyplot as plt


# In[16]:


plt.plot(unique_strong_table['trade_date'],unique_strong_table['sum'])


# In[ ]:





# In[21]:





# In[ ]:





# In[ ]:




