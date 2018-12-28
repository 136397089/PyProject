##2017-06-25
##�ļ���Ҫ���ܣ�ͳ���ļ����������ļ������ݣ�����ͳ�ƵĽ��
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
#ͳ���ļ����������ļ������ݣ�����ͳ�ƵĽ��
def UpdataStockData(FilePath):
    files = os.listdir(FilePath)#��·���ļ����������ļ�

    outdata = pd.Series(index = range(-50,50))#�����������
    outdata.index = outdata.index*0.2
    outdata = outdata.fillna(0)
    thisfile = 0.0
    for Datafile in files:
        filedata = Read_Csv_File(FilePath+'\\'+Datafile)#��ȡÿ���ļ�������
        outdata = outdata + GetFrequency(filedata,'p_change')
        thisfile = thisfile+1
        print thisfile/len(files)
    return outdata
		



#
#
#
#
#
#��ȡת�ñ��������ݣ�ת��Ϊ����ʱ�ĸ�ʽ
#mFilename�ļ���
def Read_Csv_File(mFilename):
    filedata = pd.read_csv(mFilename).T
    filedata.columns = filedata.ix[0]#columns����Ϊ����
    filedata.index.name = 'date'
    filedata.columns.name = None
    filedata = filedata.ix[filedata.index[1:-1]]#ȥ������
    filedata = filedata.drop_duplicates()#ȥ���ظ�
    return filedata


#
#
#
#
#
#��mMindata,mMaxdata����mIndex�����ݵ�����
#ֻ��mIndex����[mMindata,mMaxdata]֮������ݲſ��Ա����
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
#ͳ��mStockData�������Ƶ������
#mStockData��Ŀ������
#mIndex��ͳ�Ƶ�Ŀ����
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
#����ĳ���н��з���
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
	

#����Dll
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
    files = os.listdir(FilePath)#��·���ļ����������ļ�
    Increase = 0
    Reduce = 0
    AllGroup = 0
    for Datafile in files:
        filedata = Read_Csv_File(FilePath + '\\' + Datafile)#��ȡÿ���ļ�������
        filedata = StockToolInterface(filedata)
        groupedData = filedata.groupby('BARChange')
        for name,singledata in groupedData:
            Increase += isIncrease(singledata,'close')
            Reduce += isReduce(singledata,'close')
            AllGroup = AllGroup + 1
        print Datafile
    return [AllGroup,Increase,Reduce]
		
		
		
		