# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 11:59:47 2022

@author: HYF
"""


import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os,sys,glob
from osgeo import osr,ogr,gdal

sample_tif = r'E:\陈星师姐\3\Regions10_qhai01.tif'

def Get_tif_xy(Sample_tif):
    '''
    Args: 
    input:
        Sample_tif:  输入的tif数据的路径
    return:
        arr_x:   tif数据中像元对应的经度的数组
        arr_y:   tif数据中像元对应的纬度的数组
        nXSize： tif数据的列数
        nYSize： tif数据的行数
    '''
    
    dataset = gdal.Open(Sample_tif)  # 打开tif
    
    adfGeoTransform = dataset.GetGeoTransform()  # 读取地理信息
    
    # 左上角地理坐标
    print('左上角x地理坐标：',adfGeoTransform[0])
    print('左上角y地理坐标：',adfGeoTransform[3])
    
    nXSize = dataset.RasterXSize  # 列数
    nYSize = dataset.RasterYSize  # 行数
    
    print('列数为：',nXSize, '行数为：',nYSize)
    
    arr_x = []  # 用于存储每个像素的（X，Y）坐标
    arr_y = []
    for i in range(nYSize):
        row_x = []
        row_y = []
        for j in range(nXSize):
            px = adfGeoTransform[0] + j * adfGeoTransform[1] + i * adfGeoTransform[2]
            py = adfGeoTransform[3] + j * adfGeoTransform[4] + i * adfGeoTransform[5]
            row_x.append(px)
            row_y.append(py)
        arr_x.append(row_x)
        arr_y.append(row_y)
        
    return arr_x,arr_y,nXSize,nYSize


def read_img(filename):
    '''
    Args:
    input:
        filename: 输入的tif数据的路径
    output:
        im_data: tif数据对应的数组
    '''
    dataset=gdal.Open(filename)       #打开文件
 
    im_width = dataset.RasterXSize    #栅格矩阵的列数
    im_height = dataset.RasterYSize   #栅格矩阵的行数
 
    im_geotrans = dataset.GetGeoTransform()  #仿射矩阵
    im_proj = dataset.GetProjection() #地图投影信息
    im_data = dataset.ReadAsArray(0,0,im_width,im_height) #将数据写成数组，对应栅格矩阵
 
    del dataset 
    return im_data


x,y,col,line = Get_tif_xy(sample_tif)
Region_x_array,Region_y_array = np.array(x).flatten(),np.array(y).flatten()  #将存放经纬度的二维列表转为一维数组
Region_x_y_array = pd.DataFrame(np.array([Region_y_array,Region_x_array]).T)   #将两个一维数组合并并倒置转为数据框
Region_data = read_img(sample_tif)    #读取tif数据的值
Region_x_y_array['Region_value'] = Region_data.flatten()   #添加一列值
# Region_x_y_array[0] = round(Region_x_y_array[0],2)
Region_x_y_array[0] = Region_x_y_array[0].apply(lambda x:"%.1f"%x)
Region_x_y_array[1] = round(Region_x_y_array[1],1)
Region_x_y_array = Region_x_y_array[Region_x_y_array['Region_value']!=15]
Region_x_y_array[[0,1]].to_csv(r'E:\陈星师姐\3\\' + 'out.csv',index = False,header=None)
