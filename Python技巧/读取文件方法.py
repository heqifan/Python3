# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 09:57:02 2021

@author: 树风
"""

# =============================================================================
获取文件路径
# 最常用的就是   glob.glob()
# 1.支持通配符操作: ?代表1个字符进行模糊     
#                *代表多个字符进行模糊     
#                []代表匹配指定范围内的字符
# 2.获取的是当前文件夹下的绝对路径，不会到子目录下
# =============================================================================
               


# =============================================================================
拆分文件路径的文件名，后缀名等,常常和   glob.glob 一起用
# 1.split():str.split(str="", num=string.count(str))
# str -- 分隔符  默认为所有的空字符，包括空格、换行(\n)、制表符(\t)等
# num -- 分割次数
# samples:
# '/home/ubuntu/python/example.py'.split('/')  # 分裂
# ['', 'home', 'ubuntu', 'python', 'example.py']
#  
# '/home/ubuntu/python/example.py'.split('/', 1)  # 只分裂一次
# ['', 'home/ubuntu/python/example.py']
# 
# 2.os.path.split()
# 函数将文件路径和文件名分开
# os.path.split('/home/ubuntu/python/example.py')
# ('/home/ubuntu/python', 'example.py')
# 
# 3.os.path.splitext()
# 函数将文件名和扩展名分开
# os.path.splitext('/home/ubuntu/python/example.py')
# ('/home/ubuntu/python/example', '.py')
# =============================================================================

# =============================================================================
字符串和数字的格式化
# 1.   简单的有      f"{}+'字符串'+{}+'字符串' " 
#         或者用     str()
# 2    复杂的有     str.format()
# >>>"{} {}".format("hello", "world")    # 不设置指定位置，按默认顺序
# 'hello world'
#  
# >>> "{0} {1}".format("hello", "world")  # 设置指定位置
# 'hello world'
#  
# >>> "{1} {0} {1}".format("hello", "world")  # 设置指定位置
# 'world hello world'
# 
# print("网站名：{name}, 地址 {url}".format(name="菜鸟教程", url="www.runoob.com"))
#  
# # 通过字典设置参数
# site = {"name": "菜鸟教程", "url": "www.runoob.com"}
# print("网站名：{name}, 地址 {url}".format(**site))
#  
# # 通过列表索引设置参数
# my_list = ['菜鸟教程', 'www.runoob.com']
# print("网站名：{0[0]}, 地址 {0[1]}".format(my_list))  # "0" 是必须的
# 
# 也可以向 str.format() 传入对象：
# class AssignValue(object):
#     def __init__(self, value):
#         self.value = value
# my_value = AssignValue(6)
# print('value 为: {0.value}'.format(my_value))  # "0" 是可选的
# 3.数字的格式化
# print("{:.2f}".format(3.1415926))
# 
# =============================================================================



