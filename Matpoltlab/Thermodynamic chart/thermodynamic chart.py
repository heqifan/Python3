# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 13:05:17 2021

@author: 树风
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
path = r'D:\python作业\seaborn\数据/'
path_list = ['lansat5.txt' ,'lansat7.txt','lansat8.txt']
zhong = pd.DataFrame()
i= 5
# sns.set_style('darkgrid')
for path3 in path_list:      #循环读取数据
    data = pd.read_csv(path+path3,names = ['图像数'])   
    list1 = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']*29
    data['月'] = list1
    years =list(range(1988,2017))
    list3 = []
    for year in years: 
        list2 = [str(year)]*12
        list3 = list3 + list2
    data['年'] = list3
    tuxiang = data['图像数'].values.reshape(29,-1)   #重新塑形，整成想要的dataframe的数据框的形状
    df1 = pd.DataFrame(tuxiang,index= list(data['年'].unique()),columns= list(data['月'].unique()))
    df1.sort_index(ascending=False,inplace = True)     #根据索引降序排列
    plt.figure(figsize=(10,8))    #绘制画布，宽度，高度，以英寸为单位
    tu = sns.heatmap(data=df1 , cmap="hsv",annot=True,fmt="d",cbar=True)   #cmap 从数据值到颜色空间的映射。
    plt.title(path3[:7])   #设置图的标题          #annot 如果为True，则在每个单元格中写入数据值。
    plt.show()  #展示图                   #fmt 添加注释时要使用的字符串格式化代码。  'd'为整数
    zhong[str(i)] = data['图像数']        # cbar  是否绘制颜色条;
    i+=1    #这里顺便将每个lansat的数据整合放在一个新的数据框,为后面做铺垫
zhong['lansat'] = zhong.iloc[:,:].sum(axis=1)         #计算所有lansat的数据之和
tuxiang = zhong['lansat'].values.reshape(29,-1)   #一样要塑形
lansats = pd.DataFrame(tuxiang,index= list(data['年'].unique()),columns= list(data['月'].unique()))
lansats.sort_index(ascending=False,inplace = True)    
plt.figure(figsize=(8,8))
tu = sns.heatmap(data=lansats , cmap='hsv',annot=True,fmt="d",vmax = 45,annot_kws={'size':9,'color':'black'},vmin = 0,cbar=True,xticklabels=True)
# plt.title('Lansat5,7,8')   #这里的操作与上面是一样的意思
plt.xticks(rotation=90)
plt.xlabel('(b)Month',fontsize = 15)
plt.show()    