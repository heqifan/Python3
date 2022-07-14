# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 18:08:07 2021

@author: 树风
"""

import matplotlib.pyplot as plt
from matplotlib.pylab import style
style.use('ggplot')    
plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False  
import pandas as pd
import seaborn as sns
import os
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
path = r'D:\python作业\seaborn\作图数据/'
nameList = os.listdir(path)       
for i in nameList:
    temp = pd.read_excel(path+i)
    plt.figure(figsize=(15,5))
    sns.set_style('ticks')
    temp.set_index(["country"], inplace=True)
    temp = temp.T
    temp = temp.stack().reset_index(level=1, name='承载力').rename(columns={'level_1':'country'})[['承载力','country']]
    temp = temp.reset_index().rename(columns={'index':'年'})
    sns.lineplot(data=temp, x="年", y="承载力", hue="country")  #style="event" 为设置不同的线的类型，hue="country"为设置不同的线的颜色
    sns.despine(top=True, right=True, left=False, bottom=False, offset=None, trim=False)   #边框的设置
    plt.xticks(rotation=30)            # 刻度线的设置  True为去掉  False为保留
    plt.ylabel('承载力')  #不要x,y轴上的标签
    plt.xlabel('年份')
    plt.title('经济承载力')
    #根据x和y画图
    #plt.plot(x,y,label='我是图例')
    #显示图例
    plt.legend()
    #markers=True, dashes=False
    #flights_wide = temp.pivot("year", "country", "value")   #设置为数据透射表，这样也可以做
    #sns.lineplot(data=flights_wide)
    plt.show
    