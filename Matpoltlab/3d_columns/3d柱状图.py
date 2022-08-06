# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 18:18:29 2022

@author: HYF
"""
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mplfonts import use_font
# use_font('Noto Serif CJK SC')#指定中文字体

import mpl_toolkits.mplot3d
from matplotlib.font_manager import _rebuild

_rebuild() #reload一下
matplotlib.rcParams['font.family'] = 'Times New Roman'
matplotlib.rcParams['mathtext.default'] = 'regular'

inpath = r'D:\Cheng\npp稳定性之滑动窗口0725.xlsx'

data = pd.read_excel(inpath,index_col = 0,header=None)
RCP4_5 = data.iloc[:,0:5]
RCP8_5 = data.iloc[:,6:]

y_tickets = [u"青藏高原区",u"青藏高原区",u"热带-亚热带季风区",u"温带季风区",u"温带大陆区",u"全国"]  #Bug1
x_tickets = ['','2011-2030','2031-2050','2051-2070',' ','2071-2094']   #Bug2

zlabels = ['RCP4.5NPP稳定性','RCP8.5NPP稳定性']

x = np.array([10,20,30,40,50])
y = np.array([20,30,40,50,60,70])


RCP8_5_z_1 = list(RCP8_5.iloc[:20,:].mean())
RCP8_5_z_2 = list(RCP8_5.iloc[20:40,:].mean())
RCP8_5_z_3 = list(RCP8_5.iloc[40:60,:].mean())
RCP8_5_z_4 = list(RCP8_5.iloc[60:,:].mean())
RCP8_5_z = np.array(RCP8_5_z_1 + RCP8_5_z_2 + RCP8_5_z_3 + RCP8_5_z_4 ).reshape(4,5)  #转为二维数组

RCP4_5_z_1 = list(RCP4_5.iloc[:20,:].mean())
RCP4_5_z_2 = list(RCP4_5.iloc[20:40,:].mean())
RCP4_5_z_3 = list(RCP4_5.iloc[40:60,:].mean())
RCP4_5_z_4 = list(RCP4_5.iloc[60:,:].mean())
RCP4_5_z = np.array(RCP4_5_z_1 + RCP4_5_z_2 + RCP4_5_z_3 + RCP4_5_z_4).reshape(4,5)

n = 0

color = ['steelblue','darkgoldenrod','steelblue','darkgoldenrod','steelblue',
         'darkturquoise','gold','darkturquoise','gold','darkturquoise',
         'deepskyblue','yellow','deepskyblue','yellow','deepskyblue',
         'LightSteelBlue','LightYellow','LightSteelBlue','LightYellow','LightSteelBlue'
         ]
    
for RCP in [RCP4_5_z,RCP8_5_z]:
        
    fig = plt.figure(dpi=600,figsize=(8,8))   #设置画布大小
    
    ax = fig.add_subplot(111,projection='3d')
    height = np.zeros_like(RCP)  #大小一样的数组，值都为零
    xpos, ypos = np.meshgrid(x[:-1]-2.5 , y[:-1]-2.5 )
    xpos = xpos.flatten('F')  #按列降维
    ypos = ypos.flatten('F')  #按列降维
    zpos = np.zeros_like(xpos)
    
    
    dx =5 * np.ones_like(zpos)  #大小一样的数组，值都为1
    dy = dx.copy()
    dz = RCP.flatten()
    
    
    ax.set_xticklabels(x_tickets,fontsize = 4)  
    ax.set_yticklabels(y_tickets,fontsize = 4)
    
    ax.set_zticklabels([x for x in range(0,150,20)],fontsize = 4)    
    ax.set_zlim(0, 140,20)  #设置最大，最小值，间隔
    
    ax.view_init(elev=10, azim=10)#设置旋转角度 
    
    ax.set_zlabel(zlabels[n],labelpad=3,fontsize = 4)  #设置z轴标签，距离坐标轴的距离，字体大小
    
    ax.set_xlabel('年份 Year',labelpad=7,fontsize = 4)
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz,color=color,zsort='average')
    plt.show()
    n += 1
