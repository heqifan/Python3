# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 21:18:56 2021

@author: 树风
"""

from selenium import webdriver

# 不自动关闭浏览器
option = webdriver.ChromeOptions()
option.add_experimental_option("detach", True)

# 将option作为参数添加到Chrome中
driver = webdriver.Chrome(chrome_options=option)

# Chrome浏览器      注意此处添加了chrome_options参数
driver = webdriver.Chrome()
driver.get('https://www.csdn.net/')
#<input id="toolbar-search-input" autocomplete="off" type="text" value="" placeholder="C++难在哪里？">
driver.find_element_by_id("toolbar-search-input")
#<meta name="keywords" content="CSDN博客,CSDN学院,CSDN论坛,CSDN直播">
driver.find_element_by_name("keywords")
