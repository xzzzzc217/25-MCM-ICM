#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import matplotlib.pyplot as plt

import numpy as np
import time
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import numpy

np.set_printoptions(suppress=True)
get_ipython().run_line_magic('matplotlib', 'inline')

from sklearn.preprocessing import MinMaxScaler
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False 
import seaborn as sns 
sns.set_palette("husl") #设置所有图的颜色，使用hls色彩空间
import numpy as np
from sklearn import metrics
from sklearn.metrics import mean_squared_error #均方误差
from sklearn.metrics import mean_absolute_error #平方绝对误差

from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.svm import SVR


# In[2]:


# 读取BCHAIN-MKPRU.csv文件
df_BM = pd.read_csv('BCHAIN-MKPRU.csv', encoding='utf-8')
# 读取LBMA-GOLD.csv文件
df_GOLD = pd.read_csv('LBMA-GOLD.csv', encoding='utf-8')

# 通过简单的观察，采用Date字段合并数据，采用merge连接
df = pd.merge(df_BM, df_GOLD, how='outer', on='Date')
# 格式化时间 文件的时间格式是 月/日/年 -> 20xx/月/日
df["Date"] = df["Date"].apply(lambda x: time.strftime('%Y/%m/%d %H:%M:%S', time.strptime(x, '%m/%d/%y')))
# 排序Date字段
df = df.sort_values("Date")
df


# In[3]:


#查看缺失值
#比特币可以每天交易，但黄金仅在开市日交易
df.isnull().sum()


# In[4]:


df.columns=['Date','BCHAIN-MKPRU','GOLD']


# In[5]:


#计算日收益率
df['GOLD_fillna']=df['GOLD'].fillna(method='bfill')


# In[6]:


# 计算每日收益率
stock_data = df[['BCHAIN-MKPRU','GOLD_fillna']].pct_change()
# 打印前5行数据
stock_data.head()


# In[7]:


df['BCHAIN日收益率']=stock_data['BCHAIN-MKPRU']
df['GOLD日收益率']=stock_data['GOLD_fillna']


# In[8]:


df['BCHAIN日收益率'].plot(label='BCHAIN')
df['GOLD日收益率'].plot(label='GOLD')
plt.legend()
plt.show()


# In[9]:


df


# In[10]:


#时序数据滑窗转换用于将时间序列数据转为回归数据，简单地说，就是把一个单序列的数据变为X->Y的回归数据。

#步阶为2代表2个X（步阶多少就有多少个X），一个Y（这个不会变的），

#简单地说，就是用第1，2天的数据预测第3天，用第2，3天的数据预测第4天，以此类推。
def create_dataset(dataset, look_back):

    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back)]
        dataX.append(a)
        dataY.append(dataset[i + look_back])
        dddd=pd.concat([pd.DataFrame(np.array(dataY)),pd.DataFrame(np.array(dataX))],axis=1)
        dddd.columns=['Y']+['shiftX_'+str(i) for i in range(len(dddd.columns)-1)]
    return dddd
data1=create_dataset(df_BM['Value'],look_back=1)
data1


# In[11]:



'''
随机森林回归
'''

from sklearn.metrics import r2_score


def score(y_true, y_pre):
    # MSE
    print("MSE :")
    print(metrics.mean_squared_error(y_true, y_pre)) 
    # RMSE
    print("RMSE :")
    print(np.sqrt(metrics.mean_squared_error(y_true, y_pre))) 
    # MAE
    print("MAE :")
    print(metrics.mean_absolute_error(y_true, y_pre)) 
    # R2
    print("R2 :")
    print(r2_score(y_true,y_pre)) 


# In[12]:


from sklearn.model_selection import train_test_split
X=data1['shiftX_0'].values.reshape(-1, 1)
Y=data1['Y'].values.reshape(-1, 1)

train_X,test_X,train_y,test_y = train_test_split(X,Y,test_size=0.3,random_state=5)


model_rf = RandomForestRegressor()
model_rf.fit(train_X,train_y)

score(test_y, model_rf.predict(test_X))


# In[13]:


plt.plot(test_y,color='blue', label='observed data')
plt.plot(model_rf.predict(test_X), color='red', label='RandomForestRegressor')

plt.legend() # 显示图例
plt.show()


# In[15]:


df_BM['Value']=pd.DataFrame(model_rf.predict(df_BM['Value'].values.reshape(-1, 1)),columns=['Value'])


# In[17]:


