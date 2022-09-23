# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 21:15:17 2022

@author: HYF
"""
import pandas as pd
path = r'C:\Users\HYF\OneDrive\文档\WeChat Files\wxid_yv6px43krvoq22\FileStorage\File\2022-09\PRCP_2005.txt'

op = pd.read_csv(path,sep='\s+',header=0,index_col=0)