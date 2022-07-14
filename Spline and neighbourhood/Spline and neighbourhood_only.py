# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 21:14:10 2022

@author: HYF
"""



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os,sys,glob
from osgeo import osr,ogr
from osgeo import gdal
import scipy.interpolate as spi
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

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
    # 数据驱动driver的open()方法返回一个数据源对象 0是只读，1是可写
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds = driver.Open(ptShp, 0)
    if ds is None:
        print('打开矢量文件失败')
        sys.exit(1)
    else:
        print('打开矢量文件成功')
    # 读取数据层
    # 一般ESRI的shapefile都是填0的，如果不填的话默认也是0.
    layer = ds.GetLayer(0)
    # 要素个数(属性表行)
    ptNum = layer.GetFeatureCount()

    # 存放每个点的xy坐标的数组
    xValues = []
    yValues = []
    # 存放点“区站号”
    station_list = []

    # 重置遍历对象（所有要素）的索引位置，以便读取
    layer.ResetReading()
    for i in range(layer.GetFeatureCount()):
        feature = layer.GetFeature(i)
        geometry = feature.GetGeometryRef()
        x = geometry.GetX()
        y = geometry.GetY()
        # 将要分类的点的坐标和点的类型添加
        xValues.append(x)
        yValues.append(y)
        # 读取矢量对应”区站号“字段的值
        station = feature.GetField(siteName)
        station_list.append(station)
    
    # 创建二维空列表
    
    result = []
    '''循环每个栅格数据'''
    for tif, tif_i in zip(tifList, range(len(tifList))):
        # Execute ExtractByMask
        #print(tif)
        # # 打开文件
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
            print(xValues[i],yValues[i])
            [x,y] = lonlat2imagexy(dr,xValues[i],yValues[i])
            #print(xValues[i],yValues[i])
            #print([x,y])
            if np.isnan(x) or np.isnan(y):
                print('有问题的经度为：',xValues[i])
                print('有问题的纬度为：',yValues[i])
                continue
            # 判断方框滤波
            if nirCellNum==1:
                dt = dr.ReadAsArray(int(x), int(y), 1, 1)[0][0]
            elif nirCellNum%2==0:
                print('nirCellNum：The box image element is set incorrectly and must be an odd number')
                break
            else:
                dt = dr.ReadAsArray(int(x-(nirCellNum-1)/2), int(y-(nirCellNum-1)/2), nirCellNum, nirCellNum)
                #print(dt)
            if dt is None:
                continue
            stations.append(list(dt.flatten()))   #将站点数据进行合并
        result.append(stations)   #将每张栅格上的站点数据进行合并     
    return result

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



excel_inpath = r'F:\CarbonReport\Table\通量.xlsx' 
station_inpath = r'F:\CarbonReport\Data\Station\站点2.shp'
data_shp = r'F:\CarbonReport\Data\T'



for dir_ in os.listdir(data_shp):
    print(dir_)
    datas = glob.glob(data_shp + os.sep+ dir_ + os.sep + '*.flt' )
    print(datas)
    
    da = SampleRaster(datas,station_inpath,'Site',nirCellNum=3)
    
    da_ = [c for a in da for b in a for c in b]   #多维列表转一维列表
    
    c = pd.DataFrame()
    
    for i in range(99):
        list_2 = da_[i::9*11]
        #数据准备
        X = np.arange(0,460,1)
        Y = np.array(list_2)
        #定义差值点
        new_x=np.arange(0,460,0.125)
        #进行三次样条拟合
        ipo3=spi.splrep(X,Y,k=3) #样本点导入，生成参数
        iy3=spi.splev(new_x,ipo3) #根据观测点和样条参数，生成插值
        all_ = np.sum(iy3[np.delete(np.arange(3680),np.random.choice(3680, size=80,replace = False))].flatten().reshape(-1,30), axis=1)   #计算
        all_ = pd.DataFrame(all_[12:-12])
        c = pd.concat([c,all_],axis = 1)   #按列进行合
    for i in range(0,c.shape[1],9):
        a = c.iloc[:,i:i+9]
        if dir_ == 'RNPP':
            a = a[::-1]
        a.to_excel(r"F:\CarbonReport\Table\\" + dir_ + str(i) + '.xlsx')
        

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    