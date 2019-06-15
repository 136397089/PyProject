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
StockDatapath = 'd:\\StockFile\\StockData_D_Current'
StockDatapathW = 'd:\\StockFile\\StockData_W_Current'
StockDatapathM = 'd:\\StockFile\\StockData_M_Current'

#
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
    return filedata

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


def GetCurrentData():
    CurrentData = ts.get_today_all()
    if CurrentData.index.name != 'code' and CurrentData.columns.contains('code'):
        CurrentData.set_index(['code'], inplace=True)
    else:
         return False
    if CurrentData.columns.contains('trade'):
        CurrentData.rename(columns={'trade': 'close'}, inplace=True)
    return CurrentData

def UpdataStockData(FilePath):
    CurrentData = GetCurrentData()
    files = os.listdir(FilePath)  # 打开路径文件夹下所有文件
    for Datafile in files:
        updateFile(FilePath + '\\' + Datafile,Datafile[0:6],CurrentData)
    print("Done!")


def updateFile(FilePath,StockCode,todayData):
    filedata = Read_Csv_File(FilePath)  # 读取每个文件的数据
#    if filedata.empty():
#        print('Read ' + StockCode + ' error')
#        return False
    lastDay = filedata.index.max()  # 最近的那一天
    beginday = filedata.index.min()
    cur = datetime.datetime.now()  # 当前时间
    today = str(cur.year) + '/' + str(cur.month) + '/' + str(cur.day)
    filedata = filedata.reindex(list(filedata.index) + [today])
    targetData=[]
    if todayData.index.contains(StockCode[0:6]):
        targetData = todayData.loc[StockCode[0:6]]
    else:
        print('do not find '+ StockCode + 'data.')
        print(StockCode + " Is Stop.")
        return False
    filedata.loc[today]['open'] = targetData['open']
    filedata.loc[today]['close'] = targetData['close']
    filedata.loc[today]['high'] = targetData['high']
    filedata.loc[today]['low'] = targetData['low']
    filedata.loc[today]['volume'] = targetData['volume']
#    filedata = filedata.sort_index()  # 排序
    filedata.T.to_csv(FilePath)  # 保存数据
    print('........')
    print(StockCode)



if __name__=="__main__":
    print('是否将目录 '+StockDatapath+' 下的股票数据全部更新到今天。(y：是 n:否)  本程序只更新一天数据')
    os.system('pause')
    UpdataStockData(StockDatapath)
    cur = datetime.datetime.now()
    OriginalDay = '1997-01-01'
    today = str(cur.year) + '-' + str(cur.month) + '-' + str(cur.day)
    ts.get_k_data('sh',start=OriginalDay, end=today).sort_index().T.to_csv('d://StockFile//whole//sh'+'.csv')






