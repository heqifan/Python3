# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 15:46:13 2022

@author: HYF
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 21:08:43 2022

@author: HYF
"""

import numpy as np
import netCDF4 as nc
from osgeo import gdal,osr,ogr
import glob
import os
import shutil
#import win32ui

import os
os.environ['PROJ_LIB'] = r'D:\Software\anaconda\Library\share\proj'
os.environ['GDAL_DATA'] = r'D:\Software\anaconda\Library\share'


'''
需要更换的变量名为：
Input_folder：  输入的文件夹路径，要么更改要么不填
styear：   开始年份，要么更改要么不填
End_name：  数据后缀
其它不用变
'''

#path = win32ui.CreateFileDialog(True)
#path = win32ui.CreateFileDialog(1)

#path.DoModal()
#Input_folder = path.GetPathName()

sample_tif = r'J:\Integrated_analysis_data\Data\Sample\Mask_Mul_2005.tif'
ds = gdal.Open(sample_tif) 
Input_folder = r'J:\netcdf'

if Input_folder == '':
    Input_folder = input('请输入文件夹名称：(Sample: F:\\MsTMIP\\NPP or F:/MsTMIP/NPP )——————————————')
    

End_name ='nc'
if End_name == '':
    End_name = input('请输入文件的后缀：(Sample: nc4)——————————————')

band_start = 9999
Filldata = 99999


def NC_to_tiffs(data,Output_folder):
    
    '''
    Input:
        data: Inputdata's path
        out_path: Outpath
        styear:   Start year name
    Output:
        None
        Example:  nc_to_tif(data = dat,out_path = Output_folder,styear)
    '''
    coord = 4326            #坐标系，["EPSG","4326"]，默认为4326
    nc_data_obj = nc.Dataset(data)
    #print(nc_data_obj,type(nc_data_obj))              # 了解nc的数据类型，<class 'netCDF4._netCDF4.Dataset'>
    #print(nc_data_obj.variables)                      #了解nc数据的基本信息
    key=list(nc_data_obj.variables.keys())            #获取时间，经度，纬度，波段的名称信息，这些可能是不一样的
    lon_loc = [i for i,x in enumerate(key) if (x.find('lon'.upper())!=-1 or x.find('lon'.lower())!=-1)][0]   #模糊查找属于经度的名称
    lat_loc = [i for i,x in enumerate(key) if (x.find('lat'.upper())!=-1 or x.find('lat'.lower())!=-1)][0]   #模糊查找属于纬度的名称
    global band_loc
    print('基础属性为-----',key)
    # if band_loc == 9999:
    #     print('基础属性为-----',key)
    global band_start
    if band_start == 9999:
        band_start = eval(input("请输入您想要输出的多个波段数的开始序号:————————"))   

    for band_var in key[band_start-1:]: 
        # key_band = key[band_loc]            #获取波段的名称     
        key_lon = key[lon_loc]              #获取经度的名称   
        key_lat = key[lat_loc]              #获取纬度的名称  
        Lon = nc_data_obj.variables[key_lon][:]   #获取每个像元的经度
        Lat = nc_data_obj.variables[key_lat][:]    #获取每个像元的纬度
        band = np.asarray(nc_data_obj.variables[band_var]).astype(float)  #获取对应波段的像元的值，类型为数组
        global Filldata
        print("请查看你的填充值：",nc_data_obj.variables[band_var])
        # Filldata = nc_data_obj.variables[key_band].missing_value
        # scale = nc_data_obj.variables[key_band].scale_factor
        # add_offset = nc_data_obj.variables[key_band].add_offset
        if Filldata == 99999:   #获取从用户那获取填充值
            print("请查看你的填充值：",nc_data_obj.variables[band_var])
            Filldata =  eval(input("请输入您刚刚查看的填充值(float)：——————————"))
        #影像的四个角的坐标
        LonMin,LatMax,LonMax,LatMin = [Lon.min(),Lat.max(),Lon.max(),Lat.min()] 
        print("请查看你的填充值：",nc_data_obj.variables[band_var])
        #分辨率计算
        N_Lat = len(Lat) 
        if Lon.ndim==1 :
            N_Lon = len(Lon)   #如果Lon为一维的话，就取长度
        else:         
            N_Lon = len(Lon[0])   #如果Lon为二维的话，就取宽度
        Lon_Res = (LonMax - LonMin) /(float(N_Lon)-1)
        Lat_Res = (LatMax - LatMin) / (float(N_Lat)-1)
        
        if Lat[0]<=Lat[-1]:
            print(f'{data}里面的数据是倒的，现在进行矫正............')
        #创建.tif文件
        print(band.shape[0])
        # print(scale)
        
        for i in range(band.shape[0]):
            driver = gdal.GetDriverByName('GTiff')   # 创建驱动          
            arr1 = band[i,:,:]               # 获取不同时间段的数据
            out_tif_name = Output_folder + os.sep + data.split('\\')[-1][:-4] + '_' + band_var + '_' + str(i) + '.tif'
            out_tif = driver.Create(out_tif_name,N_Lon,N_Lat,1,gdal.GDT_Float32) 
            # 设置影像的显示范围
            #-Lat_Res一定要是-的
            geotransform = (LonMin, Lon_Res, 0, LatMax, 0, -Lat_Res)
            out_tif.SetGeoTransform(geotransform)
            srs = osr.SpatialReference()
            srs.ImportFromEPSG(4326)
            out_tif.SetProjection(srs.ExportToWkt())
                
            #获取地理坐标系统信息，用于选取需要的地理坐标系统
            # srs = osr.SpatialReference()
            
            # srs.ImportFromEPSG(coord)                               # 定义输出的坐标系为"WGS 84"，AUTHORITY["EPSG","4326"]             # 给新建图层赋予投影信息
                
            #更改异常值    
            #arr1[arr1[:, :]< 1000000] = -32767
            
            #数据写出
            if arr1.ndim==2:     #如果本来就是二维数组就不变
                a = arr1[:,:]   
            else:                #将三维数组转为二维
                a = arr1[0,:,:]  
            if Lat[0]<=Lat[-1]:   #如果维度上的第一个值小于等于最后的的一个值就认为是倒序，就得进行数组的倒序排列，否则就是正向，不用倒序排列
                a=a[::-1]
                print('矫正完成...........')
            else:
                pass
            # a = a*scale+add_offset
            out_tif.GetRasterBand(1).WriteArray(a)   #写入数据
            out_tif.GetRasterBand(1).SetNoDataValue(Filldata)   #设置输出数据的无效值
            out_tif.FlushCache() # 将数据写入硬盘
            print(f'{i} is ok!!!!')
            del out_tif       # 注意必须关闭tif文件
    print('ALL is ok !!!!!')



def nc_to_tif(Input_folder:str):
    
    '''
    Input:
        Input_folder: Inputdata's File Path
        End_name: Data's suffix name
        styear:   Start year name
    Output:
        status： 1成功 0不成功
        Example:  nc_to_tif(Input_folder = r'F:\\MsTMIP\\NPP',End_name='nc4',1990)
    '''
    
    if not os.path.exists(Input_folder):       #判断原始文件路劲是否存在,如果不存在就直接退出
        print('The deldir is not exist:%s' % Input_folder)
        status = 0
    else:   
        # 读取所有nc数据
        data_list = glob.glob(Input_folder + os.sep + '*' + End_name)
        print("被读取的nc文件有：",data_list)
        for i in range(len(data_list)):
            dat = data_list[i]
            Output_folder = os.path.split(Input_folder)[0]  + os.sep+ 'out_' + os.path.split(Input_folder)[-1] + os.sep + dat.split('\\')[-1][:-3]  
            print("输出位置为: ",Output_folder)
            if os.path.exists(Output_folder):
                shutil.rmtree(Output_folder)          #如果文件夹存在就删除
            os.makedirs(Output_folder)            #再重建，这样就不用运行之后又要删了之后再运行了，可以一直运行
            NC_to_tiffs(dat,Output_folder)
            print (dat + '----转tif成功')
        print(f"输入位置为: {Input_folder}")
        print(f'输出位置为: {Output_folder}')
        status = 1
    return status
    
'''如果是以nc为后缀的多时间序列的数据话的话输入路径不能有中文字符----------比如放在D盘中就可以(目前我发现只有有多时间序列的nc文件才会有这个问题，，，)'''    
re = nc_to_tif(Input_folder)   #用户需要输入 ：nc文件所放的文件夹的路径，默认输出至同级目录中，名为'out_...'


print('-------完成--------' if re==1 else '-------输入文件夹不存在--------')
