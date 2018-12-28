import pandas as pd
import os
import datetime
import tushare as ts
import numpy as np

#���ϲ������ݳ�����Ҫ��һ������
#��Ҫ��һ�����Է�����ʾ���ݲ���ͼ�Ĺ���

DataFile = 'd:\\StockFile\\StockCode.csv'
OriginalDay = '1991-01-01'
StockDatapath = 'd:\\StockFile\\StockData_D'
StockDatapathW = 'd:\\StockFile\\StockData_W'

UpdataStockData(StockDatapath)	

#
#��CSV�ļ���ת��֮����ļ�
#mFilename��Ŀ���ļ���
#����ֵ������������
def Read_Csv_File(mFilename):
    filedata = pd.read_csv(mFilename).T
    filedata.columns = filedata.ix[0]#columns����Ϊ����
    filedata.index.name = 'date'
    filedata.columns.name = None
    filedata = filedata.ix[filedata.index[1:-1]]#ȥ������
    filedata = filedata.drop_duplicates()#ȥ���ظ�
    return filedata
################################################����get_hist_data###########################################
#����DataFile����Ĺ�Ʊ����
#��ȡĿ���ļ���'code'���еĹ�Ʊ���룬���ض�Ӧ���������
def GetAllDataAndSave(DataFiles, SavePath):
    FailList=pd.read_csv(DataFiles)
    for StockCode in FailList['code']:
        cur=datetime.datetime.now()               #��ǰʱ��
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
    files = os.listdir(FilePath)#��·���ļ����������ļ�
    for Datafile in files:
        filedata = Read_Csv_File(FilePath + '\\' + Datafile)#��ȡÿ���ļ�������
        lastDay = filedata.index.max()            #�������һ��
        beginday = filedata.index.min()
        cur=datetime.datetime.now()               #��ǰʱ��
        today=str(cur.year)+'-'+str(cur.month)+'-'+str(cur.day)
        if lastDay.replace('0','') != today.replace('0',''):
            try:
                #print('from:' + lastDay +' to:' + today)
                StockData = ts.get_hist_data(Datafile[0:6],start = lastDay,end = today)#ȡ������
            except:
                print('Error')
            else:
                StockData = pd.concat([filedata,StockData])#�ϲ�����
                StockData = StockData.sort_index()#
                #StockData = StockData[ StockData['stock'].isnull()]# ȥ���п�ֵ����
                StockData.T.to_csv(FilePath + '\\' + Datafile)#��������
                print('........')
                print(Datafile)
    print("Done!")
def RepairFrontStockData(FilePath):
    files = os.listdir(FilePath)#��·���ļ����������ļ�
    for Datafile in files:
        filedata = Read_Csv_File(FilePath + '\\' + Datafile)#��ȡÿ���ļ�������
        lastDay = filedata.index.max()            #�������һ��
        beginday = filedata.index.min()
        cur=datetime.datetime.now()               #��ǰʱ��
        today=str(cur.year)+'-'+str(cur.month)+'-'+str(cur.day)
        if OriginalDay.replace('0','') != beginday.replace('0',''):
            try:
                #print('from:' + lastDay +' to:' + today)
                StockData = ts.get_hist_data(Datafile[0:6],start = OriginalDay,end = beginday)#ȡ������
            except:
                print('Error')
            else:
                StockData = pd.concat([filedata,StockData])#�ϲ�����
                StockData = StockData.sort_index()#
                #StockData = StockData[ StockData['stock'].isnull()]# ȥ���п�ֵ����
                StockData.T.to_csv(FilePath + '\\' + Datafile)#��������
                print('........')
                print(Datafile)
    print("Done!")
	
###############################################################################################################
#����get_hist_data
#UpdataStockData�����ļ��������й�Ʊ�ļ�������
#FilePath��Ŀ���ļ���
#�޷���ֵ
def GetAllDataAndSave_W(DataFiles, SavePath):
    FailList=pd.read_csv(DataFiles)
    for StockCode in FailList['code']:
        cur=datetime.datetime.now()               #��ǰʱ��
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
    files = os.listdir(FilePath)#��·���ļ����������ļ�
    for Datafile in files:
        filedata = Read_Csv_File(FilePath+'\\'+Datafile)#��ȡÿ���ļ�������
        lastDay = filedata.index.max()            #�������һ��
        beginday = filedata.index.min()
        cur=datetime.datetime.now()               #��ǰʱ��
        today=str(cur.year)+'-'+str(cur.month)+'-'+str(cur.day)
        if lastDay.replace('0','') != today.replace('0',''):
            try:
                #print('from:' + lastDay +' to:' + today)
                StockData = ts.get_hist_data(Datafile[0:6],start = lastDay,end = today,ktype = 'W')#ȡ������
            except:
                print('Error')
            else:
                StockData = pd.concat([filedata,StockData])#�ϲ�����
                StockData = StockData.sort_index()#
                #StockData = StockData[ StockData['stock'].isnull()]# ȥ���п�ֵ����
                StockData.T.to_csv(FilePath + '\\' + Datafile)#��������
                print('........')
                print(Datafile)
    print("Done!")
def RepairFrontStockData_W(FilePath):
    files = os.listdir(FilePath)#��·���ļ����������ļ�
    for Datafile in files:
        filedata = Read_Csv_File(FilePath+'\\'+Datafile)#��ȡÿ���ļ�������
        lastDay = filedata.index.max()            #�������һ��
        beginday = filedata.index.min()
        cur=datetime.datetime.now()               #��ǰʱ��
        today=str(cur.year)+'-'+str(cur.month)+'-'+str(cur.day)
        if lastDay.replace('0','') != today.replace('0',''):
            try:
                #print('from:' + lastDay +' to:' + today)
                StockData = ts.get_hist_data(Datafile[0:6],start = OriginalDay,end = beginday,ktype = 'W')#ȡ������
            except:
                print('Error')
            else:
                StockData = pd.concat([filedata,StockData])#�ϲ�����
                StockData = StockData.sort_index()#
                #StockData = StockData[ StockData['stock'].isnull()]# ȥ���п�ֵ����
                StockData.T.to_csv(FilePath + '\\' + Datafile)#��������
                print('........')
                print(Datafile)
    print("Done!")


	
##ts.get_h_data         ���Ի�ȡ��ʷ���й�Ʊ����
##ts.get_hist_data      ��ȡ������Ĺ�Ʊ����
#����DataFile����Ĺ�Ʊ����
#��ȡĿ���ļ���'code'���еĹ�Ʊ���룬���ض�Ӧ���������
def GetAllDataAndSave_M(DataFiles, SavePath):
    FailList=pd.read_csv(DataFiles)
    for StockCode in FailList['code']:
        cur=datetime.datetime.now()               #��ǰʱ��
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
    files = os.listdir(FilePath)#��·���ļ����������ļ�
    for Datafile in files:
        filedata = Read_Csv_File(FilePath+'\\'+Datafile)#��ȡÿ���ļ�������
        lastDay = filedata.index.max()            #�������һ��
        beginday = filedata.index.min()
        cur=datetime.datetime.now()               #��ǰʱ��
        today=str(cur.year)+'-'+str(cur.month)+'-'+str(cur.day)
        if lastDay.replace('0','') != today.replace('0',''):
            try:
                #print('from:' + lastDay +' to:' + today)
                StockData = ts.get_hist_data(Datafile[0:6],start = lastDay,end = today,ktype = 'M')#ȡ������
            except:
                print('Error')
            else:
                StockData = pd.concat([filedata,StockData])#�ϲ�����
                StockData = StockData.sort_index()#
                #StockData = StockData[ StockData['stock'].isnull()]# ȥ���п�ֵ����
                StockData.T.to_csv(FilePath + '\\' + Datafile)#��������
                print('........')
                print(Datafile)
    print("Done!")
def RepairFrontStockData_M(FilePath):
    files = os.listdir(FilePath)#��·���ļ����������ļ�
    for Datafile in files:
        filedata = Read_Csv_File(FilePath+'\\'+Datafile)#��ȡÿ���ļ�������
        lastDay = filedata.index.max()            #�������һ��
        beginday = filedata.index.min()
        cur=datetime.datetime.now()               #��ǰʱ��
        today=str(cur.year)+'-'+str(cur.month)+'-'+str(cur.day)
        if lastDay.replace('0','') != today.replace('0',''):
            try:
                #print('from:' + lastDay +' to:' + today)
                StockData = ts.get_hist_data(Datafile[0:6],start = OriginalDay,end = beginday,ktype = 'M')#ȡ������
            except:
                print('Error')
            else:
                StockData = pd.concat([filedata,StockData])#�ϲ�����
                StockData = StockData.sort_index()#
                #StockData = StockData[ StockData['stock'].isnull()]# ȥ���п�ֵ����
                StockData.T.to_csv(FilePath + '\\' + Datafile)#��������
                print('........')
                print(Datafile)
    print("Done!")





#���ر�����ָ֤������
StockData = ts.get_hist_data('sh')
StockData.sort_index().T.to_csv('d://StockFile//sh.csv')
#########################################################################################################