data1=create_dataset(df_GOLD['USD (PM)'],look_back=1)
data1.dropna(inplace=True)
data1


# In[18]:


X=data1['shiftX_0'].values.reshape(-1, 1)
Y=data1['Y'].values.reshape(-1, 1)

train_X,test_X,train_y,test_y = train_test_split(X,Y,test_size=0.3,random_state=5)


model_rf = RandomForestRegressor()
model_rf.fit(train_X,train_y)

score(test_y, model_rf.predict(test_X))


# In[19]:


plt.plot(test_y,color='blue', label='observed data')
plt.plot(model_rf.predict(test_X), color='red', label='RandomForestRegressor')

plt.legend() # 显示图例
plt.show()


# In[21]:


df_GOLD['USD (PM)']=pd.DataFrame(model_rf.predict(df_GOLD['USD (PM)'].fillna(method='bfill').values.reshape(-1, 1)),columns=['USD (PM)'])


# In[22]:


# 通过简单的观察，采用Date字段合并数据，采用merge连接
df = pd.merge(df_BM, df_GOLD, how='outer', on='Date')
# 格式化时间 文件的时间格式是 月/日/年 -> 20xx/月/日
df["Date"] = df["Date"].apply(lambda x: time.strftime('%Y/%m/%d %H:%M:%S', time.strptime(x, '%m/%d/%y')))
# 排序Date字段
df = df.sort_values("Date")
df.fillna(method='bfill',inplace=True)
df


# In[23]:



from sko.operators import ranking, selection, crossover, mutation
from sko.GA import GA


# In[24]:


# 黄金持有
z1 = 500
# 比特币持有
z2 = 500
# m1 今日黄金价格
m1 = 1324.2576

# m2 今日比特币价格
m2 = 773.88040
# n1 明日黄金价格
n1 = 1323.3617
# n2 明日比特币价格
n2 = 774.83980


# In[25]:


def model_1_ga(z1,z2,m1,m2,n1,n2):
    demo_func = lambda x: -((n1 / m1) * (z1 + x[0]) + (n2 / m2) * (z2 + x[1]))
    constraint_ueq = [
    lambda x: x[0] + x[1] - (z1 + z2),
    lambda x: (-z1 - z2) - (x[0] + x[1]),
    lambda x: 0.01 - ((n1 / m1) - 1),
    lambda x: 0.02 - ((n2 / m2) - 1)
    ]
    ga = GA(func=demo_func, n_dim=2, size_pop=100, max_iter=500, prob_mut=0.001,
    lb=[-z1, -z2], ub=[z1, z2], precision=[1e-7, 1e-7], constraint_ueq=constraint_ueq)
    ga.register(operator_name='selection', operator=selection.selection_roulette_2)
    ga.register(operator_name='ranking', operator=ranking.ranking).     register(operator_name='crossover', operator=crossover.crossover_2point_bit).     register(operator_name='mutation', operator=mutation.mutation)
    best_x, func = ga.run()

    return -func[0],best_x[0],best_x[1]
model_1_ga(z1,z2,m1,m2,n1,n2)


# In[26]:


get_ipython().run_cell_magic('time', '', "\n\ndef model_2_ga(z1,z2,n1,n2):\n\n    demo_func = lambda x: -(z1 + (n2 / m2) * (z2 + x[0]))\n\n\n    constraint_ueq = [\n        lambda x: x[0] - z2,\n        lambda x: - z2 - x[0],\n        lambda x: 0.02  - ((n2 / m2) - 1)\n    ]\n    ga = GA(func=demo_func, n_dim=1, size_pop=100, max_iter=500, prob_mut=0.001,\n            lb=[-z1], ub=[z1], precision=[1e-7], constraint_ueq=constraint_ueq)\n\n    ga.register(operator_name='selection', operator=selection.selection_roulette_2)\n    ga.register(operator_name='ranking', operator=ranking.ranking). \\\n        register(operator_name='crossover', operator=crossover.crossover_2point_bit). \\\n        register(operator_name='mutation', operator=mutation.mutation)\n    best_x, func = ga.run()\n    return -func[0],best_x[0]\n\nmodel_2_ga(z1,z2,n1,n2)")


# In[28]:


# 读取BCHAIN-MKPRU.csv文件
df_BM = pd.read_csv('BCHAIN-MKPRU.csv', encoding='utf-8')
# 读取LBMA-GOLD.csv文件
df_GOLD = pd.read_csv('LBMA-GOLD.csv', encoding='utf-8')

