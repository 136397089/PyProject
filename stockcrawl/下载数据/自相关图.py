import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

'''
Descr:输入：时间序列timeSeries，滞后阶数k
        输出：时间序列timeSeries的k阶自相关系数
    l：序列timeSeries的长度
    timeSeries1，timeSeries2:拆分序列1，拆分序列2
    timeSeries_mean:序列timeSeries的均值
    timeSeries_var:序列timeSeries的每一项减去均值的平方的和
'''
def get_auto_corr(timeSeries, k):
    l = len(timeSeries)
    # 取出要计算的两个数组
    timeSeries1 = timeSeries[0:l - k]
    timeSeries2 = timeSeries[k:]
    timeSeries_mean = timeSeries.mean()
    timeSeries_var = np.array([i ** 2 for i in timeSeries - timeSeries_mean]).sum()
    auto_corr = 0
    for i in range(l - k):
        temp = (timeSeries1[i] - timeSeries_mean) * (timeSeries2[i] - timeSeries_mean) / timeSeries_var
        auto_corr = auto_corr + temp
    return auto_corr


# 画出各阶自相关系数的图
k = 4

'''
Descr:需要计算自相关函数get_auto_corr(timeSeries,k)
        输入时间序列timeSeries和想绘制的阶数k，k不能超过timeSeries的长度
        输出：k阶自相关系数图，用于判断平稳性
'''
def plot_auto_corr(timeSeries, k):
    timeSeriestimeSeries = pd.DataFrame(list(range(k)))
    for i in range(1, k + 1):
        timeSeriestimeSeries.loc[i - 1] = get_auto_corr(timeSeries, i)
    #plt.bar(range(1, len(timeSeriestimeSeries) + 1), timeSeriestimeSeries[0])
    return timeSeriestimeSeries

def Read_Csv_File(mFilename):
    if mFilename.find('csv') == -1:
        return
    filedata = pd.read_csv(mFilename).T
    filedata.columns = filedata.ix[0]  # columns更新为首行
    filedata.index.name = 'date'
    filedata.columns.name = None
    filedata = filedata.ix[filedata.index[1:-1]]  # 去除首行
    filedata = filedata.drop_duplicates()  # 去除重复
    return filedata


sh1=Read_Csv_File('D:\\StockFile\\test\\sh1.csv')
shclose=sh1.T[0:2].T
a=plot_auto_corr(shclose, len(shclose))
plt.plot(a)
plt.show()