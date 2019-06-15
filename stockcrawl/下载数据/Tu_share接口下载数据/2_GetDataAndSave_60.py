import pandas as pd
import os
import datetime
import tushare as ts
import numpy as np

# 最后合并的数据出错，需要进一步整理
# 需要有一个可以方便显示数据拆线图的工具

DataFile = 'd:\\StockFile\\whole\\StockCode.csv'
TestFile = 'D:\\StockFile\\test'
OriginalDay = '1991-01-01'
StockDatapath60 = 'd:\\StockFile\\StockData_60_New'


################################################调用get_hist_data###########################################
# 下载DataFile里面的股票数据
# 读取目标文件下'code'列中的股票代码，下载对应代码的数据
def GetAllDataAndSave(DataFiles, SavePath):
    FileList = pd.read_csv(DataFiles)
    for StockCode in FileList['code']:
        cur = datetime.datetime.now()  # 当前时间
        today = str(cur.year) + '-' + str(cur.month) + '-' + str(cur.day)
        strStoceCade = '0' * (6 - len(str(StockCode))) + str(StockCode)
        try:
            StockData = ts.get_k_data(strStoceCade, OriginalDay, today,ktype='60')
        except:
            print('Error')
        else:
            filename = SavePath + '//' + strStoceCade + '.csv'
            print(filename)
            try:
                if StockData.columns.name != 'date':
                    StockData.set_index(['date'], inplace=True)  # 将date列设置为index
                    StockData.columns.name = 'date'
                StockData = StockData.sort_index()#
                StockData = StockData.T.to_csv(filename)
            except:
                print('Save '+filename+' Error.')
    print('Done!')



if __name__=="__main__":
    GetAllDataAndSave(DataFile,StockDatapath60)

#########################################################################################################








