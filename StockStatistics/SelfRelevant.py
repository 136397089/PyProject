import pandas as pd
import os
import datetime
import tushare as ts
import numpy as np
import pandas.io.data as web
import matplotlib.pyplot as plt
%matplotlib inline

def Correlation(x,t):
    X = np.convolve(np.array(x),np.array(x),mode='same')
    #plt.plot(X[:200])
    if t == 0:
        y1=x
        y2=x
    else:
        y1=x[0:-t]
        y2=x[t:]
    y = np.array(y1)*np.array(y2)
    return sum(y)/len(y)

def Read_Csv_File(mFilename):
    filedata = pd.read_csv(mFilename).T
    filedata.columns = filedata.ix[0]#columns更新为首行
    filedata.index.name = 'date'
    filedata.columns.name = None
    filedata = filedata.ix[filedata.index[1:-1]]#去除首行
    filedata = filedata.drop_duplicates()#去除重复
    return filedata

def test(StockNum):
    A = Read_Csv_File('D:/StockFile/StockData/' + StockNum +'.csv')
    x = A['p_change']
    d = [Correlation(x, i) for i in range(0, 20)]
    print sum(d)
    plt.plot(d)

