# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 16:29:05 2021

@author: 树风
"""

1.查看dataframe的数据类型
df.info()

2，查看数据框的前面一些行
df.head()

3， DataFrame的描述分析
#数值型：
df[['col1','col2']].describe()
#类别型：
df['col1'].value_counts()[0:10]
#category型：
df['col1'] = df['col1'].astype('category')
df['col1'].describe()

4.清洗数据（重复值，缺失值，异常值）的处理：
重复值的检测及处理：
# 判断某个字段是否有重复值
len(df.col1.unique())  #将返回值与len(df.col1)进行比较
# 记录重复处理：
df.drop_duplicates(subset=['col1','col2'],keep='first',inplace=False)
# subset为需要去重复的列，keep参数有first（保留第一个），last（保留最后一个），
  false（只要有重复都不保留） inplace为是否在源数据上操作，默认False
  
缺失值的检测及处理

# 判断字段是否有缺失
df.isnull().sum() 或 df.notnull().sum()

# 缺失值处理--删除：
df.dropna(axis=1,how='any',inplace=False)
# axis为1是删除列，为0时删除行  how参数为any（只要有缺失值存在就删除），all（全部为缺失值
  时才删除，默认为any  inplace为是否在源数据上操作，默认为False

# 缺失值处理--替换法
# 替换数值型字段时，常用平均数，中位数，替换类别性字段时，常用众数
df.fillna(value=None,method=None,axis=1,inplace=False,limit=None)
# method参数为ffill（用上一个非缺失值填充），bfill（用下一个非缺失值来填充）

# 缺失值处理--插值法
# 线性插值：
from scipy.interpolate import interplt
x=np.array(df['col1'])
y=np.array(df['col2'])
linearInsValue = interplt(x,y,kind='linear')
linearInsValue([6,7])
# 拉格朗日插值：
from scipy.interpolate import lagrange
x=np.array(df['col1'])
y=np.array(df['col2'])
largeInsValue = lagrange(x,y)
largeInsValue([6,7])
# 样条插值：
from scipy.interpolate import spline
x=np.array(df['col1'])
y=np.array(df['col2'])
splineInsValue = spline(x,y,xnew=np.array([6,7]))
# 线性插值法需要x与y存在线性关系，效果才好，大多数情况下，用拉格朗日法和样条插值法较好

异常值的检测及处理:
 使用3σ原则识别异常值，不过该原则只对正态分布或近似正态分布的数据有效
def outRange(ser1):
    boolInd = (ser1.mean()-3*ser1.std()>ser1)|(ser1.mean()+3*ser1.std()<ser1)
    index = np.arange(ser1.shape[0])[boolInd]
    outRange = ser1.iloc[index]
    return outRange
outlier = outRange(df['col1'])
len(outlier)

# 用箱线图来分析异常值
import matplotlib.pyplot as plt
plt.figure(figsize=(10,7))
p = plt.boxplot(df['col1'].values,notch=True)
outlier = p['fliers'][0].get_ydata()
plt.show()
len(outlier)
