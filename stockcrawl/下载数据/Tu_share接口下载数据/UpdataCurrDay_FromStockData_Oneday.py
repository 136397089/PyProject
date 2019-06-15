import pandas as pd
import os
import datetime
import tushare as ts
import numpy as np



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


def UpdateData(fileData,stockcode,currentData):
    if fileData.columns.contains('amount'):
        fileData = fileData.drop(['amount'], axis=1)
    if fileData.columns.contains('code'):
        fileData = fileData.drop(['code'], axis=1)
    print("remove code")
    theStockCurrent =[]
    if not currentData.index.contains(stockcode):
        return fileData
    theStockCurrent = currentData.loc[stockcode]  # 取得目标股票的当前数据
    cur = datetime.datetime.now()
    newindexname = str(cur.year) + '-' + str(cur.month).zfill(2) + '-' + str(cur.day).zfill(2)
    fileData = fileData.reindex(list(fileData.index) + [newindexname])
    for dataname in fileData.columns:
        fileData.loc[newindexname][dataname] = theStockCurrent[dataname]
    #fileData.loc[newindexname]['open'] = fileData.loc[fileData.index[-2]]['close']
    fileData.loc[newindexname]['volume'] = fileData.loc[newindexname]['volume']/100#成交量单位换算
    return fileData


def UpdataCurrentDataFiles(CurrentData,sourceFilePath,WhereaboutsFilePath):
    if CurrentData.columns.contains('trade'):
        CurrentData.rename(columns={'trade': 'close'}, inplace=True)
    files = os.listdir(sourceFilePath)
    for Datafile in files:
        filedata = Read_Csv_File(sourceFilePath+'//'+Datafile)
        filedata = UpdateData(filedata,Datafile[0:6],CurrentData)
        print(WhereaboutsFilePath + Datafile)
        filedata.T.to_csv(WhereaboutsFilePath + Datafile)

StockDatapath2 = 'd://StockFile//tockData_60//000002.csv'
StockDatapath1 = 'd://StockFile//StockData_60//000001.csv'
FromFilePath = 'd://StockFile//StockData_60'
ToFilePath = 'd://StockFile//StockData_60_Current//'


if __name__=="__main__":
    sourceFilePath = 'd://StockFile//StockData_D'
    WhereaboutsFilePath = 'd://StockFile//StockData_D_Current//'
    print('是否从' + sourceFilePath + '读出数据，并将目录 ' + WhereaboutsFilePath + ' 下的股票数据全部更新到今天。(y：是 n:否)  本程序只更新一天数据')
    os.system('pause')
    CurrentData = ts.get_today_all()
    if CurrentData.index.name != 'code' and CurrentData.columns.contains('code'):
        CurrentData.set_index(['code'], inplace=True)
    print('begin '+sourceFilePath)
    UpdataCurrentDataFiles(CurrentData,sourceFilePath,WhereaboutsFilePath)




