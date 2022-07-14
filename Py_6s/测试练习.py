# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 18:33:37 2022

@author: Administrator
"""

'''1'''
# Import all of the Py6S code
from Py6S import *
# Create a SixS object called s (used as the standard name by convention)     创建一个名为s的SixS对象(按约定用作标准名称)
s = SixS()
# Run the 6S simulation defined by this SixS object across the      运行由这个SixS对象定义的6S模拟
# whole VNIR range         整个VNIR范围
wavelengths, results = SixSHelpers.Wavelengths.run_vnir(s, output_name="pixel_radiance")
# Plot these results, with the y axis label set to "Pixel Radiance"  绘制这些结果，将y轴标签设置为“像素亮度”
SixSHelpers.Wavelengths.plot_wavelengths(wavelengths, results, "Pixel Radiance")

'''2'''
from Py6S import *
s = SixS()
s.atmos_profile = AtmosProfile.PredefinedType(AtmosProfile.Tropical) #将大气剖面更改为名为“热带”的预定义剖面
s.wavelength = Wavelength(0.357)   #模拟的波长更改为 0.357 微米
s.run() #直接访问输出，而不是在特定波长范围内运行并绘制它
print(s.outputs.fulltext)   #