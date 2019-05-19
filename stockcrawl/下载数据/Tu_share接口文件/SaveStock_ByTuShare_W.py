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


###############################################################################################################
#调用get_hist_data
#UpdataStockData更新文件夹下所有股票文件的数据
#FilePath：目标文件夹
#无返回值
def GetAllDataAndSave_W(DataFiles, SavePath):
    FailList=pd.read_csv(DataFiles)
    for StockCode in FailList['code']:
        cur=datetime.datetime.now()               #当前时间
        today=str(cur.year)+'-'+str(cur.month)+'-'+str(cur.day)
        strStoceCade = '0'*(6-len(str(StockCode))) + str(StockCode)
        try:
            StockData = ts.get_hist_data(strStoceCade,OriginalDay,today,ktype = 'W')
        except:
            print('Error')
        else:
            filename = SavePath + '//' + strStoceCade + '.csv'
            print(filename)
            StockData = StockData.sort_index()#
            StockData = StockData.T.to_csv(filename)
    print('Done!')
	

