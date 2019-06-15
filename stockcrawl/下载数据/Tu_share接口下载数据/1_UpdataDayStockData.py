# -*- coding:utf-8 -*-


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
StockDatapath = 'd:\\StockFile\\StockData_D'
StockDatapathW = 'd:\\StockFile\\StockData_W'
StockDatapathM = 'd:\\StockFile\\StockData_M'



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
    filedata = filedata.drop_duplicates(['close', 'high', 'low', 'open', 'volume'])  # 去除重复的行
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


def UpdataStockData(FilePath):
    files = os.listdir(FilePath)  # 打开路径文件夹下所有文件
    for Datafile in files:
        updateFile(FilePath + '\\' + Datafile,Datafile[0:6])
    print("Done!")


def updateFile(FilePath,StockCode):
    filedata = Read_Csv_File(FilePath)  # 读取每个文件的数据
    lastDay = filedata.index.max()  # 最近的那一天
    beginday = filedata.index.min()
    filedata = filedata[:-1]
    cur = datetime.datetime.now()  # 当前时间
    today = str(cur.year) + '-' + str(cur.month) + '-' + str(cur.day + 1)
    if lastDay.replace('0', '') != today.replace('0', ''):
        try:
            StockData = ts.get_hist_data(StockCode[0:6], start=lastDay, end=today)  # 取得数据
        except:
            print('Error')
        else:
            if not StockData is None:
                StockData.columns.name = 'date'
                StockData = pd.concat([filedata, StockData])  # 合并数据
                StockData.columns.name = 'date'
                StockData = StockData.sort_index()  # 排序
                StockData = StockData.dropna(axis=1)  # 去除有空值的列
                StockData['date'] = StockData.index
                StockData = StockData.drop_duplicates(['date'])  # 去除重复的行
                StockData.drop(['date'],axis=1,inplace=True)
                StockData.T.to_csv(FilePath)  # 保存数据
                print('........')
                print(StockCode)
            else:
                print(StockCode + " Is Stop.")


def RepairFrontStockData(FilePath):
    files = os.listdir(FilePath)  # 打开路径文件夹下所有文件
    for Datafile in files:
        filedata = Read_Csv_File(FilePath + '\\' + Datafile)  # 读取每个文件的数据
        lastDay = filedata.index.max()  # 最近的那一天
        beginday = filedata.index.min()
        cur = datetime.datetime.now()  # 当前时间
        today = str(cur.year) + '-' + str(cur.month) + '-' + str(cur.day)
        if OriginalDay.replace('0', '') != beginday.replace('0', ''):
            try:
                # print('from:' + lastDay +' to:' + today)
                StockData = ts.get_hist_data(Datafile[0:6], start=OriginalDay, end=today)  # 取得数据
            except:
                print('Error')
            else:
                StockData = pd.concat([filedata, StockData])  # 合并数据
                StockData = StockData.sort_index()  #
                StockData.dropna(axis=1)# 去除有空值的列
                StockData.T.to_csv(FilePath + '\\' + Datafile)  # 保存数据
                print('........')
                print(Datafile)
    print("Done!")


# 下载保存上证指数数据
StockData = ts.get_hist_data('sh')
StockData.sort_index().T.to_csv('d://StockFile//sh.csv')
#########################################################################################################


if __name__=="__main__":
    print('是否将目录 ' + StockDatapath + ' 下的股票数据全部更新到今天。(y：是 n:否)  本程序自动补全之前没有下载的数据。')
    os.system('pause')
    UpdataStockData(StockDatapath)
    cur = datetime.datetime.now()
    OriginalDay = '1997-01-01'
    today = str(cur.year) + '-' + str(cur.month) + '-' + str(cur.day)
    data = ts.get_k_data('sh',start=OriginalDay, end=today).set_index(['date']).sort_index()
    data.columns.name = 'date'
    data = data.T.to_csv('d://StockFile//whole//sh'+'.csv')





