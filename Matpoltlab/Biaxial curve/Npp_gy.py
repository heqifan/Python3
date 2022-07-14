# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 09:40:21 2021

@author: 树风
"""

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
npp_gy = pd.read_excel(inpath + 'Zonalstas0228.xlsx',sheet_name='县',header = None)
a_npp = npp_gy.iloc[1:23,1:20]
a_gy = npp_gy.iloc[27:49,1:20]
a_npp.set_index(1, drop=True,inplace =True)
a_gy.set_index(1, drop=True,inplace =True)
a_npp.columns = list(range(2000,2018))
a_gy.columns = list(range(2000,2018))
a_npp1 = a_npp.loc[['兴海县'],:].T
a_npp1['年'] = a_npp1.index
a_npp2 = a_npp.loc[['同德县'],:].T
a_npp2['年'] = a_npp2.index
a_npp3 = a_npp.loc[['泽库县'],:].T
a_npp3['年'] = a_npp3.index
a_npp4 = a_npp.loc[['玛沁县'],:].T
a_npp4['年'] = a_npp4.index
sns.set_style('ticks')
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.figure(figsize=(10,5))    #绘制画布，宽度，高度，以英寸为单位
plt.xlim((2000, 2018))
plt.ylim((50,1050))
plt.xticks(list(range(2000,2018,1)),rotation=270)            # 刻度线的设置  True为去掉  False为保留
plt.yticks(list(range(50,1050,100)))        #xticks，.yticks为设置x,y坐标的刻度值
font2 = {'family' : 'Times New Roman','weight' : 'normal','size' : 30}
plt.ylabel('NPP',font2)  #不要x,y轴上的标签
sns.set(font="SimHei")
sns.despine(top=True, right=True, left=False, bottom=False, offset=None, trim=False)   #边框的设置
fig = sns.lineplot(x=a_npp1['年'], y=a_npp1['兴海县'],data = a_npp1,color= 'black',marker='s',ms=10,label=u"兴海 Xinghai")
fig = sns.lineplot(x=a_npp2['年'], y=a_npp2['同德县'],data = a_npp2,color= 'black',marker='o',ms=10,label=u"同德 Tongde")  
fig = sns.lineplot(x=a_npp3['年'], y=a_npp3['泽库县'],data = a_npp3,color= 'black',marker='h',ms=10,label=u"泽库 Zeku") 
fig = sns.lineplot(x=a_npp4['年'], y=a_npp4['玛沁县'],data = a_npp4,color= 'black',marker='D',ms=10,label=u"玛沁 Maqin") 
#plt.legend(loc='lower center',ncol = 4,frameon=False,fontsize=18,columnspacing = 0.2,handletextpad=0.1)
#box = ax1.get_position()
#ax1.set_position([box.x0, box.y0, box.width , box.height* 0.8])
plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3),ncol = 4,frameon=False,fontsize=18,columnspacing = 0.2,handletextpad=0.1)
plt.xlabel(None)
plt.show
a_npp1 = a_npp.loc[['河南县'],:].T
a_npp1['年'] = a_npp1.index
a_npp2 = a_npp.loc[['甘德县'],:].T
a_npp2['年'] = a_npp2.index
a_npp3 = a_npp.loc[['久治县'],:].T
a_npp3['年'] = a_npp3.index
a_npp4 = a_npp.loc[['班玛县'],:].T
a_npp4['年'] = a_npp4.index
sns.set_style('ticks')
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.figure(figsize=(10,5))    #绘制画布，宽度，高度，以英寸为单位
sns.despine(top=True, right=True, left=False, bottom=False, offset=None, trim=False)   #边框的设置
plt.xlim((2000, 2018))
plt.ylim((50,1050))
plt.xticks(list(range(2000,2018,1)),rotation=270)         # 刻度线的设置  True为去掉  False为保留
plt.yticks(list(range(50,1050,100)))        #xticks，.yticks为设置x,y坐标的刻度值
font2 = {'family' : 'Times New Roman','weight' : 'normal','size' : 30}
plt.ylabel('NPP',font2)  #不要x,y轴上的标签
sns.set(font="SimHei")
sns.despine(top=True, right=True, left=False, bottom=False, offset=None, trim=False)   #边框的设置
fig = sns.lineplot(x=a_npp1['年'], y=a_npp1['河南县'],data = a_npp1,color= 'black',marker='s',ms=10,label=u"河南 Henan")
fig = sns.lineplot(x=a_npp2['年'], y=a_npp2['甘德县'],data = a_npp2,color= 'black',marker='o',ms=10,label=u"甘德 Gande")  
fig = sns.lineplot(x=a_npp3['年'], y=a_npp3['久治县'],data = a_npp3,color= 'black',marker='h',ms=10,label=u"久治 Jiuzhi") 
fig = sns.lineplot(x=a_npp4['年'], y=a_npp4['班玛县'],data = a_npp4,color= 'black',marker='D',ms=10,label=u"班玛 Banma") 
plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3),ncol = 4,frameon=False,fontsize=18,columnspacing = 0.2,handletextpad=0.1)
plt.xlabel(None)
plt.show
a_npp1 = a_npp.loc[['达日县'],:].T
a_npp1['年'] = a_npp1.index
a_npp2 = a_npp.loc[['玛多县'],:].T
a_npp2['年'] = a_npp2.index
a_npp3 = a_npp.loc[['曲麻莱县'],:].T
a_npp3['年'] = a_npp3.index
a_npp4 = a_npp.loc[['称多县'],:].T
a_npp4['年'] = a_npp4.index
sns.set_style('ticks')
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.figure(figsize=(10,5))    #绘制画布，宽度，高度，以英寸为单位
sns.despine(top=True, right=True, left=False, bottom=False, offset=None, trim=False)   #边框的设置
plt.xlim((2000, 2018))
plt.ylim((50,1050))
plt.xticks(list(range(2000,2018,1)),rotation=270)            # 刻度线的设置  True为去掉  False为保留
plt.yticks(list(range(50,1050,100)))        #xticks，.yticks为设置x,y坐标的刻度值
font2 = {'family' : 'Times New Roman','weight' : 'normal','size' : 30}
plt.ylabel('NPP',font2)  #不要x,y轴上的标签
sns.set(font="SimHei")
sns.despine(top=True, right=True, left=False, bottom=False, offset=None, trim=False)   #边框的设置
fig = sns.lineplot(x=a_npp1['年'], y=a_npp1['达日县'],data = a_npp1,color= 'black',marker='s',ms=10,label=u"达日 Dari")
fig = sns.lineplot(x=a_npp2['年'], y=a_npp2['玛多县'],data = a_npp2,color= 'black',marker='o',ms=10,label=u"玛多 Maduo")  
fig = sns.lineplot(x=a_npp3['年'], y=a_npp3['曲麻莱县'],data = a_npp3,color= 'black',marker='h',ms=10,label=u"曲麻莱 Qumalai") 
fig = sns.lineplot(x=a_npp4['年'], y=a_npp4['称多县'],data = a_npp4,color= 'black',marker='D',ms=10,label=u"称多县 Chenduo") 
plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3),ncol = 4,frameon=False,fontsize=18,columnspacing = 0.2,handletextpad=0.1)
plt.xlabel(None)
plt.show
a_npp1 = a_npp.loc[['玉树市'],:].T
a_npp1['年'] = a_npp1.index
a_npp2 = a_npp.loc[['囊谦县'],:].T
a_npp2['年'] = a_npp2.index
a_npp3 = a_npp.loc[['杂多县'],:].T
a_npp3['年'] = a_npp3.index
a_npp4 = a_npp.loc[['治多县'],:].T
a_npp4['年'] = a_npp4.index
a_npp5 = a_npp.loc[['唐古拉山乡'],:].T
a_npp5['年'] = a_npp5.index
sns.set_style('ticks')
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.figure(figsize=(10,5))    #绘制画布，宽度，高度，以英寸为单位
sns.despine(top=True, right=True, left=False, bottom=False, offset=None, trim=False)   #边框的设置
plt.xlim((2000, 2018))
plt.ylim((50,1050))
plt.xticks(list(range(2000,2018,1)),rotation=270)            # 刻度线的设置  True为去掉  False为保留
plt.yticks(list(range(50,1050,100)))        #xticks，.yticks为设置x,y坐标的刻度值
font2 = {'family' : 'Times New Roman','weight' : 'normal','size' : 30}
plt.ylabel('NPP',font2)  #不要x,y轴上的标签
sns.set(font="SimHei")
sns.despine(top=True, right=True, left=False, bottom=False, offset=None, trim=False)   #边框的设置
fig = sns.lineplot(x=a_npp1['年'], y=a_npp1['玉树市'],data = a_npp1,color= 'black',marker='s',ms=10,label=u"玉树 Yushu")
fig = sns.lineplot(x=a_npp2['年'], y=a_npp2['囊谦县'],data = a_npp2,color= 'black',marker='o',ms=10,label=u"囊谦 Nangqian") 
fig = sns.lineplot(x=a_npp3['年'], y=a_npp3['杂多县'],data = a_npp3,color= 'black',marker='h',ms=10,label=u"杂多 Zhaduo") 
fig = sns.lineplot(x=a_npp4['年'], y=a_npp4['治多县'],data = a_npp4,color= 'black',marker='D',ms=10,label=u"治多 Zhiduo") 
fig = sns.lineplot(x=a_npp5['年'], y=a_npp5['唐古拉山乡'],data = a_npp5,color= 'black',marker='^',ms=10,label=u"唐古拉 Tanggula") 
plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.4),ncol = 3,frameon=False,fontsize=18,columnspacing = 0.2,handletextpad=0.1)
plt.xlabel(None)
plt.show










a_gy1 = a_gy.loc[['兴海县'],:].T
a_gy1['年'] = a_gy1.index
a_gy2 = a_gy.loc[['同德县'],:].T
a_gy2['年'] = a_gy2.index
a_gy3 = a_gy.loc[['泽库县'],:].T
a_gy3['年'] = a_gy3.index
a_gy4 = a_gy.loc[['玛沁县'],:].T
a_gy4['年'] = a_gy4.index
sns.set_style('ticks')
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.figure(figsize=(10,5))    #绘制画布，宽度，高度，以英寸为单位
plt.xlim((2000, 2018))
plt.ylim((450,8000))
plt.xticks(list(range(2000,2018,1)),rotation=270)            # 刻度线的设置  True为去掉  False为保留
plt.yticks(list(range(450,8000,500)))        #xticks，.yticks为设置x,y坐标的刻度值
font2 = {'family' : 'Times New Roman','weight' : 'normal','size' : 30}
plt.ylabel('Yield(kg/hm\u00b2)',fontproperties = font2)  #不要x,y轴上的标签
sns.set(font="SimHei")
sns.despine(top=True, right=True, left=False, bottom=False, offset=None, trim=False)   #边框的设置
fig = sns.lineplot(x=a_gy1['年'], y=a_gy1['兴海县'],data = a_gy1,color= 'black',marker='s',ms=10,label=u"兴海 Xinghai")
fig = sns.lineplot(x=a_gy2['年'], y=a_gy2['同德县'],data = a_gy2,color= 'black',marker='o',ms=10,label=u"同德 Tongde")  
fig = sns.lineplot(x=a_gy3['年'], y=a_gy3['泽库县'],data = a_gy3,color= 'black',marker='h',ms=10,label=u"泽库 Zeku") 
fig = sns.lineplot(x=a_gy4['年'], y=a_gy4['玛沁县'],data = a_gy4,color= 'black',marker='D',ms=10,label=u"玛沁 Maqin") 
#plt.legend(loc='lower center',ncol = 4,frameon=False,fontsize=18,columnspacing = 0.2,handletextpad=0.1)
#box = ax1.get_position()
#ax1.set_position([box.x0, box.y0, box.width , box.height* 0.8])
plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3),ncol = 4,frameon=False,fontsize=18,columnspacing = 0.2,handletextpad=0.1)
plt.xlabel(None)
plt.show
a_gy1 = a_gy.loc[['河南县'],:].T
a_gy1['年'] = a_gy1.index
a_gy2 = a_gy.loc[['甘德县'],:].T
a_gy2['年'] = a_gy2.index
a_gy3 = a_gy.loc[['久治县'],:].T
a_gy3['年'] = a_gy3.index
a_gy4 = a_gy.loc[['班玛县'],:].T
a_gy4['年'] = a_gy4.index
sns.set_style('ticks')
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.figure(figsize=(10,5))    #绘制画布，宽度，高度，以英寸为单位
sns.despine(top=True, right=True, left=False, bottom=False, offset=None, trim=False)   #边框的设置
plt.xlim((2000, 2018))
plt.ylim((450,8000))
plt.xticks(list(range(2000,2018,1)),rotation=270)         # 刻度线的设置  True为去掉  False为保留
plt.yticks(list(range(450,8000,500)))        #xticks，.yticks为设置x,y坐标的刻度值
font2 = {'family' : 'Times New Roman','weight' : 'normal','size' : 30}
plt.ylabel('Yield(kg/hm\u00b2)',fontproperties = font2)  #不要x,y轴上的标签
sns.set(font="SimHei")
sns.despine(top=True, right=True, left=False, bottom=False, offset=None, trim=False)   #边框的设置
fig = sns.lineplot(x=a_gy1['年'], y=a_gy1['河南县'],data = a_gy1,color= 'black',marker='s',ms=10,label=u"河南 Henan")
fig = sns.lineplot(x=a_gy2['年'], y=a_gy2['甘德县'],data = a_gy2,color= 'black',marker='o',ms=10,label=u"甘德 Gande")  
fig = sns.lineplot(x=a_gy3['年'], y=a_gy3['久治县'],data = a_gy3,color= 'black',marker='h',ms=10,label=u"久治 Jiuzhi") 
fig = sns.lineplot(x=a_gy4['年'], y=a_gy4['班玛县'],data = a_gy4,color= 'black',marker='D',ms=10,label=u"班玛 Banma") 
plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3),ncol = 4,frameon=False,fontsize=18,columnspacing = 0.2,handletextpad=0.1)
plt.xlabel(None)
plt.show
a_gy1 = a_gy.loc[['达日县'],:].T
a_gy1['年'] = a_gy1.index
a_gy2 = a_gy.loc[['玛多县'],:].T
a_gy2['年'] = a_gy2.index
a_gy3 = a_gy.loc[['曲麻莱县'],:].T
a_gy3['年'] = a_gy3.index
a_gy4 = a_gy.loc[['称多县'],:].T
a_gy4['年'] = a_gy4.index
sns.set_style('ticks')
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.figure(figsize=(10,5))    #绘制画布，宽度，高度，以英寸为单位
sns.despine(top=True, right=True, left=False, bottom=False, offset=None, trim=False)   #边框的设置
plt.xlim((2000, 2018))
plt.ylim((450,8000))
plt.xticks(list(range(2000,2018,1)),rotation=270)            # 刻度线的设置  True为去掉  False为保留
plt.yticks(list(range(450,8000,500)))        #xticks，.yticks为设置x,y坐标的刻度值
font2 = {'family' : 'Times New Roman','weight' : 'normal','size' : 30}
plt.ylabel('Yield(kg/hm\u00b2)',fontproperties = font2)  #不要x,y轴上的标签
sns.set(font="SimHei")
sns.despine(top=True, right=True, left=False, bottom=False, offset=None, trim=False)   #边框的设置
fig = sns.lineplot(x=a_gy1['年'], y=a_gy1['达日县'],data = a_gy1,color= 'black',marker='s',ms=10,label=u"达日 Dari")
fig = sns.lineplot(x=a_gy2['年'], y=a_gy2['玛多县'],data = a_gy2,color= 'black',marker='o',ms=10,label=u"玛多 Maduo")  
fig = sns.lineplot(x=a_gy3['年'], y=a_gy3['曲麻莱县'],data = a_gy3,color= 'black',marker='h',ms=10,label=u"曲麻莱 Qumalai") 
fig = sns.lineplot(x=a_gy4['年'], y=a_gy4['称多县'],data = a_gy4,color= 'black',marker='D',ms=10,label=u"称多县 Chenduo") 
plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3),ncol = 4,frameon=False,fontsize=18,columnspacing = 0.2,handletextpad=0.1)
plt.xlabel(None)
plt.show
a_gy1 = a_gy.loc[['玉树市'],:].T
a_gy1['年'] = a_gy1.index
a_gy2 = a_gy.loc[['囊谦县'],:].T
a_gy2['年'] = a_gy2.index
a_gy3 = a_gy.loc[['杂多县'],:].T
a_gy3['年'] = a_gy3.index
a_gy4 = a_gy.loc[['治多县'],:].T
a_gy4['年'] = a_gy4.index
a_gy5 = a_gy.loc[['唐古拉山乡'],:].T
a_gy5['年'] = a_gy5.index
sns.set_style('ticks')
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.figure(figsize=(10,5))    #绘制画布，宽度，高度，以英寸为单位
sns.despine(top=True, right=True, left=False, bottom=False, offset=None, trim=False)   #边框的设置
plt.xlim((2000, 2018))
plt.ylim((450,8000))
plt.xticks(list(range(2000,2018,1)),rotation=270)            # 刻度线的设置  True为去掉  False为保留
plt.yticks(list(range(450,8000,500)))        #xticks，.yticks为设置x,y坐标的刻度值
font2 = {'family' : 'Times New Roman','weight' : 'normal','size' : 30}
plt.ylabel(u'Yield(kg/hm\u00b2)',fontproperties = font2)  #不要x,y轴上的标签
sns.set(font="SimHei")
sns.despine(top=True, right=True, left=False, bottom=False, offset=None, trim=False)   #边框的设置
fig = sns.lineplot(x=a_gy1['年'], y=a_gy1['玉树市'],data = a_gy1,color= 'black',marker='s',ms=10,label=u"玉树 Yushu")
fig = sns.lineplot(x=a_gy2['年'], y=a_gy2['囊谦县'],data = a_gy2,color= 'black',marker='o',ms=10,label=u"囊谦 Nangqian") 
fig = sns.lineplot(x=a_gy3['年'], y=a_gy3['杂多县'],data = a_gy3,color= 'black',marker='h',ms=10,label=u"杂多 Zhaduo") 
fig = sns.lineplot(x=a_gy4['年'], y=a_gy4['治多县'],data = a_gy4,color= 'black',marker='D',ms=10,label=u"治多 Zhiduo") 
fig = sns.lineplot(x=a_gy5['年'], y=a_gy5['唐古拉山乡'],data = a_gy5,color= 'black',marker='^',ms=10,label=u"唐古拉 Tanggula") 
plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.4),ncol = 3,frameon=False,fontsize=18,columnspacing = 0.2,handletextpad=0.1)
plt.xlabel(None)
plt.show