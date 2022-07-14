concat，merge，join和append的区别
Pandas提供了concat，merge，join和append四种方法用于dataframe的拼接，其区别如下：

Table1 concat，merge，join和append的适用情形
函数	适用场景	调用方法	备注
.concat()	可用于两个或多个df间行方向（增加行，下同）或列方向（增加列，下同）进行内联或外联拼接操作，默认行拼接，取并集	result = pd.concat( [df1,df4], axis=1 )	提供了参数axis设置行/列拼接的方向
.merge()	可用于两个df间行方向（一般用join代替）或列方向的拼接操作，默认列拼接，取交集（即：存在相同主键的df1和df2的列拼接）	result=pd.merge(df1, df2,how=‘left’)	提供了类似于SQL数据库连接操作的功能，支持左联、右联、内联和外联等全部四种SQL连接操作类型
.join()	可用于df间列方向的拼接操作，默认左列拼接，how=’left’	df1.join(df2)	支持左联、右联、内联和外联四种操作类型
.append()	可用于df间行方向的拼接操作，默认		
1. pandas.concat()函数详解
1.1 语法格式：
pandas.concat(objs, axis=0, join='outer', join_axes=None, ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False, sort=None, copy=True) 
1
1.2 参数说明：
objs：series，dataframe或者是panel对象构成的序列lsit
axis：指明连接的轴向， {0/’index’（行）, 1/’columns’（列）}，默认为0
join：指明连接方式 ， {‘inner’（交集）, ‘outer（并集）’}，默认为outer
join_axes：自定义的索引。指明用其他n-1条轴的索引进行拼接， 而非默认join =’ inner’或’outer’方式拼接
keys：创建层次化索引。可以是任意值的列表或数组、元组数组、数组列表（如果将levels设置成多级数组的话）
ignore_index=True：重建索引

1.3 核心功能：
两个DataFrame通过pd.concat()，既可实现行拼接又可实现列拼接，默认axis=0，join='outer'。表df1和df2的行索引（index）和列索引（columns）均可以重复。

设置join='outer'，只是沿着一条轴，单纯将多个对象拼接到一起，类似数据库中的全连接（union all）。
　　a. 当axis=0（行拼接）时，使用pd.concat([df1,df2])，拼接表的index=index(df1) + index(df2)，拼接表的columns=columns(df1) ∪ columns(df2)，缺失值填充NaN。
　　b. 当axis=1（列拼接）时，使用pd.concat([df1,df2],axis=1)，拼接表的index=index(df1) ∪ index(df2)，拼接表的columns=columns(df1) + columns(df2)，缺失值填充NaN。
　　备注： index(df1) + index(df2) 表示：直接在df1的index之后 直接累加 df2的index；columns(df1) ∪columns(df2)表示：df1的columns和df2的columns 累加去重 ，下同。
　　a. 当axis=0时，pd.concat([obj1, obj2])与obj1.append(obj2)的效果是相同的，使用参数key可以为每个数据集（bj1, obj2）指定块标记；
　　b. 当axis=1时，pd.concat([obj1, obj2], axis=1)与pd.merge(obj1, obj2, left_index=True, right_index=True, how='outer') 的效果是相同的。
设置join='inner'，拼接方式为“交联”，即：行拼接时，仅保留df1和df２列索引重复的列；列拼接时，仅保留df1和df２行索引重复的行。
　　a. 当axis=0（行拼接）时，使用pd.concat([df1,df4],join='inner')，拼接表的index=index(df1) + index(df2)，拼接表的columns=columns(df1) ∩ columns(df2)；
　　b. 当axis=1（列拼接）时，pd.concat([df1,df4],axis=1,join='inner')，拼接表的index=index(df1) ∩ index(df2)，拼接表的columns=columns(df1) + columns(df2)；
　　备注：　columns(df1) ∩columns(df2)表示：df1的columns和df2的columns 重复相同 ，下同。
1.4 常见范例：
a.列名（columns）相同，行索引（index）无重复项的表df1、df2、df3实现行拼接：

