# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 16:43:18 2021

@author: 树风
"""
                             
import rasterio 
import numpy as np   
import pandas as pd  
from multiprocessing import Pool     #pool:赋予函数并行化处理一系列输入值的能力，可以将输入数据分配给不同进程处理（数据并行）
import multiprocessing               #多进程进行的库，基于进程的并行
out_path = r'G:/Workspace/China1km/MeteoGrid/MDT_'
in_path_max = r'G:/Workspace/China1km/MeteoGrid/TMAX/TMAX_'
in_path_min = r'G:/Workspace/China1km/MeteoGrid/TMIN/TMIN_'
def fun(data):
    return data.mean(1)
    
for y in range(1,362,8):
    Files=list()  #定义空的列表
    y='%03d' % y  #把1改成001的样子
    for i in range(2005,2021):
        path_max = in_path_max + str(i) + str(y) + '.flt'
        path_min = in_path_min + str(i) + str(y) + '.flt'
        Files.append(path_max)
        Files.append(path_min)
    for k, l in enumerate(Files):  # enumerate 遍历数据对象
        with rasterio.open(l) as Src_read:  # "rasterio.open":打开栅格数据
            width1 = Src_read.width
            height1 = Src_read.height
            profile = Src_read.profile #profile：源数据属性    
            temp = Src_read.read(1)  #读取栅格数据的第一波段，格式为  “数组"
            temp1 = pd.DataFrame(temp)  #转为dataframe
            temp1[temp1 == profile.temp1['nodata']] = np.nan
            temp2 = temp1.values.reshape(-1, 1)  #2维数组重新塑形
            if k == 0:
                data2 = temp2  
            else   :   
                data2 = np.hstack([data2, temp2])#追加
    cores = multiprocessing.cpu_count()  # 计算机cpu的核心数（核心数=线程数，但具有多线程技术和超线程技术的线程数一般为核心数的两倍）
    pool = Pool(cores)            # 开启线程池
    data3 = pool.map(fun, data2)           # 进行并行计算，得到的data2是一个列表，map是按行读取数组来计算 return回多少个变量就有多少列
    data3 = pd.DataFrame(data3)    
    data3 = data3[:, 0]
    data3 = data3.reshape(height1, width1)
    out = out_path  + str(y)  + '.flt'#编写输出路径以及文件名
    profile['dtype'] = 'float32'
    with rasterio.open(out , 'w', **profile) as Sre_write:#写出
        Sre_write.write(data3.astype(profile['dtype']), 1)