# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 22:11:48 2021

@author: 树风
"""
import numpy as np
import pandas as pd
#1    反转列表本身
testList = [1, 3, 5]
testList.reverse()
print(testList)

#2     在循环中迭代时反转
for element in reversed([1,3,5]): print(element)

#3     反转一个字符串
print("Test Python"[::-1])

#4     使用切片反转列表
[1, 3, 5][::-1]

#5      使用枚举器，在循环中很容易找到索引
testlist = [10, 20, 30]
for i, value in enumerate(testlist):
	print(i, ': ', value)
    
#6      在 Python 中使用枚举。
class Shapes:
	Circle, Square, Triangle, Quadrangle = range(4)
print(Shapes.Circle)
print(Shapes.Square)
print(Shapes.Triangle)
print(Shapes.Quadrangle)

#7      使用 splat 运算符解包函数参数
def test(x, y, z):
	print(x, y, z)

testDict = {'x': 1, 'y': 2, 'z': 3} 
testList = [10, 20, 30]
test(*testDict)
test(**testDict)
test(*testList)

#8      使用字典来存储 switch。
stdcalc = {
	'sum': lambda x, y: x + y,
	'subtract': lambda x, y: x - y
}

print(stdcalc['sum'](9,3))
print(stdcalc['subtract'](9,3))

#9      查找列表中出现频率最高的值。
test = [1,2,3,4,2,2,3,1,4,4,4]
print(max(set(test), key=test.count))

#10      检查对象的内存使用情况。
import sys
x=1
print(sys.getsizeof(x))

#11      从两个相关序列创建字典。
t1 = (1, 2, 3)
t2 = (10, 20, 30)

print(dict (zip(t1,t2)))

#12     在线搜索字符串中的多个前缀。
print("http://www.baidu.com".startswith(("http://", "https://")))
print("https://juejin.cn".endswith((".com", ".cn")))

#13     形成一个统一的列表，不使用任何循环。
import itertools
test = [[-1, -2], [30, 40], [25, 35]]
print(list(itertools.chain.from_iterable(test)))

#14         在 Python 中实现真正的 switch-case 语句
def xswitch(x): 
	return xswitch._system_dict.get(x, None) 

xswitch._system_dict = {'files': 10, 'folders': 5, 'devices': 2}

print(xswitch('default'))
print(xswitch('devices'))

#15         就地交换两个数字
x, y = 10, 20
print(x, y)
 
x, y = y, x
print(x, y)

#16        比较运算符的链接。
n = 10 
result = 1 < n < 20 
print(result) 
# True 
result = 1 > n <= 9 
print(result) 
# False

#17       在列表推导式中使用三元运算符。
[m**2 if m > 10 else m**4 for m in range(50)]
#=> [0, 1, 16, 81, 256, 625, 1296, 2401, 4096, 6561, 10000, 121, 144, 169, 196, 225, 256, 289, 324, 361, 400, 441, 484, 529, 576, 625, 676, 729, 784, 841, 900, 961, 1024, 1089, 1156, 1225, 1296, 1369, 1444, 1521, 1600, 1681, 1764, 1849, 1936, 2025, 2116, 2209, 2304, 2401]

#18       将列表元素存储到新变量中
testList = [1,2,3]
x, y, z = testList
print(x, y, z)
#-> 1 2 3

#19        使用交互式“_”运算符
2 + 1
3
#  _
3
print('_')
3

#20        字典/集合理解
#testDict = {i: i * i for i in xrange(10)} 
#testSet = {i * 2 for i in xrange(10)}

#print(testSet)
#print(testDict)

#set([0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
#{0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25, 6: 36, 7: 49, 8: 64, 9: 81}

#21     查看函数含义 
1.'选中函数'   ctrl+i
2.print('函数或库的名字'.__doc__)
3.help('函数或库的名字')










