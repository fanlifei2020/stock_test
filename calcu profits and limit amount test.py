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


# In[22]:


def calculate_profit():
    
    """问题：停牌的股票也会推后算，这怎么算"""
    df = pro.daily(ts_code="601010.SH", start_date="20150408").tail(16).head(15)
    df.sort_values(by='trade_date',ascending=True,inplace=True)
   # print('\n')
   # print('股票：',series['ts_code'])
    print(df)
   
    buy_flag = 0
    buy_price = 0
    sell_price = 0
    for index, row in df.iterrows():
        print('日期：', row['trade_date'])
        print("**************")   
       
        if buy_flag == 0 :  #没买则买入
            print('尚未买入')
            if row['open']>row['pre_close']*1.093:#一字开盘没买点，不买
                print('一字板开盘，无买点，退出')
                return np.nan
            else:
                buy_price = row['open']#非一字开盘竞价入
                print('非一字开盘，有买点，买入价格： ',buy_price)
                buy_flag = 1   #已买
        else:  #如果已买
            #几种情况要分别计算1.跌停不卖 2.跌停卖
            print('已经买入')
            #-3卖出
            if row['low']<row['open']*(1-0.03):
               
                sell_price = row['open']*(1-0.03)
                print('-3卖出,价格：',sell_price)
                break
            #没有-3
            else:
                if (row["pct_chg"]>9.3) |(row["pct_chg"]<-9.3 ):
                    print('当天涨停或跌停，继续算下一天的卖点')
                    continue
                else:
                    sell_price = row['close']
                    print('无-3，无涨停，尾盘卖出,价格：',sell_price)
                    break

    rate = (sell_price-buy_price)/buy_price*100 -2
    rate = round(rate,2)
    print('盈利率：' ,rate)
    return rate


def count_limit_amount():
#取得15天日线
    df = pro.daily(ts_code="601200.SH", end_date="20170407").head(15)
    print(df)
    count = 0
    flag = 0
    """for index, row in df.iterrows():
    print row["c1"], row["c2"]"""
    for index, row in df.iterrows():
        #往前回溯到没涨停的，直接结束
        #print('\n')
       # print('日期',row['trade_date'])
        if row['pct_chg']<9.9:
            #print('遇到没涨停，结束')
            break
            
        
        if row['vol']>30000 :
            #print('有量')
             #有量且一字：标记+1    
            if  row['high'] == row['low']:
                flag += 1
                #print('有量且一字，标记+1,flag=',flag)
            else:
                #增加创业板20%涨幅的计算
                #有量非一字：结算前面的涨停数+一字标记数 = 总涨停数
                if row['pct_chg']>19.9:
                    count = count + flag + 2
                    flag = 0 #结算后flag重新计数
                    #print(' count=',count)
                else:
                    count = count + flag + 1 
                    flag = 0 #结算后flag重新计数
                   # print('有量非一字，结算flag且+1,count = ',count)
        #无量涨停：一字标记+1
        else:
            flag += 1 
           # print('无量一字，标记+1,flag=',flag)
   # print(count)
    return count
    #往前回溯第一个放量涨停，计算涨停数
        


# In[23]:


count_limit_amount()


# In[ ]:





# In[ ]:





# In[ ]:




