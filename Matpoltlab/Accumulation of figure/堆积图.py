# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 20:15:12 2021

@author: 树风
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.font_manager import FontProperties
myfont=FontProperties(fname=r'/Users/Library/Fonts/SourceHanSansSC-Normal.otf')
sns.set(font=myfont.get_family())
sns.set_style("whitegrid",{"font.sans-serif":['Source Han Sans CN']})
path = r'C:\Users\树风\Desktop\seaborn\seaborn数据/'
path_list = ['size5.csv' ,'size7.csv','size8.csv']
zhong = pd.DataFrame()
i= 5
sns.set_style('darkgrid')
for path3 in path_list:      #循环读取数据
    data = pd.read_csv(path+path3,names = ['图像数'])   
    list1 = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']*35
    data['月'] = list1
    years =list(range(1986,2021))
    list3 = []
    for year in years: 
        list2 = [str(year)]*12
        list3 = list3 + list2
    data['年'] = list3
    tuxiang = data['图像数'].values.reshape(35,-1)   #重新塑形，整成想要的dataframe的数据框的形状
    df1 = pd.DataFrame(tuxiang,index= list(data['年'].unique()),columns= list(data['月'].unique()))
    df1.sort_index(ascending=False,inplace = True)     #根据索引降序排列
    plt.figure(figsize=(10,8))    #绘制画布，宽度，高度，以英寸为单位
    tu = sns.heatmap(data=df1 , cmap="hsv",annot=True,fmt="d",cbar=True)   #cmap 从数据值到颜色空间的映射。
    plt.title(path3[:7])   #设置图的标题          #annot 如果为True，则在每个单元格中写入数据值。
    plt.show()  #展示图                   #fmt 添加注释时要使用的字符串格式化代码。  'd'为整数
    zhong[str(i)] = data['图像数']        # cbar  是否绘制颜色条;
    i+=1    #这里顺便将每个lansat的数据整合放在一个新的数据框,为后面做铺垫              
zhong['lansat'] = zhong.iloc[:,:].sum(axis=1)         #计算所有lansat的数据之和
tuxiang = zhong['lansat'].values.reshape(35,-1)   #一样要塑形
lansats = pd.DataFrame(tuxiang,index= list(data['年'].unique()),columns= list(data['月'].unique()))
lansats.sort_index(ascending=False,inplace = True)    
plt.figure(figsize=(10,8))
tu = sns.heatmap(data=lansats , cmap="hsv",annot=True,fmt="d",cbar=True)
plt.title('lansat5,7,8')   #这里的操作与上面是一样的意思
plt.show()    
year_zhongs = []  #定义一个空的列表，将会存放每年的数据，有每个lansat的,有所有lansat的。
k = 12
rc = {'font.sans-serif': 'SimHei',     # 设置中文
      'axes.unicode_minus': False}
for j in range(0,35):
    year_zhong  = list(zhong.iloc[k*j:k*j+12,:].sum(axis=0))   #这里就是计算每年的数据
    year_zhongs.append(year_zhong)    
year_zong = pd.DataFrame(year_zhongs,index=None,columns= ['lansat5','lansat7','lansat8','lansat5,7,8'])
year_zong['lansat5,7'] = year_zong.iloc[:,:2].sum(axis=1)    #计算lansat的5和7的和，因为后面画堆积图时很重要
year_zong['年'] = list(data['年'].unique())     
sns.set_context({"figure.figsize": (24, 10)})   #这里也是定义画布的意思，但是这里使用seaborn的函数，主要区别是字典，上面是bool
sns.set(style='ticks',palette='dark',color_codes=True, rc=rc)    #与set_theme等效，后面可能会被删除 用来设置主题 style为设置画布风格，plettle为设置调色板风格，rc：设置中文
sns.despine(top=False, right=False, left=False, bottom=False, offset=None, trim=False) # 刻度线的设置 offset 绝对距离，以点为单位，刻度应远离轴(负值将使脊柱向内移动)。单个值适用于所有脊柱;可以使用字典来设置每边的偏移值。
plt.xticks(list(range(1986,2021,1)),rotation=90,size = 30)            # 刻度线的设置  True为去掉  False为保留
plt.yticks(list(range(0,150,10)),size = 30)        #xticks，.yticks为设置x,y坐标的刻度值
sns.barplot(x = year_zong['年'], y = year_zong['lansat5,7,8'], color = "orangered") #建立矩形条  
bottom_plot = sns.barplot(x = year_zong['年'], y = year_zong['lansat5,7'], color = "darkorange")  #再建立矩形条，会自动覆盖在底部
bottom_plot = sns.barplot(x = year_zong['年'], y = year_zong['lansat5'], color = "olive")    #再建立矩形条，会自动覆盖在底部
bottombar2 = plt.Rectangle((0,0),1,1,fc='orangered',  edgecolor = 'none')   
topbar = plt.Rectangle((0,0),1,1,fc="darkorange", edgecolor = 'none')   #设置矩形条的形状
bottombar1 = plt.Rectangle((0,0),1,1,fc='olive',  edgecolor = 'none')
l = plt.legend([bottombar2, topbar,bottombar1], ['OLI', 'ETM+','TM'], loc=2, ncol = 1, prop={'size':25})   #设置图例，并对应矩形条，设置名称，字体大小
bottom_plot.set_ylabel('影像的数量',size = 50,labelpad=30)  #设置y轴上的标题
bottom_plot.set_xlabel('年份',size =50,labelpad=30)     #设置x轴上的标题
sns.despine()  #从图中删除顶部和右侧的轴
plt.show()