import numpy as np
import pandas as pd
#样集1
df1=pd.DataFrame({'A':['A0','A1','A2','A3'],'B':['B0','B1','B2','B3'],
                  'C':['C0','C1','C2','C3'],'D':['D0','D1','D2','D3']},
                index=[0,1,2,3])
#样集2
df2=pd.DataFrame({'A':['A4','A5','A6','A7'],'B':['B4','B5','B6','B7'],
                  'C':['C4','C5','C6','C7'],'D':['D4','D5','D6','D7']},
                  index=[4,5,6,7])   
#样集3
df3=pd.DataFrame({'A':['A8','A9','A10','A11'],'B':['B8','B9','B10','B11'],
                  'C':['C8','C9','C10','C11'],'D':['D8','D9','D10','D11']},
                index=[8,9,10,11])   
#样集4
df4=pd.DataFrame({'B':['B2','B3','B6','B7'],'D':['D2','D3','D6','D7'],
                  'F':['F2','F3','F6','F7']},index=[2,3,6,7])
#样集1、2、3、4详见图1.1（a）                                                             
#列名（columns）相同，行索引（index）无重复项的表df1、df2、df3实现行拼接
frames = [df1, df2, df3]
pd.concat(frames)                           #效果见图1.1（b）
#使用参数key可以为每个数据集指定块标记
pd.concat(frames,keys=[ 'x','y','z' ])      #效果见图1.1（c）
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
得到的行拼接效果如图1.1所示：


Fig. 1.1 列名相同，行索引无重复项的表df1、df2、df3实现行拼接
b.列名（columns）和行索引（index）均有重复的表df1、df4实现行/列拼接（默认‘join=outer’）：

## 使用concat()实现df1、df4行拼接               
result = pd.concat( [df1,df4] )              #效果见图1.2（b）
#使用concat()实现df1、df4列拼接
result = pd.concat( [df1,df4] , axis=1 )     #效果见图1.2（c）
1
2
3
4


Fig.1.2 列名和行索引均有重复的表df1、df4实现行/列拼接（默认‘join=outer’）
c.列名（columns）和行索引（index）均有重复的表df1、df4实现行/列拼接（设置‘join=inner’）：

#concat修改join='inner'，只保留重复列索引的行拼接
result=pd.concat([df1,df4],join='inner')   #效果见图1.3（b）
#concat修改join='inner'，只保留重复行索引的列拼接
result=pd.concat([df1,df4],axis=1,join='inner')     #效果见图1.3（c）
#利用参数join_axes=[df1.index]指定concat按照df1的行索引进行列拼接，df2仅保留行索引与df1重复的部分     
result=pd.concat( [df1,df4],axis=1,join_axes=[df1.index] )   #效果见图1.3（d）
1
2
3
4
5
6
得到的列拼接效果如图1.3所示：


Fig.1.3 列名（columns）和行索引（index）均有重复的表df1、df4实现行/列拼接（设置‘join=inner’）
2. pandas.merge()函数详解
2.1 语法格式：
DataFrame.merge(left, right, how='inner', on=None, left_on=None, right_on=None, left_index=False, right_index=False, sort=False, suffixes=('_x', '_y'), copy=True, indicator=False, validate=None)
1
2.2 参数说明：
left和right：两个不同的DataFrame或Series
how：连接方式，有inner、left、right、outer，默认为inner
on：用于连接的列索引名称，必须同时存在于左、右两个DataFrame中，默认是以两个DataFrame列名的交集作为连接键，若要实现多键连接，‘on’参数后传入多键列表即可
left_on：左侧DataFrame中用于连接键的列名，这个参数在左右列名不同但代表的含义相同时非常有用；
right_on：右侧DataFrame中用于连接键的列名
left_index：使用左侧DataFrame中的行索引作为连接键（ 但是这种情况下最好用JOIN）
right_index：使用右侧DataFrame中的行索引作为连接键（ 但是这种情况下最好用JOIN）
sort：默认为False，将合并的数据进行排序，设置为False可以提高性能
suffixes：字符串值组成的元组，用于指定当左右DataFrame存在相同列名时在列名后面附加的后缀名称，默认为(’_x’, ‘_y’)
copy：默认为True，总是将数据复制到数据结构中，设置为False可以提高性能
indicator：显示合并数据中数据的来源情况

