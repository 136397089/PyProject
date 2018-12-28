import pandas as pd
import os
import datetime
import tushare as ts
import numpy as np

#最后合并的数据出错，需要进一步整理
#需要有一个可以方便显示数据拆线图的工具

DataFile = 'd:\\StockFile\\StockCode.csv'
OriginalDay = '1991-01-01'
StockDatapath = 'd:\\StockFile\\StockData_D'
StockDatapathW = 'd:\\StockFile\\StockData_W'

UpdataStockData(StockDatapath)	

#
#读CSV文件，转置之后的文件
#mFilename：目标文件名
#返回值：读出的数据
def Read_Csv_File(mFilename):
    filedata = pd.read_csv(mFilename).T
    filedata.columns = filedata.ix[0]#columns更新为首行
    filedata.index.name = 'date'
    filedata.columns.name = None
    filedata = filedata.ix[filedata.index[1:-1]]#去除首行
    filedata = filedata.drop_duplicates()#去除重复
    return filedata
################################################调用get_hist_data###########################################
#下载DataFile里面的股票数据
#读取目标文件下'code'列中的股票代码，下载对应代码的数据
def GetAllDataAndSave(DataFiles, SavePath):
    FailList=pd.read_csv(DataFiles)
    for StockCode in FailList['code']:
        cur=datetime.datetime.now()               #当前时间
        today=str(cur.year)+'-'+str(cur.month)+'-'+str(cur.day)
        beginDay = filedata.index.min()
        strStoceCade = '0'*(6-len(str(StockCode))) + str(StockCode)
        try:
            StockData = ts.get_hist_data(strStoceCade ,OriginalDay ,today)
        except:
            print('Error')
        else:
            filename = SavePath + '//' + strStoceCade + '.csv'
            print(filename)
            StockData = StockData.sort_index()#
            StockData = StockData.T.to_csv(filename)
    print('Done!')
def UpdataStockData(FilePath):
    files = os.listdir(FilePath)#打开路径文件夹下所有文件
    for Datafile in files:
        filedata = Read_Csv_File(FilePath + '\\' + Datafile)#读取每个文件的数据
        lastDay = filedata.index.max()            #最近的那一天
        beginday = filedata.index.min()
        cur=datetime.datetime.now()               #当前时间
        today=str(cur.year)+'-'+str(cur.month)+'-'+str(cur.day)
        if lastDay.replace('0','') != today.replace('0',''):
            try:
                #print('from:' + lastDay +' to:' + today)
                StockData = ts.get_hist_data(Datafile[0:6],start = lastDay,end = today)#取得数据
            except:
                print('Error')
            else:
                StockData = pd.concat([filedata,StockData])#合并数据
                StockData = StockData.sort_index()#
                #StockData = StockData[ StockData['stock'].isnull()]# 去除有空值的列
                StockData.T.to_csv(FilePath + '\\' + Datafile)#保存数据
                print('........')
                print(Datafile)
    print("Done!")
def RepairFrontStockData(FilePath):
    files = os.listdir(FilePath)#打开路径文件夹下所有文件
    for Datafile in files:
        filedata = Read_Csv_File(FilePath + '\\' + Datafile)#读取每个文件的数据
        lastDay = filedata.index.max()            #最近的那一天
        beginday = filedata.index.min()
        cur=datetime.datetime.now()               #当前时间
        today=str(cur.year)+'-'+str(cur.month)+'-'+str(cur.day)
        if OriginalDay.replace('0','') != beginday.replace('0',''):
            try:
                #print('from:' + lastDay +' to:' + today)
                StockData = ts.get_hist_data(Datafile[0:6],start = OriginalDay,end = beginday)#取得数据
            except:
                print('Error')
            else:
                StockData = pd.concat([filedata,StockData])#合并数据
                StockData = StockData.sort_index()#
                #StockData = StockData[ StockData['stock'].isnull()]# 去除有空值的列
                StockData.T.to_csv(FilePath + '\\' + Datafile)#保存数据
                print('........')
                print(Datafile)
    print("Done!")
	
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
        beginDay = filedata.index.min()
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
def UpdataStockData_W(FilePath):
    files = os.listdir(FilePath)#打开路径文件夹下所有文件
    for Datafile in files:
        filedata = Read_Csv_File(FilePath+'\\'+Datafile)#读取每个文件的数据
        lastDay = filedata.index.max()            #最近的那一天
        beginday = filedata.index.min()
        cur=datetime.datetime.now()               #当前时间
        today=str(cur.year)+'-'+str(cur.month)+'-'+str(cur.day)
        if lastDay.replace('0','') != today.replace('0',''):
            try:
                #print('from:' + lastDay +' to:' + today)
                StockData = ts.get_hist_data(Datafile[0:6],start = lastDay,end = today,ktype = 'W')#取得数据
            except:
                print('Error')
            else:
                StockData = pd.concat([filedata,StockData])#合并数据
                StockData = StockData.sort_index()#
                #StockData = StockData[ StockData['stock'].isnull()]# 去除有空值的列
                StockData.T.to_csv(FilePath + '\\' + Datafile)#保存数据
                print('........')
                print(Datafile)
    print("Done!")
