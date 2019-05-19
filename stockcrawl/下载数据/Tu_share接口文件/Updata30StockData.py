import pandas as pd
import os
import datetime
import tushare as ts
import numpy as np

DataFile = 'd:\\StockFile\\StockCode.csv'
TestFile = 'D:\\StockFile\\test'
OriginalDay = '1991-01-01'

StockDatapath = 'd:\\StockFile\\StockData_30'
StockDatapath2 = 'd:\\StockFile\\StockData_30\\000002.csv'
StockDatapath1 = 'd:\\StockFile\\StockData_30\\000001.csv'

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

def UpdataStockData(FilePath):
    files = os.listdir(FilePath)  # 打开路径文件夹下所有文件
    for Datafile in files:
        updateFile(FilePath + '\\' + Datafile,Datafile[0:6])
    print("Done!")


def updateFile(FilePath,StockCode):
    print(StockCode+' begin.')
    filedata = Read_Csv_File(FilePath)  # 读取每个文件的数据
    lastDay = filedata.index.max()  # 最近的那一天
    beginday = filedata.index.min()
    print(lastDay)
    if lastDay.find('/') > 0:
        lastdayTemp = datetime.datetime.strptime(lastDay, "%Y/%m/%d %H:%M")
    if lastDay.find('-') > 0:
         lastdayTemp = datetime.datetime.strptime(lastDay, "%Y-%m-%d %H:%M")
    lastdayTemp = lastdayTemp + datetime.timedelta(days=-1)
    lastDay = str(lastdayTemp.year) + '-' + str(lastdayTemp.month) + '-' + str(lastdayTemp.day)
    cur = datetime.datetime.now()  # 当前时间
    cur = cur + datetime.timedelta(days=0)
    today = str(cur.year) + '-' + str(cur.month) + '-' + str(cur.day)
    if lastDay.replace('0', '') != today.replace('0', ''):
        try:
            StockData = ts.get_k_data(StockCode[0:6], start=lastDay, end=today,ktype='30')  # 取得数据
        except:
            print('Error')
        else:
            if not StockData is None:
                StockData.columns.name = 'date'
                StockData.set_index(["date"], inplace=True)
                StockData = pd.concat([filedata, StockData])  # 合并数据
                StockData.columns.name = 'date'
                StockData = StockData.sort_index()  # 排序
                StockData = StockData.dropna(axis=1)  # 去除有空值的列
                StockData = StockData.drop_duplicates(['close', 'high', 'low', 'open'])  # 去除重复的行
                StockData.T.to_csv(FilePath)  # 保存数据
                print('........')
                print(StockCode)
            else:
                print(StockCode + " Is Stop.")
    print(StockCode+' finish.')



if __name__=="__main__":
    UpdataStockData(StockDatapath)

