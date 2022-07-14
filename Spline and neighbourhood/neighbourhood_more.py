# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 17:52:05 2022

@author: HYF
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os,sys,glob
from osgeo import osr,ogr
from osgeo import gdal
from tkinter import _flatten
import time

def SampleRaster(tifList, ptShp, siteName, nirCellNum=1, Scope=''):
    '''
    Using PtShp File to Sample Raster
    :param tifList: 栅格列表
    :param ptShp: 点shp文件
    :param siteName: 点字段名称
    :param nirCellNum: 方格大小，取像元附近均值（只能奇数）；默认值为1，为像元本身
    :param Scope: 筛选范围，eg：“>0” or ""
    :return: 
    '''
    driver = ogr.GetDriverByName('ESRI Shapefile')  #创建驱动
    ds = driver.Open(ptShp, 0)       # 数据驱动driver的open()方法返回一个数据源对象 0是只读，1是可写

    if ds is None:
        print('打开矢量文件失败')
        sys.exit(1)
    else:
        print('打开矢量文件成功')
        

    layer = ds.GetLayer(0)    # 读取数据层，一般ESRI的shapefile都是填0的，如果不填的话默认也是0.
    # 要素个数(属性表行)

    # 存放每个点的xy坐标的数组
    xValues = []
    yValues = []
    # 存放点“区站号”
    station_list = []

    layer.ResetReading()      # 重置遍历对象（所有要素）的索引位置，以便读取
    for i in range(layer.GetFeatureCount()):       #获取矢量的数量
        feature = layer.GetFeature(i)         #获取每个要素
        geometry = feature.GetGeometryRef()   #获取要素的坐标
        x = geometry.GetX()   #  获取经度
        y = geometry.GetY()  #获取纬度
        # 将要分类的点的坐标和点的类型添加
        xValues.append(x)
        yValues.append(y)
        # 读取矢量对应”区站号“字段的值
        station = feature.GetField(siteName)   
        print(f'----矢量数据中第{i}个要素的名称为；{station}----')
        station_list.append(station)

    # 创建二维空列表
    
    result = []
    '''循环每个栅格数据'''
    for tif_i, tif in enumerate(tifList): 
        dr = gdal.Open(tif)
        if dr is None:
           print('Could not open ' + tif)
           sys.exit(1)
        print(f'Reading Data is {tif}' )
        # 存储着栅格数据集的地理坐标信息
        # Sample
        stations = []
        '''循环每个站点数据'''
        for i in range(len(station_list)):
            # LonLat to ColRow
            #print('i:',i)
            [x,y] = lonlat2imagexy(dr,xValues[i],yValues[i])
            print(f'经度: {xValues[i]}',f'纬度 : {yValues[i]}')
            print(f'列号：{x}',f'行号：{y}')
            if np.isnan(x) or np.isnan(y):
                print(f'有问题的经度为：{xValues[i]}')
                print(f'有问题的纬度为：{yValues[i]}')
                continue
            # 判断方框滤波
            if nirCellNum==1:
                dt = dr.ReadAsArray(int(x), int(y), 1, 1)[0][0]   #获取对应点
            elif nirCellNum%2==0:
                print('nirCellNum：The box image element is set incorrectly and must be an odd number')
                break
            else:
                dt = dr.ReadAsArray(int(x-(nirCellNum-1)/2), int(y-(nirCellNum-1)/2), nirCellNum, nirCellNum)  #获取邻域
                #print(dt)
            if dt is None:
                continue
            stations.append(list(dt.flatten()))   #将站点数据进行合并
        result.append(stations)   #将每张栅格上的站点数据进行合并     
    return result,station_list

def getSRSPair(dataset):
    '''
    得到给定数据的投影参考系和地理参考系
    :param dataset: GDAL地理数据
    :return: 投影参考系和地理参考系
    '''
    prosrs = osr.SpatialReference()
    prosrs.ImportFromWkt(dataset.GetProjection())
    geosrs = prosrs.CloneGeogCS()
    return prosrs, geosrs

def geo2lonlat(dataset, x, y):
    '''
    将投影坐标转为经纬度坐标（具体的投影坐标系由给定数据肯定）
    :param dataset: GDAL地理数据
    :param x: 投影坐标x
    :param y: 投影坐标y
    :return: 投影坐标(x, y)对应的经纬度坐标(lon, lat)
    '''
    prosrs, geosrs = getSRSPair(dataset)
    ct = osr.CoordinateTransformation(prosrs, geosrs)
    coords = ct.TransformPoint(x, y)
    return coords[:2] #关于coords = ct.TransformPoint(px,py)的介绍:coords是一个Tuple类型的变量包含3个元素，coords[0]为纬度，coords[1]为经度，coords[2]为高度

