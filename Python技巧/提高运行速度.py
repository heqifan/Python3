# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 09:56:38 2021

@author: 树风
"""

1.并行运算
map():        一定情况下替代了for 循环
    map(function, iterable, ...)
    function -- 函数
    iterable -- 一个或多个序列
    
samples:
def square(x) :            # 计算平方数
... return x ** 2
...
map(square, [1,2,3,4,5])   # 计算列表各个元素的平方
[1, 4, 9, 16, 25]
map(lambda x: x ** 2, [1, 2, 3, 4, 5])  # 使用 lambda 匿名函数
[1, 4, 9, 16, 25]
# 提供了两个列表，对相同位置的列表数据进行相加
map(lambda x, y: x + y, [1, 3, 5, 7, 9], [2, 4, 6, 8, 10])
[3, 7, 11, 15, 19]

zip()              一定情况下可以同时循环多个列表，与map()一起用的话有奇效
    zip([iterable, ...])
    iterabl -- 一个或多个迭代器;
a = [1,2,3]
b = [4,5,6]
c = [4,5,6,7,8]
zipped = zip(a,b)     # 打包为元组的列表
[(1, 4), (2, 5), (3, 6)]
zip(a,c)              # 元素个数与最短的列表一致    
[(1, 4), (2, 5), (3, 6)]
zip(*zipped)          # 与 zip 相反，*zipped 可理解为解压，返回二维矩阵式了，解压一般是对于都是数字而言的
[(1, 2, 3), (4, 5, 6)]

所以并行计算的方式是
1.import concurrent.futures    #先导入库
2.定义函数
3.开启线程池：with concurrent.ProcessPoolExecutor() as executor:
4.执行：for '对zip的第一个列表或元组要循环出来的结果：name1', '对zip的第二个列表或元组要循环出来的结果:name2' in zip(['第一个列表或元组'], executor.map('函数名', '执行函数的列表或元组')):
            print('%d is prime: %s' % (nume1, name2))    详情请见：https://docs.python.org/zh-cn/3/library/concurrent.futures.html



