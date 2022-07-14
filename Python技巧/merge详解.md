`merge`是用来拼接两张表的，那么拼接时自然就需要将用户信息**一一对应**地进行拼接，所以进行拼接的两张表需要有一个共同的识别用户的**键（key）**。总结来说，整个`merge`的过程就是将信息**一一对应匹配**的过程，下面介绍`merge`的四种类型，分别为`'inner'`、`'left'`、`'right'`和`'outer'`。

## **一、inner**

`merge`的`'inner'`的类型称为**内连接**，它在拼接的过程中会取**两张表的键（key）的交集**进行拼接。什么意思呢？下面以图解的方式来一步一步拆解。

首先我们有以下的数据，左侧和右侧的数据分别代表了用户的**基础信息**和**消费信息**，连接两张表的键是`userid`。

![img](https://pic3.zhimg.com/80/v2-919d59c55d07d27cbe17561ff4090af2_1440w.jpg)

现在用`'inner'`的方式进行`merge`

```text
In [6]: df_1.merge(df_2,how='inner',on='userid')
Out[6]:
  userid  age  payment
0      a   23     2000
1      c   32     3500
```

**过程图解：**

①取两张表的键的**交集**，这里`df_1`和`df_2`的`userid`的交集是`{a,c}`

![img](https://pic1.zhimg.com/80/v2-a9fd053b4aa3e14c770f9879d174cb10_1440w.jpg)

②对应匹配

![img](https://pic4.zhimg.com/80/v2-75ab5c34d653055dfe752bb2baa8e4c7_1440w.jpg)

③结果

![img](https://pic2.zhimg.com/80/v2-a029dcf20aabb6d0eb663c727e670151_1440w.jpg)

**过程汇总：**

![img](https://pic4.zhimg.com/80/v2-edda27bd6990feb60c8b7499e356bfcb_1440w.jpg)

相信整个过程并不难理解，上面演示的是同一个键下，两个表对应只有一条数据的情况（一个用户对应一条消费记录），那么，如果**一个用户对应了多条消费记录**的话，那又是怎么拼接的呢？

假设现在的数据变成了下面这个样子，在`df_2`中，有两条和`a`对应的数据：

![img](https://pic1.zhimg.com/80/v2-aa3a316a4496e3823302b7c157596f74_1440w.jpg)

同样用`inner`的方式进行`merge`：

```text
In [12]: df_1.merge(df_2,how='inner',on='userid')
Out[12]:
  userid  age  payment
0      a   23     2000
1      a   23      500
2      b   46     1000
3      c   32     3500
```

整个过程除了**对应匹配阶段**，其他和上面基本都是一致的。

**过程图解：**

①取两张表的键的**交集**，这里`df_1`和`df_2`的`userid`的交集是`{a,b,c}`

![img](https://pic4.zhimg.com/80/v2-ceb1eab5b64865b410bc3da7540b2ed3_1440w.jpg)

②对应匹配时，由于这里的`a`有两条对应的消费记录，故在拼接时，会将用户基础信息表中`a`对应的数据**复制多一行来和右边进行匹配**。

![img](https://pic2.zhimg.com/80/v2-cdc07e9ad0a1178d8c15671cb0e49da9_1440w.jpg)

③结果

![img](https://pic3.zhimg.com/80/v2-7e6ca9af48ff041ce480b856e8709ef2_1440w.jpg)

## **二、left 和right**

`'left'`和`'right'`的`merge`方式其实是类似的，分别被称为**左连接**和**右连接**。这两种方法是可以互相转换的，所以在这里放在一起介绍。

- `'left'`

`merge`时，以**左边表格的键为基准**进行配对，如果左边表格中的键在右边不存在，则用缺失值`NaN`填充。

- `'right'`

`merge`时，以**右边表格的键为基准**进行配对，如果右边表格中的键在左边不存在，则用缺失值`NaN`填充。

什么意思呢？用一个例子来具体解释一下，这是演示的数据

![img](https://pic4.zhimg.com/80/v2-3f91e3029109a1722ba7edd466ea358b_1440w.jpg)

现在用`'left'`的方式进行`merge`

```text
In [21]: df_1.merge(df_2,how='left',on='userid')
Out[21]:
  userid  age  payment
0      a   23   2000.0
1      b   46      NaN
2      c   32   3500.0
3      d   19      NaN
```

**过程图解：**

①以左边表格的所有键为基准进行配对。图中，因为右表中的`e`不在左表中，故不会进行配对。

![img](https://pic2.zhimg.com/80/v2-a06a39f19646c10c3001aa5d7174e5f1_1440w.jpg)

②若右表中的`payment`列合并到左表中，对于没有匹配值的用缺失值`NaN`填充

![img](https://pic3.zhimg.com/80/v2-4d634bf55fd31a0b95393d85770ebdc2_1440w.jpg)

**过程汇总：**

![img](https://pic2.zhimg.com/80/v2-fed4d5834207a2aada79256e487a2041_1440w.jpg)

对于`'right'`类型的`merge`和`'left'`其实是差不多的，只要把两个表格的位置调换一下，两种方式返回的结果就是一样的（），如下：

```text
In [22]: df_2.merge(df_1,how='right',on='userid')
Out[22]:
  userid  payment  age
0      a   2000.0   23
1      c   3500.0   32
2      b      NaN   46
3      d      NaN   19
```

至于`'left'`和`'right'`中（乃至于下面将介绍的`'outer'`）连接的键是一对多的情况，原理和上方的`'inner'`是类似的，这里便不再赘述。

## **三、outer**

`'outer'`是**外连接**，在拼接的过程中它会取**两张表的键（key）的并集**进行拼接。看文字不够直观，还是上例子吧！

还是使用上方用过的演示数据

![img](https://pic4.zhimg.com/80/v2-3f91e3029109a1722ba7edd466ea358b_1440w.jpg)

这次使用`'outer'`进行`merge`

```text
In [24]: df_1.merge(df_2,how='outer',on='userid')
Out[24]:
  userid   age  payment
0      a  23.0   2000.0
1      b  46.0      NaN
2      c  32.0   3500.0
3      d  19.0      NaN
4      e   NaN    600.0
```

**图解如下：**

①取两张表键的并集，这里是`{a,b,c,d,e}`

![img](https://pic2.zhimg.com/80/v2-3e7a748ff15e99dfe66811ab8542f9fd_1440w.jpg)

②将两张表的数据列拼起来，对于没有匹配到的地方，使用缺失值`NaN`进行填充

![img](https://pic3.zhimg.com/80/v2-2e994e07050a44687fdb98414129a95a_1440w.jpg)

能读到这里的小伙伴想必也基本理解了`merge`的整个过程，总结来说，`merge`的不同类型区别就在于拼接时，**选用的是两表的键的集合不同**。关于Pandas的`merge`就介绍到这里！