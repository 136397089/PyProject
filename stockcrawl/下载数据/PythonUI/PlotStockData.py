#!/usr/bin/python3
# -*- coding: utf-8 -*-

from matplotlib import pyplot as plt
import matplotlib.finance as mpf
from matplotlib.pylab import date2num
import pandas as pd
import datetime
import tushare as ts


dateFromat='%Y-%m-%d'
daycount=30
# 读CSV文件，转置之后的文件
# mFilename：目标文件名
# 返回值：读出的数据
def Read_Csv_File(mFilename):
    if mFilename.find('csv') == -1:
        return
    filedata = pd.read_csv(mFilename).T
    filedata.columns = filedata.iloc[0]  # columns更新为首行
    if filedata.columns.name != 'date':
        filedata.set_index(['date'], inplace=True)#将date列设置为index
        filedata.columns.name = 'date'
    filedata = filedata.drop(['date'])  # 去除首行
#    filedata = filedata.loc[filedata.index[1:-1]]  # 去除首行
    if filedata.columns.contains('amount'):
        filedata = filedata.drop(['amount'], axis=1)
    if filedata.columns.contains('code'):
        filedata = filedata.drop(['code'], axis=1)
    filedata = filedata.drop_duplicates(['close', 'high', 'low', 'open','volume'])  # 去除重复的行
    return filedata

def frameData2Num(inputDate):
    return  pd.Series([date2num(datetime.datetime.strptime(inputDate,dateFromat))],index=['date'])

def changetype(data):
    return pd.Series(float(data))

def financePlot_Web(stockcode,baginTime,endTime):
    quotes = []
    StockData = ts.get_k_data(stockcode, start=baginTime, end=endTime)  # 取得数据
    strbeginDay = StockData['date'][0]
    strendDay = StockData['date'][-1]
    StockData['date'] = StockData['date'].apply(frameData2Num)
    quotes = (StockData.loc[:,['date','open','high','low','close']].values.tolist())
    fig, ax = plt.subplots(facecolor=(0, 0.3, 0.5),figsize=(12,8))
    fig.subplots_adjust(bottom=0.1)
    ax.xaxis_date()
    plt.xticks(rotation=45) #日期显示的旋转角度
    plt.title(stockcode+' '+strbeginDay+' To '+strendDay)
    plt.xlabel('time')
    plt.ylabel('price')
    mpf.candlestick_ohlc(ax,quotes,width=0.7,colorup='r',colordown='green') # 上涨为红色K线，下跌为绿色，K线宽度为0.7
    plt.grid(True)
    plt.show()

def FrameDataFinancePlot(StockData,stockcode,timeType):
    quotes = []
    strbeginDay = StockData['date'][0]
    strendDay = StockData['date'][-1]
    if timeType == 'date':
        StockData['date'] = StockData['date'].apply(frameData2Num)
    elif timeType == 'time':
        StockData['date'] = pd.Series(list(range(737000,737000+len(StockData))),index=StockData.index).apply(changetype)
    quotes = (StockData.loc[:,['date','open','high','low','close']].values.tolist())
    fig, ax = plt.subplots(facecolor=(0, 0.3, 0.5),figsize=(12,8))
    fig.subplots_adjust(bottom=0.1)
    ax.xaxis_date()
    plt.xticks(rotation=45) #日期显示的旋转角度
    plt.title(stockcode+' '+strbeginDay+' To '+strendDay)
    plt.xlabel('time')
    plt.ylabel('price')
    mpf.candlestick_ohlc(ax,quotes,width=0.7,colorup='r',colordown='green') # 上涨为红色K线，下跌为绿色，K线宽度为0.7
    plt.grid(True)
    plt.show()

def CutStockData(InPutData,beginstr,endstr):
    InPutData = InPutData[InPutData.index > beginstr]
    InPutData = InPutData[InPutData.index < endstr]
    return InPutData

def PlotData_D(codename,beginTime):
    fromat='%Y-%m-%d'
    data=Read_Csv_File('D:\\StockFile\\StockData_D\\'+codename+'.csv')
    beginTime = datetime.datetime.strptime(beginTime, fromat)
    endTime = beginTime + datetime.timedelta(days = daycount)
    #beginTime = beginTime + datetime.timedelta(days = -10)
    data = CutStockData(data, beginTime.strftime(fromat),endTime.strftime(fromat))
    data['date']=data.index
    FrameDataFinancePlot(data,codename,'date')

def PlotData_30(codename,beginTime):
    fromat='%Y-%m-%d %H:%M'
    data=Read_Csv_File('D:\\StockFile\\StockData_30\\'+codename+'.csv')
    beginTime = datetime.datetime.strptime(beginTime, fromat)
    endTime = beginTime + datetime.timedelta(days = daycount)
    data = CutStockData(data, beginTime.strftime(fromat),endTime.strftime(fromat))
    data['date']=data.index
    FrameDataFinancePlot(data,codename,'time')


def PlotData_30(codename,beginTime,endTime):
    fromat='%Y-%m-%d %H:%M'
    data=Read_Csv_File('D:\\StockFile\\StockData_30\\'+codename+'.csv')
    beginTime = datetime.datetime.strptime(beginTime, fromat)
    endTime = datetime.datetime.strptime(endTime, fromat)
    data = CutStockData(data, beginTime.strftime(fromat),endTime.strftime(fromat))
    data['date']=data.index
    FrameDataFinancePlot(data,codename,'time')


def PlotData_60(codename,beginTime):
    fromat='%Y-%m-%d %H:%M'
    data=Read_Csv_File('D:\\StockFile\\StockData_60\\'+codename+'.csv')
    beginTime = datetime.datetime.strptime(beginTime, fromat)
    endTime = beginTime + datetime.timedelta(days = daycount)
    data = CutStockData(data, beginTime.strftime(fromat),endTime.strftime(fromat))
    data['date']=data.index
    FrameDataFinancePlot(data,codename,'time')


PlotData_30('000001','2019-04-01 12:00')
PlotData('000002','2019-01-01')


data=Read_Csv_File('D:\\StockFile\\StockData_30\\000001.csv')

date2num(datetime.datetime.strptime('2019-01-01 10:00:00','%Y-%m-%d'))
date2num(datetime.datetime.strptime('2019-01-01','%Y-%m-%d'))





PlotData_30('000001','2019-04-01 12:00')
PlotData_30('000001','2019-04-01 12:00')
PlotData_30('000001','2019-04-01 12:00')
PlotData_30('000001','2019-04-01 12:00')
PlotData_30('000001','2019-04-01 12:00')
PlotData_30('000001','2019-04-01 12:00')
PlotData_30('000001','2019-04-01 12:00')
PlotData_30('000001','2019-04-01 12:00')
PlotData_30('000001','2019-04-01 12:00')

