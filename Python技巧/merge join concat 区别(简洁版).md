Merge-数据库风格的合并
数据的合并（merge）和连接（join）是我们在数据分析和挖掘中不可或缺的，是通过一个或一个以上的键连接的。pandas的合并（merge）的的绝大功能和数据库操作类似的。具有如下参数：

pd.merge(left, right, how=’inner’, on=None, left_on=None, right_on=None, left_index=False, right_index=False, sort=False, suffixes=(‘_x’, ‘_y’), copy=True, indicator=False, validate=None)

参数说明：
left、right：左右连接对象

how：连接方式，共有’inner’,’left’,right’,’outer’

on：根据连接的键

left_on、right_on：在连接的键名不同的情况下使用，left_on传入左对象的键，right_on传入右对象的键

left_index、right_index：设置索引是否作为连接的键，通常 left_on=??和right_index=True, right_on=??和left_index=True，或者left_index=True和right_index=True

sort：对连接后的结果是否排序，当数据巨大的时候为了追求效率可以设置为False

suffixes：对于不作为键的同名列，在其列名后添加的后缀

copy：将左右对象的内容复制过来，默认为True

df1=pd.DataFrame({'名字':list('ABCDE'),'性别':['男','女','男','男','女'],'职称':['副教授','讲师','助教','教授','助教']},index=range(1001,1006))
df1.columns.name='学院老师'
df1.index.name='编号'
df1
1
2
3
4
代码结果：
学院老师	名字	性别	职称
编号			
1001	A	男	副教授
1002	B	女	讲师
1003	C	男	助教
1004	D	男	教授
1005	E	女	助教
df2=pd.DataFrame({'名字':list('ABDAX'),'课程':['C++','计算机导论','汇编','数据结构','马克思原理'],'职称':['副教授','讲师','教授','副教授','讲师']},index=[1001,1002,1004,1001,3001])
df2.columns.name='课程'
df2.index.name='编号'
df2
1
2
3
4
代码结果：
课程	名字	职称	课程
编号			
1001	A	副教授	C++
1002	B	讲师	计算机导论
1004	D	教授	汇编
1001	A	副教授	数据结构
3001	X	讲师	马克思原理
1 默认连接方式

默认下是根据左右对象中出现同名的列作为连接的键，且连接方式是on=’inner’

pd.merge(df1,df2)
1
代码结果：
名字	性别	职称	课程
0	A	男	副教授	C++
1	A	男	副教授	数据结构
2	B	女	讲师	计算机导论
3	D	男	教授	汇编
2 指定列名合并

pd.merge(df1,df2,on='名字')
1
代码结果：
名字	性别	职称_x	职称_y	课程
0	A	男	副教授	副教授	C++
1	A	男	副教授	副教授	数据结构
2	B	女	讲师	讲师	计算机导论
3	D	男	教授	教授	汇编
3 其他连接方式:left/right/outer

关于连接方式不懂的可参考该博客：https://blog.csdn.net/plg17/article/details/78758593

pd.merge(df1,df2,how='left')
1
代码结果：
名字	性别	职称	课程
0	A	男	副教授	C++
1	A	男	副教授	数据结构
2	B	女	讲师	计算机导论
3	C	男	助教	NaN
4	D	男	教授	汇编
5	E	女	助教	NaN
pd.merge(df1,df2,how='right')
1
代码结果：
名字	性别	职称	课程
0	A	男	副教授	C++
1	A	男	副教授	数据结构
2	B	女	讲师	计算机导论
3	D	男	教授	汇编
4	X	NaN	讲师	马克思原理
pd.merge(df1,df2,how='outer')
1
代码结果：
名字	性别	职称	课程
0	A	男	副教授	C++
1	A	男	副教授	数据结构
2	B	女	讲师	计算机导论
3	C	男	助教	NaN
4	D	男	教授	汇编
5	E	女	助教	NaN
6	X	NaN	讲师	马克思原理
4 根据多个键进行连接

pd.merge(df1,df2,on=['职称','名字'])
1
代码结果：
名字	性别	职称	课程
0	A	男	副教授	C++
1	A	男	副教授	数据结构
2	B	女	讲师	计算机导论
3	D	男	教授	汇编
5 对重复的列名处理

细心的你可能在上面的 2 观察到了，不作为连接键的相同列名更改了。那是因为当不指定连接的键的时候是将‘名字’、‘职称’作为连接的键。

pd.merge(df1,df2,on='名字',suffixes=('_1','_2'))
1
代码结果：
名字	性别	职称_1	职称_2	课程
0	A	男	副教授	副教授	C++
1	A	男	副教授	副教授	数据结构
2	B	女	讲师	讲师	计算机导论
3	D	男	教授	教授	汇编
6 将索引作为连接的键

当我们连接时，无论是左右对象的索引都会被丢弃的。当们需要将索引作为连接键时可以如下方式：

pd.merge(df1,df2,left_on='性别',right_index=True)
1
代码结果：
名字_x	性别	职称_x	名字_y	职称_y	课程
编号						
pd.merge(df1,df2,on=['名字','职称'],left_index=True,right_index=True)
1
代码结果：
名字	性别	职称	课程
编号				
1001	A	男	副教授	C++
1001	A	男	副教授	数据结构
1002	B	女	讲师	计算机导论
1004	D	男	教授	汇编
对象的实例方法-Join
DataFrame对象有个df.join()方法也能进行pd.merge()的合并，它能更加方便地按照对象df的索引进行合并，且能同时合并多个DataFrame对象。它具有如下参数：

df.join(other, on=None, how=’left’, lsuffix=”, rsuffix=”, sort=False)

创建对象
df3=pd.DataFrame({'Red':[1,3,5],'Green':[5,0,3]},index=list('abd'))
df3
1
2
代码结果：
Green	Red
a	5	1
b	0	3
d	3	5
df4=pd.DataFrame({'Blue':[1,9],'Yellow':[6,6]},index=list('ce'))
df4
1
2
代码结果：
Blue	Yellow
c	1	6
e	9	6
1 简单合并（默认是left左连接）

df3.join(df4)
1
代码结果：
Green	Red	Blue	Yellow
a	5	1	NaN	NaN
b	0	3	NaN	NaN
d	3	5	NaN	NaN
2 和merge合并方式一样

df3.join(df4,how='outer')
1
代码结果：
Green	Red	Blue	Yellow
a	5.0	1.0	NaN	NaN
b	0.0	3.0	NaN	NaN
c	NaN	NaN	1.0	6.0
d	3.0	5.0	NaN	NaN
e	NaN	NaN	9.0	6.0
3 合并多个DataFrame对象

df5=pd.DataFrame({'Brown':[3,4,5],'White':[1,1,2]},index=list('aed'))
df3.join([df4,df5])
1
2
代码结果：
Green	Red	Blue	Yellow	Brown	White
a	5	1	NaN	NaN	3.0	1.0
b	0	3	NaN	NaN	NaN	NaN
d	3	5	NaN	NaN	5.0	2.0
df3.join([df4,df5],how='outer')
1
代码结果：
Green	Red	Blue	Yellow	Brown	White
a	5.0	1.0	NaN	NaN	3.0	1.0
b	0.0	3.0	NaN	NaN	NaN	NaN
c	NaN	NaN	1.0	6.0	NaN	NaN
d	3.0	5.0	NaN	NaN	5.0	2.0
e	NaN	NaN	9.0	6.0	4.0	1.0
轴向连接-Concat
在数据处理中，通常将原始数据分开几个部分进行处理而得到相似结构的Series或DataFrame对象，我们该如何进行纵向合并它们？这时我们可以选择用pd.concat()方式极易连接两个或两个以上的Series或DataFrame对象。如下是该函数的参数解读：

pd.concat(objs, axis=0, join=’outer’, join_axes=None, ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False, copy=True)

参数说明:
objs：连接对象，多以列表、字典传入

axis：轴向，0代表纵向连接，1，代表横向连接

join：连接方式，共有’inner’,’left’,right’,’outer’

join_axes:参与连接的索引

ignore_index：是否忽略索引

keys：层次化索引

1 Series对象的连接

s1=pd.Series([1,2],index=list('ab'))
s2=pd.Series([3,4,5],index=list('bde'))

pd.concat([s1,s2])
1
2
3
4
代码结果：

a    1
b    2
b    3
d    4
e    5
dtype: int64
1
2
3
4
5
6
2 纵向连接

pd.concat([s1,s2],axis=1)
1
代码结果：
0	1
a	1.0	NaN
b	2.0	3.0
d	NaN	4.0
e	NaN	5.0
3 用内连接求交集

pd.concat([s1,s2],axis=1,join='inner')
1
代码结果：
0	1
b	2	3
4 指定部分索引进行连接

pd.concat([s1,s2],axis=1,join_axes=[list('abc')])
1
代码结果：
0	1
a	1.0	NaN
b	2.0	3.0
c	NaN	NaN
5 创建层次化索引

pd.concat([s1,s2],keys=['A','B'])
1
代码结果：

A  a    1
   b    2
B  b    3
   d    4
   e    5
dtype: int64
1
2
3
4
5
6
6 当纵向连接时keys为列名

pd.concat([s1,s2],keys=['A','B'],axis=1)
1
代码结果：
A	B
a	1.0	NaN
b	2.0	3.0
d	NaN	4.0
e	NaN	5.0
7 DataFrame对象的连接

pd.concat([df3,df4],axis=1,keys=['A','B'])
1
代码结果：
A	B
Green	Red	Blue	Yellow
a	5.0	1.0	NaN	NaN
b	0.0	3.0	NaN	NaN
c	NaN	NaN	1.0	6.0
d	3.0	5.0	NaN	NaN
e	NaN	NaN	9.0	6.0
8 用字典的方式连接同样可以创建层次化列索引

pd.concat({'A':df3,'B':df4},axis=1)
1
代码结果：
A	B
Green	Red	Blue	Yellow
a	5.0	1.0	NaN	NaN
b	0.0	3.0	NaN	NaN
c	NaN	NaN	1.0	6.0
d	3.0	5.0	NaN	NaN
e	NaN	NaN	9.0	6.0
9 忽略索引

pd.concat([df3,df4],ignore_index=True)
1
代码结果：
Blue	Green	Red	Yellow
0	NaN	5.0	1.0	NaN
1	NaN	0.0	3.0	NaN
2	NaN	3.0	5.0	NaN
3	1.0	NaN	NaN	6.0
4	9.0	NaN	NaN	6.0