2.3 核心功能：
类似于关系型数据库的连接方式，可以根据一个或多个键将两张不同的DatFrame连接起来，由于默认how='inner'，故合并表仅保留key重名的行，不重名的行将被丢弃。（ 备注： merge()只能完成两张表的连接，若有三个及以上表，需不断两两合并来实现）
该函数的典型应用场景： 两张表有相同内容的某一列（类似SQL中的主键），欲根据主键将两张表进行列拼接整合到一张表中，合并表的列数等于两个原数据表的列数和减去连接键的数量。

df1和df2的列索引（columns）仅有一项重复（即：col_1(df1)=col_1(df2)）时，存在如下三种类型的数据合并：一对一、多对一、多对多，其拼接规则如下：
　　1. 一对一：若df1（左表）和df2（右表）的重名列col_1(df1)和col_1(df2)中，各列的值均不重复，通过pd.merge()方法能够自动识别相同的行作为主键，进行列拼接（拼接原理类似基因配对，拼接过程示意图见图1.4）；
　　 备注： 共同列中的元素位置可以不一致，pd.merge()能够自动选取相同的行进行拼接。另外，pd.merge()默认会丢弃原来的索引，重新生成索引。
　　 　　 2.多对一：若df1（左表）和df2（右表）的重名列col_1(df1)和col_1(df2)，有一列的值有重复，通过多对一合并获得的连接表将会保留重复值。
　　 3. 多对多：若df1（左表）和df2（右表）的重名列col_1(df1)和col_1(df2)都包含重复值，那么通过多对多合并获得的连接表将会保留所有重复值。
　　 备注： 若重名列col_1(df1)有m行重名和col_1(df2)有n行重名，则合并表将有m×n行数据。

Fig.1.4 利用merge实现表df1、df2的列拼接（默认：how='inner'，df1和df2的列索引数据类型“一对一”）
df1和df2的列索引（columns）有两项及以上重复（即：col_1(df1)=col_1(df2)，col_2(df1)=col_2(df2)，…）时，即：实现多键连接，仅需在'on'参数后传入多键列表即可。
，
2.4 常见范例：
a. 两张表df1和df2的列名有重叠，且重叠列的内容完全相同，直接用pd.merge(df1, df2)

#样集1
df1=pd.DataFrame(np.arange(12).reshape(3,4),columns=['a','b','c','d'])
>>> df1
>>> a  b   c   d
>>> 0  0  1   2   3
>>> 1  4  5   6   7
>>> 2  8  9  10  11
>>> #样集2
>>> df2=pd.DataFrame({'b':[1,5],'d':[3,7],'a':[0,4]})  
>>> df2
>>> b  d  a
>>> 0  1  3  0
>>> 1  5  7  4
>>> #两张表df1和df2的列名有重叠，且重叠列的内容完全相同，直接用pd.merge(df1, df2)
>>> pd.merge(df1,df2)  
>
>a	b	c	d
>0	0	1	2	3
>1	4	5	6	7  
>1
>2
>3
>4
>5
>6
>7
>8
>9
>10
>11
>12
>13
>14
>15
>16
>17
>18
>19
>b. 两张表df1和df2的列名有重叠，但重叠列的内容完全不同，须使用pd.merge(df1, df2, left_index=True, right_index=True, how='left')
>（备注： 如果直接用pd.merge(df1, df2)，将会得到一张空表，故必须指定行索引参数left_index, right_index，这种情况下最好使用join实现。）

