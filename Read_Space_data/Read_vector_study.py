# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 10:06:30 2022

@author: HYF
"""
import sys
from osgeo import ogr
import ospybook as pb
import os
from ospybook.vectorplotter import VectorPlotter

'''读取矢量数据'''
driver = ogr.GetDriverByName('ESRI Shapefile')
path = r'F:\MetoGrid\Data\Climate4region\CClimate4Regions.shp'
shp_test = driver.Open(path,0)
if shp_test is None:
    print ('could not open')
    sys.exit(1)
print(shp_test)

'''读取要素个数'''
layer = shp_test.GetLayer()
dir(layer)
n = layer.GetFeatureCount()
print ('feature count:', n)

'''查看属性'''
pb.print_attributes(path,1) #不建议使用这个函数来打印大型数据的全部属性表，可使用数字来控制打印几行并指定打印的字段名。

'''查看图形'''
vp = VectorPlotter(True) #声明图像为交互式图像  ospybook 提供了用于绘图的类。它是基于matplotlib的，所以必须安装matplotlib。

vp.plot(path,fill=False)  #fill是用来控制是否填充要素，默认是true

'''读取四值范围'''
extent = layer.GetExtent() #使用GetExtent方法获得四至信息，结果是一个元组，顺序为左右下上。若shp数据本身含有投影坐标，则输出的也是投影坐标系的值。
print ('extent:', extent)
print ('x range:', extent[0], extent[1])
print ('y range:', extent[2], extent[3])

'''读取单个要素'''
#使用GetFeature方法按照FID读取要素，这里读取的第二个要素，即FID=1的那个要素。
#通过GetField方法可读取要素指定列信息，值得注意的是这里需要输入的列名不分大小写，同shp格式的要求一致。
feat = layer.GetFeature(1)
fid = feat.GetField('id') 
area = feat.GetField('shape_area') 

print (fid)
print (area)
dir(feat)


'''遍历要素'''
#使用GetNextFeature方法可以省去使用For循环按ID读取的低效率；
#要使用个try except机制，不然再最后一个要素读完之后，GetNextFeature方法仍然会读下一个空要素，这时输出面积会报错。
# ResetReading函数是用来复位的，不然下次使用GetNextFeature程序接着上次读的位置继续读。
feat = layer.GetNextFeature()  #读取下一个
while feat:
    feat = layer.GetNextFeature()
    try:
        area = feat.GetField('shape_area') 
        print(area)
    except:
        print('Done!')
layer.ResetReading()  #复位

for i,feat in enumerate(layer):
    if i >= 5:
        break
    x=feat.geometry().GetX()
    y=feat.geometry().GetY()
    fid = feat.ID
    area = feat.GetField('shape_area') 
    print (fid,area,x,y)
layer.ResetReading()  #复位

'''提取要素几何信息'''
# 使用GetGeometryRef方法读取要素几何信息，通过dir函数可以查看geom可以使用的方法；
# GetX和GetY可以直接打印一个个点的坐标；
# 使用geom.Area()可以读feature的面积，默认单位为㎡。

feat = layer.GetFeature(1)
geom = feat.GetGeometryRef()

print(geom)
print(geom.Area())

'''释放内存'''
# 要素.Destory是先关闭单个要素，后面的Destory是关闭整个DataSource；
# 关闭数据源，相当于文件系统操作中的关闭文件。
feat.Destroy()
shp_test.Destroy()

'''删除文件'''
#使用DeleteDataSource可以删除shp文件及其附属文件（如dbf，poj等文件）。

import os
filename = 'F:/Zhihu/DATA/testCopy.shp'
if os.path.exists(filename):
    driver.DeleteDataSource(filename)
    print('File was deleted!')
else:
    print('File not exist')

