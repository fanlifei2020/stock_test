#!/usr/bin/env python
# coding: utf-8

# In[10]:
#test
#jhhhhdfef

#%matplotlib inline
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import tushare as ts
from time import sleep
import os
#pro = ts.pro_api('7d1f3465439683e262b5b06a8aaefa886ea48aafe2cda73c130beb97')
#df = pro.trade_cal(exchange='', start_date='20180101', end_date='20181231')
#data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
#df = pro.daily(ts_code='000001.SZ,600000.SH', start_date='20180701', end_date='20180718')
#df = pro.daily(trade_date='20180810')
"""
2020年8月后创业板开通20%涨幅，算法要改，目前是20%算作2个板来计算最高板，卖法未完善，待改进
"""


# In[11]:


df = pd.read_csv("D:\\Program Files\\python38\\reposity\\unique_result.csv")


# In[12]:


df = df.iloc[:,1:]


# In[81]:


df['limit_amount'].astype(np.int8)


# In[82]:


df_drop2 = df[df['limit_amount']>2]


# In[84]:


df_drop2['sum'] = df_drop2['profits'].cumsum()


# In[85]:


df_drop2


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[78]:


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=(30,30),dpi=100)
date = df['trade_date'].tolist()
date = [str(i)[:-2] for i in date]
result = df['sum'].tolist()
plt.plot(df.index.values,result)
plt.xticks(np.arange(0,849,30),date[::30],rotation=45,size=16)
plt.yticks(np.arange(-200,200,10),size=16)
fig = plt.gcf()
fig.set_size_inches(60,20)
plt.grid(ls='--',c='darkblue')
plt.savefig('result.jpg')
plt.show()


# In[ ]:





# In[36]:


x = np.linspace(0,10,100)
y = np.sin(x)


# In[37]:


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.plot(x,y,ls='-',lw=2,c='g',label='sinddddd图')
plt.legend(loc='center')
plt.show()


# In[38]:


x = np.arange(0,1.1,0.1)


# In[39]:


y = x*x


# In[51]:


plt.figure(figsize=(10,10),dpi=100)


# In[55]:


plt.xlabel('x')
plt.ylabel('y')
plt.title('画个图')
plt.plot(x,y,label='y=x^2')
plt.legend(loc='best')
fig = plt.gcf()
fig.set_size_inches(20,10)
#plt.xticks(np.arange(len(x),list("abcdefghij")))
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




