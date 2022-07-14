# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 10:41:33 2021

@author: 树风
"""
import os                               
import rasterio 
import numpy as np   
import pandas as pd                      
path = r'D:\qinxuejie\NPP'  
outpath = r'D:\qinxuejie\out_npp'
Files=list()  #定义空的列表
for i in range(2000,2016) :
    for j in range(1,13) :
        j='%02d' % j  #把1改成01的样子
        File = path+os.sep+"IDAHO_EPSCOR-TERRACLIMATE-" + str(i) + str(j) +".tif"   #获取数据源中的所有文件
        Files.append(File)   #把一年的文件名进行叠加
        if j==12:  #如果到了第12个月就跳到下一年
            break;  
    print(Files)        
    for k, l in enumerate(Files):  # enumerate 遍历数据对象
        with rasterio.open(l) as Src_read:  # "rasterio.open":打开栅格数据
            profile = Src_read.profile #profile：源数据属性    
            temp = Src_read.read(1)  #读取栅格数据的第一波段，格式为  “数组"
            temp1 = pd.DataFrame(temp)  #转为dataframe
            temp1[temp1 == profile.temp1['nodata']] = np.nan
            # temp2 = temp1.replace(-32768, np.nan)#替换无效值
            temp2 = temp1.values.reshape(-1, 1)  #2维数组重新塑形
            if k == 0:
                data2 = temp2  
            else   :   
                data2 = np.hstack([data2, temp2])#追加每个月的dataframe
    data1 = data2.mean(1).reshape(2592,6041)#求平均后返还数组形状
    out = outpath  +str(i)+"年总平均" + '.tif'#编写输出路径以及文件名
    profile['dtype'] = 'float32'
    with rasterio.open(out , 'w', **profile) as Sre_write:#写出
        Sre_write.write(data1.astype(profile['dtype']), 1)
