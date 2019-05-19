# -*- coding:utf-8 -*-
import pandas as pd
import os
import datetime
import tushare as ts
import numpy as np

DataFile = 'd:\\StockFile\\StockCode.csv'
OriginalDay = '1991-01-01'
StockDatapath = 'd:\\StockFile\\StockData_D'
StockDatapathW = 'd:\\StockFile\\StockData_W'
StockDatapathM = 'd:\\StockFile\\StockData_M'




##ts.get_h_data         可以获取历史所有股票数据
##ts.get_hist_data      获取近三年的股票数据
#下载DataFile里面的股票数据
#读取目标文件下'code'列中的股票代码，下载对应代码的数据
def GetAllDataAndSave_M(DataFiles, SavePath):
    FailList=pd.read_csv(DataFiles)
    for StockCode in FailList['code']:
        cur=datetime.datetime.now()               #当前时间
        today=cur.strftime('%Y-%m-%d')
        strStoceCade = '0'*(6-len(str(StockCode))) + str(StockCode)
        try:
            StockData = ts.get_hist_data(strStoceCade,OriginalDay,today,ktype = 'M')
        except:
            print('Error')
        else:
            filename = SavePath + '//' + strStoceCade + '.csv'
            print(filename)
            StockData = StockData.sort_index()#
            StockData = StockData.T.to_csv(filename)
    print('Done!')

