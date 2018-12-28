# -*- coding: utf-8 -*-  
#用CSV文件中的某几行画曲线图
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

hang1 = 14
hang2 = 17
a = pd.read_csv('D:\\StockFile\\test\\000002.csv')  #读取文件
a = a.T                                             #转置
a = a.iloc[1:-1,hang1:hang2]                        #取转置前的第1到最后一行，和hang1列到hang2列
a = a.sort_index()                                  #对转置后进行行排序
a.plot()                                            #绘图
plt.show()                                          #显示坐标