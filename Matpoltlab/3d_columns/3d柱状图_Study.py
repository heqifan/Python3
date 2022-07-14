# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 00:43:54 2022

@author: HYF
"""
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mplfonts import use_font
use_font('Noto Serif CJK SC')#指定中文字体

import mpl_toolkits.mplot3d

#设置x轴取值
xedges = np.array([10,20,30,40])
#设置y轴取值
yedges = np.array([20,30,40,50,60,70,80])
#设置X,Y对应点的值。即原始数据。
hist =np.array( [[1,2,3,4,5,6],
[0.1027,0.1039,0.1057,0.1069,0.1078,0.1109],
[0.1046,0.1059,0.1061,0.1079,0.1085,0.1114],
])

#生成图表对象。
fig = plt.figure()
#生成子图对象，类型为3d
ax = fig.add_subplot(111,projection='3d')


#设置作图点的坐标
xpos, ypos = np.meshgrid(xedges[:-1]-2.5 , yedges[:-1]-2.5 )
xpos = xpos.flatten('F')
ypos = ypos.flatten('F')
zpos = np.zeros_like(xpos)


#设置柱形图大小
dx =5 * np.ones_like(zpos)
dy = dx.copy()
dz = hist.flatten()

#设置坐标轴标签
ax.set_xlabel('R')
ax.set_ylabel('K')
ax.set_zlabel('Recall')
# x, y, z: array - like

# The coordinates of the anchor point of the bars.
# dx, dy, dz: scalar or array - like
# The width, depth, and height of the bars, respectively.
# minx = np.min(x)
# maxx = np.max(x + dx)
# miny = np.min(y)
# maxy = np.max(y + dy)
# minz = np.min(z)
# maxz = np.max(z + dz)
ax.bar3d(xpos, ypos, zpos, dx, dy, dz,color='b',zsort='average')
plt.show()