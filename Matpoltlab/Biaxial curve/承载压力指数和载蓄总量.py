# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 19:52:57 2021

@author: 树风
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import style
from matplotlib.font_manager import FontProperties
font = FontProperties(fname="SimHei.ttf", size=30)  # 设置字体
style.use('ggplot')    
plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False  
import pandas as pd
import seaborn as sns
inpath= r'D:\python作业\双轴折线\国庆作图/'
sheeps = pd.read_excel(inpath + '三江源载畜压力.xlsx')
sns.set_style('ticks')
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
fig, ax = plt.subplots(figsize=(10, 7))
styles = dict(ha="center", va="center", color="black", size=15)
ax.annotate(s="Before the livestock\nreduction", xy=(1994, 500), **styles)
ax.annotate(s="After the livestock\nreduction", xy=(2009, 500), **styles)
plt.xlim((1988, 2013))
plt.ylim((0,4000))
plt.xticks(list(range(1988,2013,1)),rotation=90)            # 刻度线的设置  True为去掉  False为保留
plt.yticks(list(range(0,4000,500)))        #xticks，.yticks为设置x,y坐标的刻度值
font2 = {'family' : 'Times New Roman','weight' : 'normal','size' : 20}
sns.set(font="SimHei")
sns.despine(top=True, right=True, left=False, bottom=False, offset=None, trim=False)   #边框的设置
fig1 = sns.lineplot(x=sheeps['年份'], y=sheeps['理论载畜总量'],data = sheeps,color= 'black',marker='d',ms=10,label=u"理论载蓄总量 Proper carrying capacity")
fig2 = sns.lineplot(x=sheeps['年份'], y=sheeps['现实载畜总量'],data = sheeps,color= 'black',marker='s',ms=10,label=u"现实载蓄总量 Standing carrying capacity")   
#the trendline    
z = np.polyfit(sheeps['年份'], sheeps['理论载畜总量'], 1)
p = np.poly1d(z)
plt.plot(sheeps['年份'],p(sheeps['年份']),"black")
z = np.polyfit(sheeps['年份'], sheeps['现实载畜总量'], 1)
p = np.poly1d(z)
plt.plot(sheeps['年份'],p(sheeps['年份']),"black")
plt.legend(loc='upper center',ncol = 1,frameon=False,fontsize=18,handletextpad=0.1)
plt.xlabel('Year',font2)
plt.ylabel(u'Carrying capacity \n(×10\u2074 Sheep units)',font2)
# list_y = list(range(500,3100,100))
# list_x = [2005]*26
# c={"x" : list_x,"y" : list_y}#将列表a，b转换成字典
# dat=pd.DataFrame(c)#将字典转换成为数据框
#dat = pd.DataFrame([list_x, list_y], columns = ["x", "y"])
#fig2 = sns.lineplot(x=list_x, y=list_y,color= 'black',linestyle='--') 
#fig= sns.lineplot(x=dat['x'], y=dat['y'],data=dat,color= 'black',marker='d')  
ax.axvline(x=2005, color='black' , linestyle='--')
plt.show




sns.set_style('ticks')
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
fig, ax = plt.subplots(figsize=(10, 5))
styles = dict(ha="center", va="center", color="black", size=15)
ax.annotate(s="Before the livestock\nreduction", xy=(1994, 0.8), **styles)
ax.annotate(s="After the livestock\nreduction", xy=(2009, 0.8), **styles)
plt.xlim((1988, 2013))
plt.ylim((0,4))
plt.xticks(list(range(1988,2013,1)),rotation=90)            # 刻度线的设置  True为去掉  False为保留
plt.yticks(list(range(0,4,1)))        #xticks，.yticks为设置x,y坐标的刻度值
font2 = {'family' : 'Times New Roman','weight' : 'normal','size' : 20}
sns.set(font="SimHei")
sns.despine(top=True, right=True, left=False, bottom=False, offset=None, trim=False)   #边框的设置
fig1 = sns.lineplot(x=sheeps.iloc[:16,0], y=sheeps.iloc[:16,4],data = sheeps,color= 'black',marker='s',ms=10)
fig1 = sns.lineplot(x=sheeps.iloc[15:,0], y=sheeps.iloc[15:,4],data = sheeps,color= 'black',marker='s',ms=10)
z = np.polyfit(sheeps.iloc[:16,0], sheeps.iloc[:16,4], 1)
p = np.poly1d(z)
plt.plot(sheeps.iloc[:16,0],p(sheeps.iloc[:16,0]),color="black")

z = np.polyfit(sheeps.iloc[15:,0], sheeps.iloc[15:,4], 1)
p = np.poly1d(z)
plt.plot(sheeps.iloc[15:,0],p(sheeps.iloc[15:,0]),color="black")

plt.legend(loc='upper center',ncol = 1,frameon=False,fontsize=18,handletextpad=0.1)
plt.xlabel('Year',font2)
plt.ylabel(u'Index of grazing pressure',font2)
ax.axvline(x=2005, color='black' , linestyle='--')
plt.show

