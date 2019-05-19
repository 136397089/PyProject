import pandas as pd
import os
import datetime
import tushare as ts
import numpy as np

# 最后合并的数据出错，需要进一步整理
# 需要有一个可以方便显示数据拆线图的工具

DataFile = 'd:\\StockFile\\StockCode.csv'
TestFile = 'D:\\StockFile\\test'
OriginalDay = '1991-01-01'
StockDatapath = 'd:\\StockFile\\StockData_D'
StockDatapathW = 'd:\\StockFile\\StockData_W'
StockDatapathM = 'd:\\StockFile\\StockData_M'



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
            StockData = ts.get_hist_data(strStoceCade, OriginalDay, today)
        except:
            print('Error')
        else:
            if not StockData is None:
                StockData.columns.name = 'date'
                filename = SavePath + '//' + strStoceCade + '.csv'
                print(filename)
                StockData = StockData.sort_index()  #
                StockData = StockData.T.to_csv(filename)
            else:
                print(filename)
    print('Done!')

#########################################################################################################


if __name__=="__main__":
    # 下载保存上证指数数据
    StockData = ts.get_hist_data('sh')
    StockData.sort_index().T.to_csv('d://StockFile//whole//sh.csv')