#样集1
df1=pd.DataFrame(np.arange(12).reshape(3,4),columns=['a','b','c','d'])
>>>df1
>>>a  b   c   d
>>>0  0  1   2   3
>>>1  4  5   6   7
>>>2  8  9  10  11
>>>#样集2
>>>df2=pd.DataFrame({'b':[15,6],'d':[1,11],'a':[0,6]}) 
>>>df2
>>>b   d  a
>>>0  15   1  0
>>>1   6  11  6
>>>#b.	两张表df1和df2的列名有重叠，但重叠列的内容完全不同
>>>pd.merge(df1, df2, left_index=True, right_index=True, how='left')    
>
>a_x	b_x	c	d_x	  b_y	d_y	  a_y
>0	0	1	2	3	 15.0	1.0	  0.0
>1	4	5	6	7	 6.0	11.0  6.0
>2	8	9	10	11	 NaN    NaN	  NaN
>1
>2
>3
>4
>5
>6
>7
>8
>9
>10
>11
>12
>13
>14
>15
>16
>17
>18
>19
>20
3. pandas.join()函数详解
3.1 语法格式：
DataFrame.join(other, on=None, how='left', lsuffix=' ', rsuffix=' ', sort=False)
1
3.2 参数说明：
参数的意义与merge方法基本相同，只是join方法默认为左外连接how=’left’

3.3 核心功能：
该函数的典型应用场景：无重复列名的两个表df1和df2 基于行索引进行列拼接，直接使用df1.join(df2)即可,无需添加任何参数，合并表的行数与left表相同，列数为left表+right表的列数之和，结果仅保留left表和right表中行索引相同的行，对列不做任何处理。如果两个表有重复的列名，需指定lsuffix, rsuffix参数。
　　利用join也可 基于列索引进行列拼接，需借助参数‘on’。常见的基于列索引的列拼接方式有3种：
（Ⅰ）列名不同，列内容有相同：需要用到 l.join(r.set_index(key of r), on='key of l')
（Ⅱ）列名和列内容均有相同：需要用到l.join(r.set_index(key), on='key')
（Ⅲ）列名不同，列内容也不同：这种情况是典型的基于行索引进行列拼接，不能用JOIN的ON参数。
JOIN 拼接列，主要用于基于行索引上的合并。

3.4 常见范例：
a. 无重复列名的两个表df1和df3基于 行索引，进行列拼接，直接使用df1.join(df2)即可
b. 有重复列名的两个表df1和df2（即使内容没有重复）基于 行索引，进行列拼接，使用df1.join(df2)时需要指定lsuffix, rsuffix参数，即：df1.join(df2, lsuffix='_l', rsuffix='_r')，否则会报错。

#样集1
df1=pd.DataFrame(np.arange(12).reshape(3,4),columns=['a','b','c','d'])
>>>df1
>>>a  b   c   d
>>>0  0  1   2   3
>>>1  4  5   6   7
>>>2  8  9  10  11
>>>#样集2
>>>df2=pd.DataFrame({'b':[15,6],'d':[1,11],'a':[0,6]})
>>>df2
>>>b   d  a
>>>0  15   1  0
>>>1   6  11  6
>>>#用join合并表df1和表df2,需指定lsuffix, rsuffix参数,标识两个表的重复列名
>>>df1.join(df2, lsuffix='_l', rsuffix='_r') 
>
>a_l	b_l	 c	 d_l	b_r	 d_r	a_r
>0	0	1	 2	 3	   15.0  1.0	0.0
>1	4	5	 6	 7	   6.0	 11.0	6.0
>2	8	9	 10	 11	   NaN	 NaN	NaN
>1
>2
>3
>4
>5
>6
>7
>8
>9
>10
>11
>12
>13
>14
>15
>16
>17
>18
>19
>20
>c. 列名不同，列内容有相同的两个表df1和df2基于 列索引，进行列拼接，使用l.join(r.set_index(key of r), on='key of l')，这种JOIN的写法等同于前面提到的merge设置left_on,right_on（备注：#列名不同，使用merge进行列拼接时，内容相同的行可以作为键），因为merge默认是内连接，所以返回的结果只有一行，而JOIN返回的结果是以左表的key列为准，有两行。

