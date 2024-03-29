# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 15:46:13 2022

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

Input_folder = r''

if Input_folder == '':
    Input_folder = input('请输入文件夹名称：(Sample: F:\\MsTMIP\\NPP or F:/MsTMIP/NPP )——————————————')
    

End_name  = r''
if End_name == '':
    End_name = input('请输入文件的后缀：(Sample: nc4)——————————————')

band_start = 9999
Filldata = 99999
band_end = 9999

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
    global band_loc
    global band_start
    global band_end
    coord = 4326            #坐标系，["EPSG","4326"]，默认为4326
    nc_data_obj = nc.Dataset(data)
    key = list(nc_data_obj.variables.keys())            #获取时间，经度，纬度，波段的名称信息，这些可能是不一样的
    lon_loc = [i for i,x in enumerate(key) if (x.find('lon'.upper())!=-1 or x.find('lon'.lower())!=-1)][0]   #模糊查找属于经度的名称
    lat_loc = [i for i,x in enumerate(key) if (x.find('lat'.upper())!=-1 or x.find('lat'.lower())!=-1)][0]   #模糊查找属于纬度的名称
    print(f'{data} 的所有波段信息为————————：{key}')
    if band_start == 9999: 
        band_start = eval(input(f"请在指定范围内 1~{len(key)} 输入您想要输出的多个波段的开始序号(int): "))   
    if band_end == 9999:
        band_end = eval(input(f"请在指定范围内 1~{len(key)} 输入您想要输出的多个波段的结束序号(int)(如果你只有一个波段想要输出的话结束序号就与开始序号相同): ")) 
        if band_end > len(key):
            print('结束序号不在指定范围内')
            return 0
    for band_var in key[band_start-1:band_end]: 
        key_lon = key[lon_loc]              #获取经度的名称   
        key_lat = key[lat_loc]              #获取纬度的名称  
        Lon = nc_data_obj.variables[key_lon][:]   #获取每个像元的经度
        Lat = nc_data_obj.variables[key_lat][:]    #获取每个像元的纬度
        band = np.asarray(nc_data_obj.variables[band_var]).astype(float)  #获取对应波段的像元的值，类型为数组
        global Filldata
        if Filldata == 99999:   #获取从用户那获取填充值
            print("请查看你的填充值：",nc_data_obj.variables[band_var])
            Filldata =  eval(input("请输入您刚刚查看的填充值：——————————"))
        #影像的四个角的坐标
        LonMin,LatMax,LonMax,LatMin = [Lon.min(),Lat.max(),Lon.max(),Lat.min()] 
        #分辨率计算
        N_Lat = len(Lat) 
        if Lon.ndim==1 :
            N_Lon = len(Lon)   #如果Lon为一维的话，就取长度
        else:         
            N_Lon = len(Lon[0])   #如果Lon为二维的话，就取宽度
        Lon_Res = (LonMax - LonMin) /(float(N_Lon)-1)
        Lat_Res = (LatMax - LatMin) / (float(N_Lat)-1)
        
        #创建.tif文件
        ndim = band.ndim

        if ndim == 4 :
            print(f'正在处理的数据为：{data}')
            print(f'正在处理的波段为：{band_var}')
            print('{band_var}波段维度为：4')
            ndim_4_1_start = eval(input("请输入您在第一维度上开始时间，如果是xxxx年的话就输入xxxx比如2000：——————————"))
            step_4_1 = eval(input("请输入您在第一维度上时间的步长，如果是每隔x年的话就输入x比如5：——————————"))
            ndim_4_2_start = eval(input("请输入您在第二维度上开始时间，如果是x月的话就输入x比如1：——————————"))
            step_4_2 = eval(input("请输入您在第二维度上时间的步长，如果是每隔x月的话就输入x比如6：——————————"))
            for i in range(band.shape[0]):
                for j in range(band.shape[1]):
                    driver = gdal.GetDriverByName('GTiff')   # 创建驱动          
                    arr1 = band[i,j,:,:]               # 获取不同时间段的数据
                    out_tif_name = Output_folder + os.sep + data.split('\\')[-1][:-4] + '_' + band_var + '_' + str(ndim_4_1_start) + \
                                    '_' + str(ndim_4_2_start) + '.tif'
                    out_tif = driver.Create(out_tif_name,N_Lon,N_Lat,1,gdal.GDT_Float32) 
                    # 设置影像的显示范围
                    #-Lat_Res一定要是-的
                    geotransform = (LonMin, Lon_Res, 0, LatMax, 0, -Lat_Res)
                    out_tif.SetGeoTransform(geotransform)
                    srs = osr.SpatialReference()
                    srs.ImportFromEPSG(4326)
                    out_tif.SetProjection(srs.ExportToWkt())
                    

                    if Lat[0]<=Lat[-1]:   #如果维度上的第一个值小于等于最后的的一个值就认为是倒序，就得进行数组的倒序排列，否则就是正向，不用倒序排列
                        print(f'{data}行数据是倒的，现在进行矫正............')
                        arr1 = arr1[::-1]
                        print('矫正完成...........')
                    else:
                        pass
                    # a = a*scale+add_offset
                    out_tif.GetRasterBand(1).WriteArray(arr1)   #写入数据
                    out_tif.GetRasterBand(1).SetNoDataValue(Filldata)   #设置输出数据的无效值
                    out_tif.FlushCache() # 将数据写入硬盘
                    print(f'{out_tif_name} is ok!!!!')
                    del out_tif       # 注意必须关闭tif文件
                    ndim_4_2_start += step_4_2
                ndim_4_1_start += step_4_1
      
        if ndim == 3 :
            print(f'正在处理的数据为：{data}')
            print(f'正在处理的波段为：{band_var}')
            print('{band_var}波段维度为：3')
            ndim_3_1_start = eval(input("请输入您在第一维度上开始时间，如果是xxxx年的话就输入xxxx比如2000：——————————"))
            step_3_1 = eval(input("请输入您在第一维度上时间的步长，如果是每隔x年的话就输入x比如5：——————————"))
            for i in range(band.shape[0]):
                driver = gdal.GetDriverByName('GTiff')   # 创建驱动          
                arr1 = band[i,:,:]               # 获取不同时间段的数据
                out_tif_name = Output_folder + os.sep + data.split('\\')[-1][:-4] + '_' + band_var + '_' + str(ndim_3_1_start) +  '.tif'
                out_tif = driver.Create(out_tif_name,N_Lon,N_Lat,1,gdal.GDT_Float32) 
                # 设置影像的显示范围
                #-Lat_Res一定要是-的
                geotransform = (LonMin, Lon_Res, 0, LatMax, 0, -Lat_Res)
                out_tif.SetGeoTransform(geotransform)
                srs = osr.SpatialReference()
                srs.ImportFromEPSG(4326)
                out_tif.SetProjection(srs.ExportToWkt())
                

                if Lat[0]<=Lat[-1]:   #如果维度上的第一个值小于等于最后的的一个值就认为是倒序，就得进行数组的倒序排列，否则就是正向，不用倒序排列
                    print(f'{data}行数据是倒的，现在进行矫正............')
                    arr1 = arr1[::-1]
                    print('矫正完成...........')
                else:
                    pass
                # a = a*scale+add_offset
                out_tif.GetRasterBand(1).WriteArray(arr1)   #写入数据
                out_tif.GetRasterBand(1).SetNoDataValue(Filldata)   #设置输出数据的无效值
                out_tif.FlushCache() # 将数据写入硬盘
                print(f'{out_tif_name} is ok!!!!')
                del out_tif       # 注意必须关闭tif文件
                ndim_3_1_start += step_3_1
                
        if ndim == 2 :
            print(f'正在处理的数据为：{data}')
            print(f'正在处理的波段为：{band_var}')
            print('{band_var}波段维度为：2')
            driver = gdal.GetDriverByName('GTiff')   # 创建驱动          
            arr1 = band[:,:]               # 获取不同时间段的数据
            out_tif_name = Output_folder + os.sep + data.split('\\')[-1][:-4] + '_' + band_var + '.tif'
            out_tif = driver.Create(out_tif_name,N_Lon,N_Lat,1,gdal.GDT_Float32) 
            # 设置影像的显示范围
            #-Lat_Res一定要是-的
            geotransform = (LonMin, Lon_Res, 0, LatMax, 0, -Lat_Res)
            out_tif.SetGeoTransform(geotransform)
            srs = osr.SpatialReference()
            srs.ImportFromEPSG(4326)
            out_tif.SetProjection(srs.ExportToWkt())
            
            if Lat[0]<=Lat[-1]:   #如果维度上的第一个值小于等于最后的的一个值就认为是倒序，就得进行数组的倒序排列，否则就是正向，不用倒序排列
                print(f'{data}行数据是倒的，现在进行矫正............')
                arr1 = arr1[::-1]
                print('矫正完成...........')
            else:
                pass
            # a = a*scale+add_offset
            out_tif.GetRasterBand(1).WriteArray(arr1)   #写入数据
            out_tif.GetRasterBand(1).SetNoDataValue(Filldata)   #设置输出数据的无效值
            out_tif.FlushCache() # 将数据写入硬盘
            print(f'{out_tif_name} is ok!!!!')
            del out_tif       # 注意必须关闭tif文件
    return 1



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
        print('输入文件夹————%s——————不存在！！！' % Input_folder)
        return 0
    else:   
        # 读取所有nc数据
        data_list = glob.glob(Input_folder + os.sep + '*' + End_name)
        for i in range(len(data_list)):
            dat = data_list[i]
            Output_folder = os.path.split(Input_folder)[0]  + os.sep+ 'out_' + os.path.split(Input_folder)[-1] + os.sep + dat.split('\\')[-1][:-3]  
            print("输出位置为: ",Output_folder)
            # if os.path.exists(Output_folder):
            #     shutil.rmtree(Output_folder)          #如果文件夹存在就删除
            # os.makedirs(Output_folder)            #再重建，这样就不用运行之后又要删了之后再运行了，可以一直运行
            re = NC_to_tiffs(dat,Output_folder)
            if re==1:
                print (dat + '----转tif成功')
            else:
                pass
        print(f'输出位置为: {Output_folder}')
    return 1
    

re = nc_to_tif(Input_folder)   #用户需要输入 ：nc文件所放的文件夹的路径，默认输出至同级目录中，名为'out_...'

