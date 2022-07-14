
import os,sys,glob,rasterio
from osgeo import osr,ogr
import pandas as pd
from osgeo import gdal, gdalconst
import numpy as np


def flatten(a):
    if not isinstance(a, (list, )):
        return [a]
    else:
        b = []
        for item in a:
            b += flatten(item)
    return b

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
    values = [[0 for col in range(len(tifList))] for row in range(len(station_list))]
    result = []
    for tif, tif_i in zip(tifList, range(len(tifList))):
        # Execute ExtractByMask
        #print(tif)
        # # 打开文件
        dr = gdal.Open(tif)
        # 存储着栅格数据集的地理坐标信息
        transform = dr.GetGeoTransform()
        # Sample
        for i in range(len(station_list)):
            # LonLat to ColRow
            #print('i:',i)
            [x,y] = lonlat2imagexy(dr,xValues[i],yValues[i])
            #print(xValues[i],yValues[i])
            #print([x,y])
            if np.isnan(x) or np.isnan(y):
                print(i)
                print('有问题的经度为：',xValues[i])
                print('有问题的纬度为：',yValues[i])
                continue
            # 判断方框滤波
            if nirCellNum==1:
                dt = dr.ReadAsArray(int(x), int(y), 1, 1)
            elif nirCellNum%2==0:
                print('nirCellNum：The box image element is set incorrectly and must be an odd number')
                break
            else:
                dt = dr.ReadAsArray(int(x-(nirCellNum-1)/2), int(y-(nirCellNum-1)/2), nirCellNum, nirCellNum)
                #print(dt)
                result.append(list(dt.flatten()))
            #valueList = dt.flatten()
            # 判断取值范围
            
            
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




# def Pixel2world(geotransform, line, column):
#     originX = geotransform[0]
#     originY = geotransform[3]
#     pixelWidth = geotransform[1]
#     pixelHeight = geotransform[5]
#     x = column*pixelWidth + originX - pixelWidth/2
#     y = line*pixelHeight + originY - pixelHeight/2
#     return(x,y)

path =  r'E:\Wu'
shp_path = path + os.sep + '站点.shp'

#t_excel_0 = pd.read_excel(path + os.sep + '通量.xlsx',sheet_name=0,header = 0,index_col = 0)

#tation_names = list(t_excel_0['Site'])
#t_Lat_Lng = t_excel_0[['Lat','Lng']].values.tolist()

# for name in tation_names:
#     print(name)
#     t_excel = pd.read_excel(path + os.sep + '通量.xlsx',sheet_name=name,header = 0,index_col = None)
#     print(t_excel)



'''C'''
# c_excel_0 = pd.read_csv(path + os.sep + '储量.CSV',header = 0,index_col = None,encoding='gbk')
# c_excel_0 = c_excel_0.head(1000)
c_data_path  = path + os.sep + 'C' 
# c_Lat_Lng = np.array(c_excel_0[['纬度','经度']]).tolist()
var = ['RVGC']
for v in var:
    result = []
    for year in range(2011,2016):
        print('year',year)
        c_datas = glob.glob(c_data_path + os.sep + '*' + v + '_' + str(year)+'.flt')
        value = SampleRaster(c_datas,shp_path,'样地ID',nirCellNum=3)
        result.append(value)
    result_da = pd.DataFrame(result)
    
    
        #print(result)
        
        
        
        
        