##2017-06-25
##文件主要功能：统计文件夹下所有文件的数据，返回统计的结果
##
##
##
##
import pandas as pd
import os
import datetime
import tushare as ts

#
#
#
#
#
#统计文件夹下所有文件的数据，返回统计的结果
def UpdataStockData(FilePath):
    files = os.listdir(FilePath)#打开路径文件夹下所有文件

    outdata = pd.Series(index = range(-50,50))#构造输出数据
    outdata.index = outdata.index*0.2
    outdata = outdata.fillna(0)
    thisfile = 0.0
    for Datafile in files:
        filedata = Read_Csv_File(FilePath+'\\'+Datafile)#读取每个文件的数据
        outdata = outdata + GetFrequency(filedata,'p_change')
        thisfile = thisfile+1
        print thisfile/len(files)
    return outdata
		



#
#
#
#
#
#读取转置保存后的数据，转换为下载时的格式
#mFilename文件名
def Read_Csv_File(mFilename):
    filedata = pd.read_csv(mFilename).T
    filedata.columns = filedata.ix[0]#columns更新为首行
    filedata.index.name = 'date'
    filedata.columns.name = None
    filedata = filedata.ix[filedata.index[1:-1]]#去除首行
    filedata = filedata.drop_duplicates()#去除重复
    return filedata


#
#
#
#
#
#按mMindata,mMaxdata过滤mIndex列数据的数据
#只有mIndex列在[mMindata,mMaxdata]之间的数据才可以被输出
def FilteData(mStockData,mIndex,mMindata,mMaxdata):
    mRetunedata = mStockData[mStockData[mIndex] >= mMindata]
    mRetunedata = mRetunedata[mStockData[mIndex] < mMaxdata]
    mRetunedata = mRetunedata[mIndex]
    return mRetunedata



#
#
#
#
#
#统计mStockData数组里的频次数据
#mStockData：目标数据
#mIndex：统计的目标列
def GetFrequency(mStockData,mIndex):
    outdata = pd.Series(index = range(-50,50))
    outdata.index = outdata.index*0.2
    outdata.fillna(0)
    for i in range(-50,50):
        index = i*0.2
        mresult = FilteData(mStockData,mIndex,index,index+0.2)
        outdata[index] = mresult.size
    return outdata



#
#
#
#
#
#按照某个列进行分组
def Subsection(mStockData,mIndex):
    indextage=1
    Fronti = mStockData[mIndex][0]
    mStockData['tempindex']=0
    for i in mStockData.index:
        if mStockData[mIndex][i]*Fronti < 0:
            mStockData['tempindex'][i] = indextage + 1
            indextage = indextage + 1 
            Fronti = mStockData[mIndex][i]
        else:
            mStockData['tempindex'][i] = indextage
        print Fronti
    return mStockData
	

#加载Dll
from ctypes import * 
import win32api
mStockData = Read_Csv_File('d:\\stockdata\\000005.csv')
dllpath='D:\\MyProjects\\win_project\\DataFrameTool\\x64\\Release\\DataFrameTool.dll'

#
#
#
#
#
def StockToolInterface(mStockData):
    try:
        dll=CDLL('D:\\MyProjects\\win_project\\DataFrameTool\\x64\\Release\\DataFrameTool.dll')
        mStockData.to_clipboard()
        b=dll.ToolInterface(1)
        result = pd.read_clipboard()
        win32api.FreeLibrary(dll._handle)
        return result
    except:
        print 'Error'
        win32api.FreeLibrary(dll._handle)
        return mStockData


#
#
#
#
#
def isIncrease(mStockData,indexname):
    if mStockData[indexname][mStockData.index[0]] < mStockData[indexname][mStockData.index[-1]] and mStockData['BAR'][mStockData.index[0]] > 0:
        return 1
    else:
        return 0


#
#
#
#
#
def isReduce(mStockData,indexname):
    if mStockData[indexname][mStockData.index[0]] > mStockData[indexname][mStockData.index[-1]] and mStockData['BAR'][mStockData.index[0]] < 0:
        return 1
    else:
        return 0




#
#
#
#
#
def CheckBARChange(FilePath) :
    files = os.listdir(FilePath)#打开路径文件夹下所有文件
    Increase = 0
    Reduce = 0
    AllGroup = 0
    for Datafile in files:
        filedata = Read_Csv_File(FilePath + '\\' + Datafile)#读取每个文件的数据
        filedata = StockToolInterface(filedata)
        groupedData = filedata.groupby('BARChange')
        for name,singledata in groupedData:
            Increase += isIncrease(singledata,'close')
            Reduce += isReduce(singledata,'close')
            AllGroup = AllGroup + 1
        print Datafile
    return [AllGroup,Increase,Reduce]
		
		
		
		