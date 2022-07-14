# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 09:28:38 2021

@author: 树风
"""

import re
import numpy as np
import netCDF4 as nc
from osgeo import gdal,osr
import glob
import os
import shutil

band_name = ''

def NC_to_tiffs(data,out_path,start_year):
    '''
    这个函数里面有些地方还是可能需要更改,像：
    coord(坐标系)
    '''
    coord = 4326            #坐标系，["EPSG","4326"]，默认为4326
    nc_data_obj = nc.Dataset(data)
    print(f'nc_data_obj:{nc_data_obj}')               # 了解nc的数据类型
    #print(nc_data_obj.variables)                     #了解nc数据的基本信息
    key=list(nc_data_obj.variables.keys())            #获取时间，经度，纬度，波段的名称信息，这些可能是不一样的
    
    print(f'基础属性为  :{key}')
    lon_size = [i for i,x in enumerate(key) if (x.find('lon'.upper())!=-1 or x.find('lon'.lower())!=-1)][0]   #模糊查找属于经度的名称
    lat_size = [i for i,x in enumerate(key) if (x.find('lat'.upper())!=-1 or x.find('lat'.lower())!=-1)][0]   #模糊查找属于纬度的名称
    time_size = [i for i,x in enumerate(key) if (x.find('ime'.upper())!=-1 or x.find('ime'.lower())!=-1)][0]  #模糊查找属于时间的名称
    
    global band_name
    
    if band_name == '':
        band_name = input("请输入您想要输出的波段的名字（您可以从'基础属性中得来',不用加上引号）———————:")   #这里是从用户那传入一个波段的字符串，因为nc4的数据比nc要复杂，所以要让用户确定波段的名字
    band_size = [i for i,x in enumerate(key) if (x.find(str(band_name).upper())!=-1 or x.find(str(band_name).lower())!=-1)][0]
    
    key_band = key[band_size]            #获取波段的名称     
    time_name = key[time_size]         #获取时间的名称
    key_lon = key[lon_size]        #获取经度的名称   
    key_lat = key[lat_size]      #获取纬度的名称  
    unit = nc_data_obj.variables[key_band].unit
    unit = float(re.findall(r"\d+\.?\d*",unit)[0])
    
    print(f'波段的基本属性  :{nc_data_obj.variables[key_band]}')
    
    print(f'unit  :{unit}')
    
    
    print(f'获取波段的名称  :{key_band}')
    print(f'获取时间的名称  :{time_name}')
    print(f'获取经度的名称  :{key_lon}')
    print(f'获取纬度的名称  :{key_lat}')
    
    Lon = nc_data_obj.variables[key_lon][:]   #获取每个像元的经度
    Lat = nc_data_obj.variables[key_lat][:]    #获取每个像元的纬度
    time = nc_data_obj.variables[time_name][:]
    
    print(f'time  :{time}')
    #times = nc.num2date(time[:],time.units)  # 时间的格式转换,得到一个数组
    #times = np.array(nc.num2date(time[:],time[:].units))
    
    print(f'获取每个像元的经度  :{Lon}')
    print(f'获取每个像元的纬度  :{Lat}')
    
    band = np.asarray(nc_data_obj.variables[key_band]).astype(float)  #获取对应波段的像元的值，类型为数组
    
    print(f"填充值：{float(nc_data_obj.variables[key_band].missing_value)}")
    
    #影像的四个角的坐标
    LonMin,LatMax,LonMax,LatMin = [Lon.min(),Lat.max(),Lon.max(),Lat.min()] 
    
    #分辨率计算
    N_Lat = len(Lat) 
    if Lon.ndim==1 :   #如果Lon维度为1的话：
        N_Lon = len(Lon)   #获取长度
    else:    #如果Lon维度为2的话
        N_Lon = len(Lon[0])
    
    print(f'len(Lat)  :{N_Lat}' )
    print(f'len(N_Lon)  :{N_Lon}')
    
    Lon_Res = (LonMax - LonMin) /(float(N_Lon)-1)
    Lat_Res = (LatMax - LatMin) / (float(N_Lat)-1)
    
    print(f'Lon_Res  :{Lon_Res}')
    print(f'Lat_Res  :{Lat_Res}')
    
    #创建.tif文件
    band_shape  = band.shape[0]
    print(f'band.shape[0]  :{band.shape[0]}')
    
    for i in range(band_shape):
        print('i --------:',i)
        driver = gdal.GetDriverByName('GTiff')   # 创建驱动      
        
        arr1 = band[i,:,:]                   # 获取不同时间段的数据
        out_tif_name = out_path + os.sep + str(key_band) + '_' + str(start_year) + '_' + str(i+1)+'.tif'
        print(f'输出的tis数据名:{out_tif_name}')
        out_tif = driver.Create(out_tif_name,N_Lon,N_Lat,1,gdal.GDT_Float32) 
         
        # 设置影像的显示范围
        #-Lat_Res一定要是-的
        geotransform = (LonMin, Lon_Res, 0, LatMax, 0, -Lat_Res)
        out_tif.SetGeoTransform(geotransform)
            
        #获取地理坐标系统信息，用于选取需要的地理坐标系统
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(coord)                       # 定义输出的坐标系为"WGS 84"，AUTHORITY["EPSG","4326"]
        out_tif.SetProjection(srs.ExportToWkt())               # 给新建图层赋予投影信息
        #print(f'乘以比例因子之前的arr1：{arr1}')
        
        arr1  = arr1 * unit
        
       
        #更改异常值    
        arr1[arr1[:, :]< -1000] = float(nc_data_obj.variables[key_band].missing_value)
        
        #print(f'乘以比例因子之后的arr1：{arr1}')
        #数据写出
        if arr1.ndim==2:     #如果本来就是二维数组就不变
            a = arr1[:,:]   
        else:     #将三维数组转为二维
            a = arr1[0,:,:]    

        #a = a[::-1]        #这里是需要倒置一下的     横重要的！！！！！！！！！！！
        out_tif.GetRasterBand(1).WriteArray(a)
        out_tif.GetRasterBand(1).SetNoDataValue(float(nc_data_obj.variables[key_band].missing_value))
        out_tif.FlushCache() # 将数据写入硬盘
        del out_tif       # 注意必须关闭tif文件
        
        if (i+1)%12==0:
            start_year+=1
        
        
def nc_to_tif(Input_folder):
    Output_folder = Input_folder +  '_out' 
    print(f'输出文件夹为:{Output_folder}')
    # 读取所有nc数据
    data_list = glob.glob(Input_folder + os.sep + '*.nc' )
    print(f"输入位置为: {Input_folder}")
    print(f"被读取的nc文件有：{data_list}")
    if os.path.exists(Output_folder):
        shutil.rmtree(Output_folder)          #如果文件夹存在就删除
    os.makedirs(Output_folder)            #再重建，这样就不用运行之后又要删了之后再运行了
    for i in range(len(data_list)):
        dat = data_list[i]
        print('dat.split("\\")[-1]:',dat.split('\\')[-1])
        start_year = int(dat.split('\\')[-1].split('.')[0].split('_')[1])
        print(f'开始年份:{start_year}')
        NC_to_tiffs(dat,Output_folder,start_year)
        print (f'{dat}-----转tif成功')
    print(f"输入位置为: {Input_folder}")
    print(f'输出位置为: { Output_folder}')
        
     
nc_to_tif(Input_folder = r'C:\Users\Administrator\Documents\WeChat Files\wxid_yv6px43krvoq22\FileStorage\File\2022-04')   #用户需要输入 ：nc文件所放的文件夹的路径，默认输出至同一上级目录中    





