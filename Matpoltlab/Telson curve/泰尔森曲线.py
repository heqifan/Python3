# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 09:35:56 2021

@author: 树风
"""
import seaborn as sns
import pandas as pd
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, TheilSenRegressor,RANSACRegressor
path1 = r'C:\Users\树风\Documents\Tencent Files\2051936579\FileRecv\Theil–Sen'
path2 = 'max_water.txt'
path3 = path1 + os.sep + path2
data = pd.read_csv(path3,sep = ',',header = 0,names = ['年份','water_area'],index_col=None)
sns.set_style('ticks')
plt.figure(figsize=(10,5))    #绘制画布，宽度，高度，以英寸为单位
fig = sns.lineplot(x=data['年份'], y=data['water_area'], data=data, color= 'black',marker='s',ms=10 )  #设置折点为三角形
sns.despine(top=True, right=True, left=False, bottom=False, offset=None, trim=False)   #边框的设置
plt.xlim((1986, 2019))
plt.ylim((2000, 4000))
plt.xticks(list(range(1986,2019,2)),rotation=30)            # 刻度线的设置  True为去掉  False为保留
plt.yticks(list(range(2000,4000,500)))        #xticks，.yticks为设置x,y坐标的刻度值
plt.ylabel(None)  #不要x,y轴上的标签
plt.xlabel(None)
estimator = TheilSenRegressor()          #加入 sklearn.linear_model 中的theil-sen 线性模型
x = np.array(data['年份'])            #设置自变量
y = np.array(data['water_area'])      #设置因变量
line_x =np.array([1986, 2018])   #设置自变量的范围
X = x[:, np.newaxis]     #np.newaxis的意思是将行转换为列，因为原来在dataframe中取出一列并转化为数组时，数组是行的，你不要打开看时好像就是列，但是其实是行
estimator.fit(X, y)   #处理自变量和因变量
y_pred = estimator.predict(line_x.reshape(2,1))   #对数据进行预测
plt.plot(line_x, y_pred,color='black',linestyle='--')     #画线
plt.show()

path3 = 'sea_water.txt'
path4 = path1 + os.sep + path3
data = pd.read_csv(path4,sep = ',',header = 0,names = ['年份','water_area'],index_col=None)
sns.set_style('ticks')
plt.figure(figsize=(10,5))    #绘制画布，宽度，高度，以英寸为单位
fig = sns.lineplot(x=data['年份'], y=data['water_area'], data=data, color= 'black',marker='^',ms=10 )
sns.despine(top=True, right=True, left=False, bottom=False, offset=None, trim=False)
plt.xlim((1986, 2019))
plt.ylim((500,2500))
plt.xticks(list(range(1986,2019,2)), rotation=30)            # 刻度线的设置  True为去掉  False为保留
plt.yticks(list(range(500,2500,500)))        #xticks，.yticks为设置x,y坐标的刻度值
plt.ylabel(None)
plt.xlabel(None)
estimator = TheilSenRegressor()
x = np.array(data['年份'])
y = np.array(data['water_area'])
line_x =np.array([1986, 2018])
X = x[:, np.newaxis]
estimator.fit(X, y) 
y_pred = estimator.predict(line_x.reshape(2,1))
plt.plot(line_x, y_pred,color='black',linestyle='--')
plt.show()

path3 = 'year_water.txt'
path4 = path1 + os.sep + path3
data = pd.read_csv(path4,sep = ',',header = 0,names = ['年份','water_area'],index_col=None)
sns.set_style('ticks')
plt.figure(figsize=(10,5))    #绘制画布，宽度，高度，以英寸为单位
fig = sns.lineplot(x=data['年份'], y=data['water_area'], data=data, color= 'black',marker='o',ms=10)
sns.despine(top=True, right=True, left=False, bottom=False, offset=None, trim=False)
plt.xlim((1986, 2019))
plt.ylim((1000,3000))
plt.xticks(list(range(1986,2019,2)), rotation=30)            # 刻度线的设置  True为去掉  False为保留
plt.yticks(list(range(1000,3000,500)))        #xticks，.yticks为设置x,y坐标的刻度值
plt.ylabel("Area(km\u00b2)")
plt.xlabel(None)
estimator = TheilSenRegressor()
x = np.array(data['年份'])
y = np.array(data['water_area'])
line_x =np.array([1986, 2018])
X = x[:, np.newaxis]
estimator.fit(X, y) 
y_pred = estimator.predict(line_x.reshape(2,1))
plt.plot(line_x, y_pred,color='black',linestyle='--')
plt.show()


