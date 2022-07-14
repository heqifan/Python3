# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 15:17:35 2021

@author: 树风
"""

from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def kappa(confusion_matrix):
    pe_rows = np.sum(confusion_matrix, axis=0)
    pe_cols = np.sum(confusion_matrix, axis=1)
    sum_total = sum(pe_cols)
    pe = np.dot(pe_rows, pe_cols) / float(sum_total ** 2)
    po = np.trace(confusion_matrix) / float(sum_total)
    return (po - pe) / (1 - pe)

path= r'D:\python作业\建立混淆矩阵并计算kappa系数\temp.csv'
data = pd.read_csv(path,sep = ',')
y_true = list(data['mean'])
y_pred = list(data['ID'])
hun = confusion_matrix(y_true, y_pred)
data = data.sort_values(by=['ID'])
didian = list(data['name'].unique())
hun_data = pd.DataFrame(hun, index=didian, columns=didian)
# 计算混淆矩阵的kappa 
K = kappa(hun)
print("Kappa值为", K)
