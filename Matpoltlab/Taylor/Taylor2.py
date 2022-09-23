# -- coding: utf-8 --
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import pickle
import skill_metrics as sm
from sys import version_info
import pandas as pd


data = pd.read_excel(r"test_data.xlsx")
# 以下操作可以当作固定步骤
taylor_stats1 = sm.taylor_statistics(data.pred1, data.ref, 'data')
taylor_stats2 = sm.taylor_statistics(data.pred2, data.ref, 'data')
taylor_stats3 = sm.taylor_statistics(data.pred3, data.ref, 'data')
sdev = np.array([taylor_stats1['sdev'][0], taylor_stats1['sdev'][1],
                 taylor_stats2['sdev'][1], taylor_stats3['sdev'][1]])
crmsd = np.array([taylor_stats1['crmsd'][0], taylor_stats1['crmsd'][1],
                  taylor_stats2['crmsd'][1], taylor_stats3['crmsd'][1]])
ccoef = np.array([taylor_stats1['ccoef'][0], taylor_stats1['ccoef'][1],
                  taylor_stats2['ccoef'][1], taylor_stats3['ccoef'][1]])

# 设置matplotlib 基本配置
rcParams["figure.figsize"] = [6, 6]
rcParams["figure.facecolor"] = "white"
rcParams["figure.edgecolor"] = "white"
rcParams["figure.dpi"] = 80
rcParams['lines.linewidth'] = 1  #
rcParams["font.family"] = "Times New Roman"
rcParams.update({'font.size': 12})  #
plt.close('all')
# 开始绘图
text_font = {'size': '15', 'weight': 'bold', 'color': 'black'}
sm.taylor_diagram(sdev, crmsd, ccoef)
plt.title("Example01 Of taylor_diagram() in Python", fontdict=text_font, pad=35)


#2
# sm.taylor_diagram(sdev,crmsd,ccoef, markerLabel = label,
#                       titleOBS = 'Observation',
#                       markerLabelColor = 'r',
#                       tickRMS= np.arange(0,30,10),
#                       tickRMSangle = 110.0,
#                       colRMS = 'm', styleRMS = ':', widthRMS = 2.0,
#                       tickSTD = np.arange(10,30,10), axismax = 30.0,
#                       colSTD = 'b', styleSTD = '-.', widthSTD = 1.0,
#                       colCOR = 'k', styleCOR = '--', widthCOR = 1.0)
# text_font = {'size':'15','weight':'bold','color':'black'}
# plt.title("Example02 Of taylor_diagram() in Python",fontdict=text_font,pad=35)


#3
# sm.taylor_diagram(sdev,crmsd,ccoef,
#                       markerDisplayed = 'colorBar', titleColorbar = 'RMSD',
#                      locationColorBar = 'EastOutside',
#                       cmapzdata = crmsd, titleRMS = 'off',
#                       tickRMS = range(0,30,10), tickRMSangle = 110.0,
#                       colRMS = 'm', styleRMS = ':', widthRMS = 2.0,
#                       tickSTD = range(10,30,10), axismax = 30.0,
#                       colSTD = 'k', styleSTD = '-', widthSTD = 1.5,
#                       colCOR = 'k', styleCOR = '--', widthCOR = 1.0)
# text_font = {'size':'15','weight':'bold','color':'black'}
# plt.title("Example03 Of taylor_diagram() in Python",fontdict=text_font,pad=35)