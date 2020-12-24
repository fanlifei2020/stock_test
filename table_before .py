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


# In[ ]:





# In[2]:


def count_limit_amount(series):
#取得15天日线
    df = pro.daily(ts_code=series['ts_code'], end_date=series['trade_date']).head(15)
    
    count = 0
    flag = 0
    """for index, row in df.iterrows():
    print row["c1"], row["c2"]"""
    for index, row in df.iterrows():
        #往前回溯到没涨停的，直接结束
        if row['pct_chg']<9.9:
            break
            
        
        if row['vol']>30000 :
             #有量且一字：标记+1    
            if  row['high'] == row['low']:
                flag += 1
            else:
                #增加创业板20%涨幅的计算
                #有量非一字：结算前面的涨停数+一字标记数 = 总涨停数
                if row['pct_chg']>19.9:
                    count = count + flag + 2
                    flag = 0 #结算后flag重新计数
                else:
                    count = count + flag + 1 
                    flag = 0 #结算后flag重新计数
        #无量涨停：一字标记+1
        else:
            flag += 1 
            
    return count
    #往前回溯第一个放量涨停，计算涨停数


# In[3]:


strong_table = pd.DataFrame(columns=['ts_code','name','limit_amount','trade_date','open','high','low',                                     'close','pre_close','change','pct_chg','vol','amount','industry'])
top_strong_table = pd.DataFrame(columns=['ts_code','name','limit_amount','trade_date','open','high','low',                                     'close','pre_close','change','pct_chg','vol','amount','industry'])


# In[4]:


year = '2015'


# In[5]:


if not os.path.exists('./stock_test'):
    os.mkdir('./stock_test')


# In[6]:


os.chdir('./stock_test')


# In[7]:


count = 0 


# In[8]:


for day in trade_days[1400:1430]:
    
    print(day,end=',')
    df = get_limit(day)
    df['limit_amount'] = df.apply(count_limit_amount,axis=1)
    df = df.loc[df['limit_amount']>1,:]

    #sleep(5)
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,name,industry')
    df2 = pd.merge(df,data,on='ts_code',how='inner')
    df2 = df2[['ts_code','name','limit_amount','trade_date','open','high','low','close','pre_close','change',               'pct_chg','vol','amount','industry']]

    df3 = df2.copy()
    df3 = df3.loc[df3['limit_amount']==df3['limit_amount'].max(),:]
   # print(df2)
   # print("___________")
    strong_table = strong_table.append(df2)
    top_strong_table = top_strong_table.append(df3)
    count += 1
   # print(strong_table)
    #print("***********")
    """strong_table['vol'] = strong_table['vol'].astype(int)
    top_strong_table['vol'] = top_strong_table['vol'].astype(int)
    unique_strong_table = top_strong_table.drop_duplicates(subset='trade_date',keep=False)"""
    


# In[9]:


strong_table['vol'] = strong_table['vol'].astype(int)
top_strong_table['vol'] = top_strong_table['vol'].astype(int)
unique_strong_table = top_strong_table.drop_duplicates(subset='trade_date',keep=False)

strong_table = strong_table.reset_index(drop=True)
if os.path.exists('strong_table.csv'):
    strong_table.to_csv('strong_table.csv',encoding='utf_8_sig',mode='a',header=False) 
else:
    strong_table.to_csv('strong_table.csv',encoding='utf_8_sig',mode='a',header=True) 
#strong_table.to_excel(year + 'strong_table.xlsx',encoding='utf_8_sig') 

top_strong_table = top_strong_table.reset_index(drop=True)
if os.path.exists('top_strong_table.csv'):
    top_strong_table.to_csv('top_strong_table.csv',encoding='utf_8_sig',mode='a',header=False) 
else:
    top_strong_table.to_csv('top_strong_table.csv',encoding='utf_8_sig',mode='a',header=True) 
#top_strong_table.to_excel(year + 'top_strong_table.xlsx',encoding='utf_8_sig') 

unique_strong_table = unique_strong_table.reset_index(drop=True)
if os.path.exists('unique_strong_table.csv'):
    unique_strong_table.to_csv('unique_strong_table.csv',encoding='utf_8_sig',mode='a',header=False) 
else:
    unique_strong_table.to_csv('unique_strong_table.csv',encoding='utf_8_sig',mode='a',header=True) 
#unique_strong_table.to_excel(year + 'unique_strong_table.xlsx',encoding='utf_8_sig')


# In[10]:


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
                if (row["pct_chg"]>9) |(row["pct_chg"]<-9 ):
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

        


# In[11]:


unique_strong_table['profits']=unique_strong_table.apply(calculate_profit,axis=1)


# In[12]:


unique_strong_table


# In[13]:


unique_strong_table['profits'].sum()


# In[ ]:





# In[ ]:




