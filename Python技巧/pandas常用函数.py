# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 15:02:29 2021

@author: 树风
"""
常用函数:
1.读
pd.read_csv(path,sep,delimiter,header,names,usecols,mangle_dupe_cols,dtype,na_values,parse_dates,date_parser,compression,encoding)

delimiter: 默认为False 设置为True时表示分隔符为空白字符,可以是空格,'\t',反正就是空白字符

header:设置导入Dataframe的列名称,

names:自定义列名，

header和names的关系为:
    names 没有被赋值，header 也没赋值 ：即选取文件的第一行作为表头
    names 没有被赋值，header 被赋值：即由header决定
    names 被赋值，header 没有被赋值：即由names决定
    names和header都被赋值：即由names决定，names将header设置好的表头给替换了
    总而言之：names的等级比header要高，还能把header给替换，把给设置好的header给删了
    用的话： 1. csv文件有表头并且是第一行，那么names和header都无需指定;
            2.csv文件有表头、但表头不是第一行，可能从下面几行开始才是真正的表头和数据，这个时候指定header即可;
            3. csv文件没有表头，全部是纯数据，那么我们可以通过names手动生成表头;
            4. csv文件有表头、但是这个表头你不想用，这个时候同时指定names和header。先用header选出表头和数据，然后再用names将表头替换掉，其实就等价于将数据读取进来之后再对列名进行rename;

usecols:如果列有很多，而我们不想要全部的列、而是只要指定的列就可以使用这个参数。
        同 index_col 一样，除了指定列名，也可以通过索引来选择想要的列，比如：usecols=[1, 2] 也会选择 "name" 和 "address" 两列，因为 "name" 这一列对应的索引是 1、"address" 对应的索引是 2。
        此外 use_cols 还有一个比较好玩的用法，就是接收一个函数，会依次将列名作为参数传递到函数中进行调用，如果返回值为真，则选择该列，不为真，则不选择,这是index_col没有的用法
        samples:
            # 选择列名的长度大于 4 的列，显然此时只会选择 address 这一列
            pd.read_csv('girl.csv', delim_whitespace=True, usecols=lambda x: len(x) > 4)
            
mangle_dupe_cols:实际生产用的数据会很复杂，有时导入的数据会含有重名的列。参数 mangle_dupe_cols 默认为 True，重名的列导入后面多一个 .1。如果设置为 False，会抛出不支持的异常：

dtype：指定类型进行解析，pandas默认会将字符串数字或数字都定义为整形，这在处理数据时不容易发现
        samples:
            df = pd.read_csv('girl.csv', delim_whitespace=True, dtype={"id": str})
            df["id"] = df["id"] * 3

na_values:na_values 参数可以配置哪些值需要处理成 NaN，这个是非常常用的，但是用的人不多。
        samples:
            pd.read_csv('girl.csv', sep="\t", na_values=["对", "古明地觉"])
            我们看到将"对"和"古明地觉"设置成了NaN，当然我们这里不同的列，里面包含的值都是不相同的。但如果两个列中包含相同的值，而我们只想将其中一个列的值换成NaN该怎么做呢？
            pd.read_csv('girl.csv', sep="\t", na_values={"name": ["古明地觉", "博丽灵梦"], "result": ["对"]})

parse_dates: 指定某些列为时间类型，这个参数一般搭配下面的date_parser使用。
    
date_parser: 是用来配合parse_dates参数的，因为有的列虽然是日期，但没办法直接转化，需要我们指定一个解析格式：
            samples:
                from datetime import datetime
                pd.read_csv('girl.csv', sep="\t", parse_dates=["date"], date_parser=lambda x: datetime.strptime(x, "%Y年%m月%d日"))

compression:参数取值为 {'infer', 'gzip', 'bz2', 'zip', 'xz', None}，默认 'infer'，这个参数直接支持我们使用磁盘上的压缩文件。
            samples:
                  # 直接将上面的girl.csv添加到压缩文件，打包成girl.zip
                  pd.read_csv('girl.zip', sep="\t", compression="zip")
                  
encoding：encoding 指定字符集类型，通常指定为 'utf-8'。根据情况也可能是'ISO-8859-1'


pd.read_excel(io,sheetname,header,index_col,dtype,converters,true_values,false_values,na_values)
io: excel文件路径
sheetname:表名，可以是str,int,list,None，默认为第一张表
                str:表名
                int:表的索引
                list:可以由str或列序号共同组成的表的列表，得到的数据类型是OrderedDict
                None:表示引用所有sheet
index_col:选用哪些作为索引，可以是 int,list of int,None
                None:默认选用第一列为索引
                int:选用哪列作为索引
                list of int: 选用哪些列作为索引，也就是索引可以由多个列组成
                dtype:Type name or dict of column 转换列的数据类型，方法与read_csv一样
                converters:dict 对指定列的数据进行指定函数的处理，传入参数为列名与函数组成的字典。key 可以是列名或者列的序号，values是函数，可以def函数或者直接lambda都行。
                        samples:对第2列的所有名称加上""，把第三列的所有年龄都减10
                            converters = {1:lambda x:"\""+x+"\"",2:lambda x:x-10})
                true_values: list 将指定的文本转换为True，默认为None
                false_values:   list 将指定的文本转换为False，默认为None
                na_values:指定某些列的某些值为NaN