def RepairFrontStockData_W(FilePath):
    files = os.listdir(FilePath)#打开路径文件夹下所有文件
    for Datafile in files:
        filedata = Read_Csv_File(FilePath+'\\'+Datafile)#读取每个文件的数据
        lastDay = filedata.index.max()            #最近的那一天
        beginday = filedata.index.min()
        cur=datetime.datetime.now()               #当前时间
        today=str(cur.year)+'-'+str(cur.month)+'-'+str(cur.day)
        if lastDay.replace('0','') != today.replace('0',''):
            try:
                #print('from:' + lastDay +' to:' + today)
                StockData = ts.get_hist_data(Datafile[0:6],start = OriginalDay,end = beginday,ktype = 'W')#取得数据
            except:
                print('Error')
            else:
                StockData = pd.concat([filedata,StockData])#合并数据
                StockData = StockData.sort_index()#
                #StockData = StockData[ StockData['stock'].isnull()]# 去除有空值的列
                StockData.T.to_csv(FilePath + '\\' + Datafile)#保存数据
                print('........')
                print(Datafile)
    print("Done!")


	
##ts.get_h_data         可以获取历史所有股票数据
##ts.get_hist_data      获取近三年的股票数据
#下载DataFile里面的股票数据
#读取目标文件下'code'列中的股票代码，下载对应代码的数据
def GetAllDataAndSave_M(DataFiles, SavePath):
    FailList=pd.read_csv(DataFiles)
    for StockCode in FailList['code']:
        cur=datetime.datetime.now()               #当前时间
        today=str(cur.year)+'-'+str(cur.month)+'-'+str(cur.day)
        beginDay = filedata.index.min()
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
def UpdataStockData_M(FilePath):
    files = os.listdir(FilePath)#打开路径文件夹下所有文件
    for Datafile in files:
        filedata = Read_Csv_File(FilePath+'\\'+Datafile)#读取每个文件的数据
        lastDay = filedata.index.max()            #最近的那一天
        beginday = filedata.index.min()
        cur=datetime.datetime.now()               #当前时间
        today=str(cur.year)+'-'+str(cur.month)+'-'+str(cur.day)
        if lastDay.replace('0','') != today.replace('0',''):
            try:
                #print('from:' + lastDay +' to:' + today)
                StockData = ts.get_hist_data(Datafile[0:6],start = lastDay,end = today,ktype = 'M')#取得数据
            except:
                print('Error')
            else:
                StockData = pd.concat([filedata,StockData])#合并数据
                StockData = StockData.sort_index()#
                #StockData = StockData[ StockData['stock'].isnull()]# 去除有空值的列
                StockData.T.to_csv(FilePath + '\\' + Datafile)#保存数据
                print('........')
                print(Datafile)
    print("Done!")
def RepairFrontStockData_M(FilePath):
    files = os.listdir(FilePath)#打开路径文件夹下所有文件
    for Datafile in files:
        filedata = Read_Csv_File(FilePath+'\\'+Datafile)#读取每个文件的数据
        lastDay = filedata.index.max()            #最近的那一天
        beginday = filedata.index.min()
        cur=datetime.datetime.now()               #当前时间
        today=str(cur.year)+'-'+str(cur.month)+'-'+str(cur.day)
        if lastDay.replace('0','') != today.replace('0',''):
            try:
                #print('from:' + lastDay +' to:' + today)
                StockData = ts.get_hist_data(Datafile[0:6],start = OriginalDay,end = beginday,ktype = 'M')#取得数据
            except:
                print('Error')
            else:
                StockData = pd.concat([filedata,StockData])#合并数据
                StockData = StockData.sort_index()#
                #StockData = StockData[ StockData['stock'].isnull()]# 去除有空值的列
                StockData.T.to_csv(FilePath + '\\' + Datafile)#保存数据
                print('........')
                print(Datafile)
    print("Done!")





#下载保存上证指数数据
StockData = ts.get_hist_data('sh')
StockData.sort_index().T.to_csv('d://StockFile//sh.csv')
#########################################################################################################








