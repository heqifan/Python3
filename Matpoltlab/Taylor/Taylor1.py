# -- coding: utf-8 --
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.font_manager import FontProperties
import numpy as np

Simsun = FontProperties(fname="/home/mw/input/font1842/SimSun.ttf")
Times = FontProperties(fname="/home/mw/input/font1842/Times.ttf")
mpl.rcParams['axes.unicode_minus']=False


fig=plt.figure(figsize=(8,8),dpi=150)
axe = plt.subplot(1,1,1,projection='polar')
axe.set_title('泰勒图',fontproperties=Simsun,fontsize=12,y=1.02)
axe.set_thetalim(thetamin=0, thetamax=90)
r_small, r_big, r_interval=0,1.6,0.25
axe.set_rlim(r_small,r_big)
rad_list=[0,0.2,0.4,0.6,0.7,0.8,0.85,0.9,0.95,0.99,1]           #需要显示数值的主要R的值
minor_rad_list=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.65,0.7,0.75,0.8,0.85,0.86,0.87,0.88,0.89,
                0.9,0.91,0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99,1]     #需要显示刻度的次要R的值
angle_list = np.rad2deg(np.arccos(rad_list))
angle_list_rad=np.arccos(rad_list)
angle_minor_list = np.arccos(minor_rad_list)
axe.set_thetagrids(angle_list, rad_list)

for i in np.arange(r_small, r_big, r_interval):
    if i == 1:
        axe.text(0, i, s='\n' + 'REF', fontproperties=Times, fontsize=8,
                      ha='center', va='top')  # text的第一个坐标是角度（弧度制），第二个是距离
    else:
        axe.text(0, i, s='\n' + str(i), fontproperties=Times, fontsize=8,
                      ha='center', va='top')  # text的第一个坐标是角度（弧度制），第二个是距离
    axe.text(np.pi / 2, i, s=str(i) + '  ', fontproperties=Times, fontsize=8,
                  ha='right', va='center')  # text的第一个坐标是角度（弧度制），第二个是距离

axe.set_rgrids([])
labels = axe.get_xticklabels() + axe.get_yticklabels()
[label.set_fontproperties(FontProperties(fname="/home/mw/input/font1842/Times.ttf", size=8)) for label in labels]

axe.grid(False)

angle_linewidth,angle_length,angle_minor_length=0.8,0.02,0.01
tick = [axe.get_rmax(), axe.get_rmax() * (1 - angle_length)]
tick_minor = [axe.get_rmax(), axe.get_rmax() * (1 - angle_minor_length)]
for t in angle_list_rad:
    axe.plot([t, t], tick, lw=angle_linewidth, color="k")  # 第一个坐标是角度（角度制），第二个是距离
for t in angle_minor_list:
    axe.plot([t, t], tick_minor, lw=angle_linewidth, color="k")  # 第一个坐标是角度（角度制），第二个是距离

circle = plt.Circle((1, 0), 0.25, transform=axe.transData._b, facecolor=(0, 0, 0, 0), edgecolor='blue',linestyle='--', linewidth=0.8)
circle1 = plt.Circle((1, 0), 0.5, transform=axe.transData._b, facecolor=(0, 0, 0, 0), edgecolor='blue',linestyle='--', linewidth=0.8)
circle2 = plt.Circle((1, 0), 0.75, transform=axe.transData._b, facecolor=(0, 0, 0, 0), edgecolor='blue',linestyle='--', linewidth=0.8)
circle3 = plt.Circle((1, 0), 1, transform=axe.transData._b, facecolor=(0, 0, 0, 0), edgecolor='blue',linestyle='--', linewidth=0.8)
axe.add_artist(circle)
axe.add_artist(circle1)
axe.add_artist(circle2)
axe.add_artist(circle3)

circle4 = plt.Circle((0, 0), 0.5, transform=axe.transData._b, facecolor=(0, 0, 0, 0), edgecolor='red',linestyle='--', linewidth=0.8)
circle5 = plt.Circle((0, 0), 1, transform=axe.transData._b, facecolor=(0, 0, 0, 0), edgecolor='red',linestyle='--', linewidth=0.8)
circle6 = plt.Circle((0, 0), 1.5, transform=axe.transData._b, facecolor=(0, 0, 0, 0), edgecolor='red',linestyle='--', linewidth=0.8)
axe.add_artist(circle4)
axe.add_artist(circle5)
axe.add_artist(circle6)


axe.set_xlabel('Normalized', fontproperties=Times, labelpad=18, fontsize=8)
axe.text(np.deg2rad(45), 1.8, s='COR', fontproperties=Times, fontsize=8, ha='center', va='bottom', rotation=-45)

axe.plot([0,np.arccos(0.4)],[0,1.6],lw=0.7,color='green',linestyle='--')
axe.plot([0,np.arccos(0.6)],[0,1.6],lw=0.7,color='green',linestyle='--')
axe.plot([0,np.arccos(0.8)],[0,1.6],lw=0.7,color='green',linestyle='--')
axe.plot([0,np.arccos(0.9)],[0,1.6],lw=0.7,color='green',linestyle='--')
axe.plot([0,np.arccos(0.95)],[0,1.6],lw=0.7,color='green',linestyle='--')
axe.plot([0,np.arccos(0.99)],[0,1.6],lw=0.7,color='green',linestyle='--')

axe.plot(float(np.arccos(0.75)), 1.1, '+',color='green',markersize=6.5, label='Green+')
axe.text(np.arccos(0.75), 1.05, s='A',fontproperties=Times, fontsize=10)
axe.plot(float(np.arccos(0.97)), 1.2, 'o',color='red',markersize=6.5, label='Redo')
axe.text(np.arccos(0.97), 1.25, s='B',fontproperties=Times, fontsize=10)
legend = plt.legend(loc='upper right', title="图例", prop=FontProperties(fname="/home/mw/input/font1842/Times.ttf", size=8),
                    labelspacing=1, markerscale=1,bbox_to_anchor=(1.03,1.03))
legend.get_title().set_fontproperties(FontProperties(fname="/home/mw/input/font1842/SimSun.ttf"))
legend.get_title().set_fontsize(fontsize=10)

plt.show()