def lonlat2geo(dataset, lon, lat):
    '''
    将经纬度坐标转为投影坐标（具体的投影坐标系由给定数据肯定）
    :param dataset: GDAL地理数据
    :param lon: 地理坐标lon经度
    :param lat: 地理坐标lat纬度
    :return: 经纬度坐标(lon, lat)对应的投影坐标
    '''
    prosrs, geosrs = getSRSPair(dataset)
    ct = osr.CoordinateTransformation(geosrs, prosrs)
    coords = ct.TransformPoint(lon, lat)
    return coords[:2]

def imagexy2geo(dataset, row, col):
    '''
    根据GDAL的六参数模型将影像图上坐标（行列号）转为投影坐标或地理坐标（根据具体数据的坐标系统转换）
    :param dataset: GDAL地理数据
    :param row: 像素的行号
    :param col: 像素的列号
    :return: 行列号(row, col)对应的投影坐标或地理坐标(x, y)
    '''
    trans = dataset.GetGeoTransform()
    px = trans[0] + col * trans[1] + row * trans[2]
    py = trans[3] + col * trans[4] + row * trans[5]
    return px, py

def geo2imagexy(dataset, x, y):
    '''
    根据GDAL的六 参数模型将给定的投影或地理坐标转为影像图上坐标（行列号）
    :param dataset: GDAL地理数据
    :param x: 投影或地理坐标x
    :param y: 投影或地理坐标y
    :return: 影坐标或地理坐标(x, y)对应的影像图上行列号(row, col)
    '''
    trans = dataset.GetGeoTransform()
    a = np.array([[trans[1], trans[2]], [trans[4], trans[5]]])
    b = np.array([x - trans[0], y - trans[3]])
    return np.linalg.solve(a, b)  # 使用numpy的linalg.solve进行二元一次方程的求解

def lonlat2imagexy(dataset, lon, lat):
    '''
    将经纬度坐标转为投影坐标（具体的投影坐标系由给定数据确定）
    :param dataset: GDAL地理数据
    :param lon: 地理坐标lon经度
    :param lat: 地理坐标lat纬度
    :return: 投影坐标或地理坐标(x, y)对应的影像图上行列号(row, col)
    '''
    # lonlat2geo
    prosrs, geosrs = getSRSPair(dataset)
    ct = osr.CoordinateTransformation(geosrs, prosrs)
    x = ct.TransformPoint(lat,lon)[0]
    y = ct.TransformPoint(lat, lon)[1]
    # geo2imagexy
    trans = dataset.GetGeoTransform()
    a = np.array([[trans[1], trans[2]], [trans[4], trans[5]]])
    b = np.array([x - trans[0], y - trans[3]])
    return np.linalg.solve(a, b)

outpath = r"F:\CarbonReport\Table"

station_inpath = r'F:\CarbonReport\Data\Station\站点2.shp'    #矢量数据

datas = glob.glob(r'F:\CarbonReport\Data\lucc2010_1km_ChinaCover.tif' )   #栅格数据

replace_dict = {0:"水体",1:"常绿针叶林",2:"常绿阔叶林",3:"落叶针叶林",4:'落叶阔叶林',5:'针阔混交林',6:"灌丛",7:"草地",8:"农作物",9:"人工表面",10:"湿地",11:"其它"}

scale = 3

da,stations = SampleRaster(datas,station_inpath,'Site',nirCellNum=3)

if len(da) ==1:
    da_ = list(_flatten(da[0]))
    new_lists =[replace_dict[i] if i in replace_dict else i for i in da_] 
    c = pd.DataFrame(np.array(new_lists).reshape(-1,scale**2)) 
    c.index = stations
    c.to_excel(outpath + os.sep   + '生态系统类型.xlsx')
else:
    for l in range(len(da)):
        da_ = list(_flatten(da[l]))
        new_lists =[replace_dict[i] if i in replace_dict else i for i in da_]
        c = pd.DataFrame(np.array(new_lists).reshape(-1,scale**2)) 
        c.index = stations
        c.to_excel(outpath + os.sep + str(l) + '生态系统类型.xlsx')






        

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    