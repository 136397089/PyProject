
#使用了get_k_data函数来获取数据
import pandas as pd
import os
import datetime
import tushare as ts
import numpy as np

# 最后合并的数据出错，需要进一步整理
# 需要有一个可以方便显示数据拆线图的工具

DataFiles = 'd:\\StockFile\\StockCode.csv'
TestFile = 'D:\\StockFile\\test'
OriginalDay = '1997-01-01'
SavePath = 'd:\\StockFile\\StockData_D'
StockDatapathW = 'd:\\StockFile\\StockData_W'
StockDatapathM = 'd:\\StockFile\\StockData_M'
StockDatapath60 = 'd:\\StockFile\\StockData_60'


################################################调用get_k_data###########################################
# 下载DataFile里面的股票数据
# 读取目标文件下'code'列中的股票代码，下载对应代码的数据
def GetAllDataAndSave(DataFiles, SavePath):
    FailList = pd.read_csv(DataFiles)
    for StockCode in FailList['code']:
        strStoceCade = '0' * (6 - len(str(StockCode))) + str(StockCode)
        GetDataAndSave(StockCode, SavePath)
    print('Done!')



def GetDataAndSave(strStoceCade,SavePath):
    cur = datetime.datetime.now()  # 当前时间
    today = str(cur.year) + '-' + str(cur.month) + '-' + str(cur.day)
    try:
        StockData = ts.get_k_data(strStoceCade, OriginalDay, today,autype='qfq')
    except:
        print('Error')
    else:
        StockData.set_index(["date"], inplace=True)
        StockData.columns.name = 'date'
        filename = SavePath + '//' + strStoceCade + '.csv'
        print(filename)
        try:
            if StockData.columns.name != 'date':
                StockData.set_index(['date'], inplace=True)  # 将date列设置为index
                StockData.columns.name = 'date'
            StockData = StockData.sort_index()  #
            StockData = StockData.T.to_csv(filename)
        except:
            print(filename + + ' Error.')



if __name__=="__main__":
    print('是否重新下载股票数据到' + SavePath+'。(y：是 n:否) ')
    os.system('pause')
    #从DataFiles读取股票代码，然后将下载的股票数据保存到SavePath当中
    GetAllDataAndSave(DataFiles,SavePath)




