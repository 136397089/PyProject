# -*- coding:utf-8 -*-
#这个文件的代码用于分析筛选某个股票在当天上涨的时候，前一天的指标
import pandas as pd
import os
import datetime
import tushare as ts
import numpy as np
from scipy import stats

#
#
#读CSV文件，转置之后的文件
#mFilename：目标文件名
#返回值：读出的数据
def Read_Csv_File(mFilename):
    filedata = pd.read_csv(mFilename).T
    filedata.columns = filedata.ix[0]#columns更新为首行
    filedata.index.name = 'date'
    filedata.columns.name = None
    filedata = filedata.ix[filedata.index[1:-1]]#去除首行
    filedata = filedata.drop_duplicates()#去除重复
    return filedata


TargeData = Read_Csv_File('D:\\StockFile\\test\\000001.csv')
#读出的数据只保留70行以后的，前面的数据不做分析
TargeData = TargeData[70:]
TargeData =TargeData.dropna(axis=1, how='any')#删除有NaN的列
size = [TargeData.shape[0],TargeData.shape[1]]
#求差分
TargeD = TargeData.diff()
Temp = TargeD
#'BAR'列向下平移
Temp = TargeD['BAR'].shift(1)
#删除含有NaN的行
Temp ＝ Temp.dropna(axis=0, how='any')
#价格上涨的行
Improve = TargeD [TargeD['p_change'] > 0.5]
#平均值
Improve['BAR'].mean()
d = TargeD [TargeD['p_change'] < -0.5]
d['BAR'].mean()
TargeD['BAR'].min()
TargeD['BAR'].max()
TargeData['p_change'].var()#方差

u = TargeData['p_change'].mean()  # 计算均值
std = TargeData['p_change'].std()  # 计算标准差
#value值直接写样本就可以了，中间是norm默认是以正态分布去做判断，后边是均值和方差
[statistic ,pvalue ]=stats.kstest(list(TargeData['p_change']), 'norm', (u, std)) 



from matplotlib import pyplot

#绘制频次分布直方图
def drawHist(datas):
    #创建直方图
    #第一个参数为待绘制的定量数据，不同于定性数据，这里并没有事先进行频数统计
    #第二个参数为划分的区间个数
    pyplot.hist(datas, 100)
    pyplot.xlabel('P_Change')
    pyplot.ylabel('Frequency')
    pyplot.title('datas')
    pyplot.show()

	
#绘制累积曲线
def drawCumulativeHist(heights):
    #创建累积曲线
    #第一个参数为待绘制的定量数据
    #第二个参数为划分的区间个数
    #normed参数为是否无量纲化
    #histtype参数为'step'，绘制阶梯状的曲线
    #cumulative参数为是否累积
    pyplot.hist(heights, 20, normed=True, histtype='step', cumulative=True)
    pyplot.xlabel('Heights')
    pyplot.ylabel('Frequency')
    pyplot.title('Heights Of Male Students')
    pyplot.show()

#绘制散点图
def drawScatter(heights, weights):
    #创建散点图
    #第一个参数为点的横坐标
    #第二个参数为点的纵坐标
    pyplot.scatter(heights, weights)
    pyplot.xlabel('Heights')
    pyplot.ylabel('Weights')
    pyplot.title('Heights & Weights Of Male Students')
    pyplot.show()
    

#获得上周5的日期
from datetime import datetime  
from dateutil.relativedelta import relativedelta  
from dateutil.rrule import *  
d = datetime.now()  
print(d)  
print(d + relativedelta(weekday=FR))  
print(d + relativedelta(weekday=FR(-1)))  
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    