#样集1
left=pd.DataFrame({'key1':['foo','bar1'],'lval':[1,2]})
>>>left
>>>key1  lval
>>>0    foo     1
>>>1   bar1     2
>>>#样集2
>>>right=pd.DataFrame({'key2':['foo','bar'],'rval':[4,5]})
>>>right
>>>key2  rval
>>>0  foo     4
>>>1  bar     5
>>>#列名不同，列内容有相同的两个表df1和df2基于列索引，进行列拼接
>>>left.join(right.set_index('key2'),on='key1')  #.set_index()设置表right的列索引
>
>key1	lval   rval
>0	foo	    1	   4.0
>1	bar1	2	   NaN
>1
>2
>3
>4
>5
>6
>7
>8
>9
>10
>11
>12
>13
>14
>15
>16
>17
>18
>d. 列名和列内容均有相同的两个表df1和df2基于 列索引，进行列拼接，使用l.join(r.set_index(key), on='key')，这种JOIN的写法等同于前面提到的merge设置不带任何参数，而且这种情况下merge会去掉重复的列

#样集1
left=pd.DataFrame({'key':['foo','bar1'],'lval':[1,2]})
>
>key  lval
>0   foo     1
>1  bar1     2
>#样集2
>right=pd.DataFrame({'key':['foo','bar'],'rval':[4,5]})
>
>key  rval
>0  foo     4
>1  bar     5
>#列名和列内容均部分相同的表df1和df2进行基于列索引，列拼接
>left.join(right.set_index('key'),on='key')
>
>key	  lval	rval
>0	foo  	1	4.0
>1	bar1	2	NaN
>#样集3
>left=pd.DataFrame({'key':['foo','bar1'],'val':[1,2]})
>
>key   val
>0   foo     1
>1   bar1    2
>#样集4
>right=pd.DataFrame({'key':['foo','bar'],'val':[4,5]})
>
>key  val
>0  foo    4
>1  bar    5
>#列名相同，列内容部分相同的表df1和df2基于列索引进行列合并，必须用参数lsuffix='_l',rsuffix='_r'指定重名列的下标，否则报错
>left.join(right.set_index('key'),on='key',lsuffix='_l',rsuffix='_r')
>
>key	  val_l	 val_r
>0	foo	    1	 4.0
>1	bar1	2	 NaN
>#特别注意，即使列名相同了，也必须用到' set_index(key)' 否则直接使用
>left.join(right,on='key',lsuffix='_l',rsuffix='_r')
>>> ValueError: You are trying to merge on object and int64 columns. If you wish to proceed you should use pd.concat
>>> #另外需明确，不指定'ON= '参数的情况下，JOIN是按行索引进行列拼接，不对列进行任何操作。
>>> left.join(right,lsuffix='_l',rsuffix='_r')
>
>  key_l	val_l	key_r	val_r
>0	    foo	     1	     foo	4
>1	    bar1	 2       bar	5
>1
>2
>3
>4
>5
>6
>7
>8
>9
>10
>11
>12
>13
>14
>15
>16
>17
>18
>19
>20
>21
>22
>23
>24
>25
>26
>27
>28
>29
>30
>31
>32
>33
>34
>35
>36
>37
>38
>39
>40
>41
>42
>43
>44
>45
4. DataFrame.append()函数详解
4.1 语法格式：
DataFrame.append(other, ignore_index=False, verify_integrity=False, sort=None)
1
4.2 参数说明：
other: DataFrame or Series/dict-like object, or list of these
The data to append.
ignore_index : boolean, default False
If True, do not use the index labels.
verify_integrity : boolean, default False
If True, raise ValueError on creating index with duplicates.
sort: boolean, default None
只是join方法默认为左外连接how=’left’

4.3 核心功能：
append是concat的简略形式,只不过只能在axis=0上进行合并

df1.append(df2),df1.append(df2,ignore_index=True)

DataFrame和Series进行合并的时候需要使用参数ignore_index=True或者含有属性name，因为Series是只有一维索引的（备注：如果不添加参数ignore_index=True，那么会出错的。）。