# 通过简单的观察，采用Date字段合并数据，采用merge连接
newdf = pd.merge(df_BM, df_GOLD, how='outer', on='Date')
# 格式化时间 文件的时间格式是 月/日/年 -> 20xx/月/日
newdf["Date"] = newdf["Date"].apply(lambda x: time.strftime('%Y/%m/%d %H:%M:%S', time.strptime(x, '%m/%d/%y')))
# 排序Date字段
newdf = newdf.sort_values("Date")
newdf

# 通过简单的观察，采用Date字段合并数据，采用merge连接
df___ = pd.merge(df, newdf, how='left', on='Date')

df___


# In[ ]:


# 黄金持有
z1 = 500
# 比特币持有
z2 = 1000-z1
alldata=[]
for i in range(df.shape[0]):
    try:
        if i== df.shape[0]-1:
            break
        # m1 真实的今日黄金价格
        m1=df___['USD (PM)_y'].iloc[i]
        # m2 真实的今日比特币价格
        m2=df___['Value_y'].iloc[i]
        # n1 预测的明日黄金价格
        n1= df___['USD (PM)_x'].iloc[i+1]
        # n2 预测的明日比特币价格
        n2= df___['Value_x'].iloc[i+1]
         # n1 真实的明日黄金价格
        N1= df___['USD (PM)_y'].iloc[i+1]
        # n2 真实的明日比特币价格
        N2= df___['Value_y'].iloc[i+1]
        
        if (np.isnan(m1)==True) or (np.isnan(n1)==True):
            ojb,x_bit=model_2_ga(z1,z2,m2,n2)
            z2=N2 / m2 * (z2 + x_bit)
            alldata.append([df___['Date'].iloc[i],m1,m2,n1,n2,N1,N2,z1,z2,np.nan,x_bit,ojb])
        else:
            ojb,x_hj,x_bit=model_1_ga(z1,z2,m1,m2,n1,n2)
            z1=N1 / m1 * (z1 + x_hj) 
            z2=N2 / m2 * (z2 + x_bit)
            alldata.append([df___['Date'].iloc[i],m1,m2,n1,n2,N1,N2,z1,z2,x_hj,x_bit,ojb])
        if z1==0 or np.isnan(z1)==True :
            z1=0.0001
  
    except:
        print(df___['Date'].iloc[i])
        break


# In[ ]:


columns1=['交易日期','真实的今日黄金价格','真实的今日比特币价格','预测的明日黄金价格','预测的明日比特币价格', '真实的明日黄金价格','真实的明日比特币价格','本日黄金持有额(加上第二日的)','本日比特币持有额(加上第二日的)','本日黄金交易额','本日比特币交易额','当前交易日资产总值']
alldata=pd.DataFrame(alldata,columns=columns1)
alldata


# In[176]:


alldata.to_excel('alldata.xlsx',index=None)


# In[ ]:


#迭代以上流程
x=[]
y=[]
for i in range(1,1001,20):
    x.append(i)
    # 黄金持有
    z1 = i 
    # 比特币持有
    z2 = 1000-z1
    alldata=[]
    for i in range(df.shape[0]):
        try:
            if i== df.shape[0]-1:
                break
            # m1 真实的今日黄金价格
            m1=df___['USD (PM)_y'].iloc[i]
            # m2 真实的今日比特币价格
            m2=df___['Value_y'].iloc[i]
            # n1 预测的明日黄金价格
            n1= df___['USD (PM)_x'].iloc[i+1]
            # n2 预测的明日比特币价格
            n2= df___['Value_x'].iloc[i+1]
             # n1 真实的明日黄金价格
            N1= df___['USD (PM)_y'].iloc[i+1]
            # n2 真实的明日比特币价格
            N2= df___['Value_y'].iloc[i+1]

            if (np.isnan(m1)==True) or (np.isnan(n1)==True):
                ojb,x_bit=model_2_ga(z1,z2,m2,n2)
                z2=N2 / m2 * (z2 + x_bit)

            else:
                ojb,x_hj,x_bit=model_1_ga(z1,z2,m1,m2,n1,n2)
                z1=N1 / m1 * (z1 + x_hj) 
                z2=N2 / m2 * (z2 + x_bit)
            if z1==0 or np.isnan(z1)==True :
                z1=0.0001
        except:
            print(df___['Date'].iloc[i])
            break
        y.append(ojb)


# In[ ]:


x


# In[ ]:




