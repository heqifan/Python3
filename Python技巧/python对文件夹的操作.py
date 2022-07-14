# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 00:03:29 2021

@author: 树风
"""

# 查看当前工作目录
os.getcwd()

# 修改当前工作目录
os.chdir( path )



创建文件：

1) os.mknod("test.txt") 创建空文件

2) open("test.txt",w) 直接打开一个文件，如果文件不存在则创建文件

创建目录：

os.mkdir("file") 创建目录

复制文件：

shutil.copyfile("oldfile","newfile") oldfile和newfile都只能是文件

shutil.copy("oldfile","newfile") oldfile只能是文件夹，newfile可以是文件，也可以是目标目录

复制文件夹：

shutil.copytree("olddir","newdir") olddir和newdir都只能是目录，且newdir必须不存在

重命名文件（目录）

os.rename("oldname","newname") 文件或目录都是使用这条命令

移动文件（目录）

shutil.move("oldpos","newpos")

删除文件

os.remove("file")

删除目录

os.rmdir("dir") 只能删除空目录

shutil.rmtree("dir") 空目录、有内容的目录都可以删

转换目录

os.chdir("path") 换路径

判断目标

os.path.exists("goal") 判断目标是否存在

os.path.isdir("goal") 判断目标是否目录

os.path.isfile("goal") 判断目标是否文件