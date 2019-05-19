import MySQLdb
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

def DataFramePlot(stockmean,titlename):
    Data = pd.Series(stockmean).sort_values()
    plt.plot(range(0, len(Data)), Data.values)
    plt.title(titlename)
    plt.grid()
    plt.show()

def XYDataPlot(xList,yList,titlename):
    plt.plot(xList, yList,'ro')
    plt.title(titlename)
    plt.grid()
    plt.show()

def PushDataFromTable(tablename,NumType,engine,ResourceData):
    sql = "select count,CRType,mean,var from " + tablename + " where Numtype=" + NumType + " and NPType=" + NumType + " and count<>0; "
    data = pd.read_sql_query(sql, engine)
    for i in data.index:
        ResourceData[tablename + 'Group' + str(i)] = (data.loc[i]['mean'])#math.log/100 + 1
    return ResourceData


#读取所有股票的NumType分组收益率，并显示
def GetAllMeanFromFreqTables(NumType):
    engine = create_engine('mysql://root:@localhost/stockdata?charset=utf8')
    sql = 'show tables;'
    stockmean={}
    tables = pd.read_sql_query(sql, engine)
    for tablename in tables['Tables_in_stockdata']:
        if tablename.find('_freqdata') > 0:
            stockmean = PushDataFromTable(tablename, NumType, engine, stockmean)
    DataFramePlot(stockmean,NumType)
    Data = pd.Series(stockmean).sort_values()
    return  Data

#从tablesList中读取股票的NumType分组收益率，并显示
def GetAllMeanFromTablesList(NumType,tablesList):
    engine = create_engine('mysql://root:@localhost/stockdata?charset=utf8')
    stockmean={}
    sql = 'show tables;'
    tables = pd.read_sql_query(sql, engine)
    for tablename in tablesList['code']:
        if len( np.where(tables==(tablename +'_freqdata'))[0] ) > 0:
            stockmean = PushDataFromTable(tablename+'_freqdata', NumType, engine, stockmean)
    DataFramePlot(stockmean,NumType+'_List')
    Data = pd.Series(stockmean).sort_values()
    return  Data

#读取基金公司的股票列表
def GetFunStockCodeList():
    engine = create_engine('mysql://root:@localhost/financedata?charset=utf8')
    sql = 'select code from fundstockcount_2019_03_31 where count > 20;'
    tables = pd.read_sql_query(sql, engine)
    return tables




###############################################################################################################################################################
#读取单个股票numtype分组的频次数据
def readRateAndFreq(tablesname,numtype,engine):
    sql = 'select * from ' + tablesname + ' where numtype=' + numtype + ' and NPtype=' + numtype + ' and count<>0;'
    tables = pd.read_sql_query(sql, engine)
    tables = tables.drop(['indexname','NumType', 'NPType', 'CRType','Count', 'Mean', 'Var' ],axis=1)
    return tables.sum()


#读取numtype小组的所有收益率频次，并求和
def ReadAllRateFreq(numtype):
    engine = create_engine('mysql://root:@localhost/stockdata?charset=utf8')
    allFreq=readRateAndFreq('000001_freqdata', '0', engine)
    sql = 'show tables;'
    tables = pd.read_sql_query(sql, engine)
    for tablename in tables['Tables_in_stockdata']:
        if tablename.find('_freqdata') > 0:
            #print(tablename)
            allFreq =  allFreq + readRateAndFreq(tablename, numtype, engine)
    return allFreq

#读取基金持仓列表中股票 numtype 小组的收益率频次，并求和
def ReadAllRateFreqFromList(numtype,tableList):
    engine = create_engine('mysql://root:@localhost/stockdata?charset=utf8')
    allFreq=readRateAndFreq('000001_freqdata', '0', engine)
    sql = 'show tables;'
    tables = pd.read_sql_query(sql, engine)
    for tablename in tableList['code']:
        strtablename = str(tablename) + '_freqdata'
        if len(np.where(tables == (tablename + '_freqdata'))[0]) > 0:
            #print(strtablename)
            allFreq =  allFreq + readRateAndFreq(strtablename, numtype, engine)
    return allFreq

#
def PlotAllFreq(numtype):
    AllFreq = ReadAllRateFreq(numtype)
    xIndex=0
    xList=[]
    yList=[]
    i = 0
    for F in AllFreq:
        xIndex = xIndex + F
        xList.append(xIndex)
        yList.append((i-110)*0.1+0.05)
        i = i + 1
    xxList = [ c*100/ xIndex for c in xList]
    XYDataPlot(xxList,yList,numtype)
    sum = 0
    sumup = 0
    for x in range(1,len(xxList)):
        sum = sum + (xxList[x] - xxList[x-1])* abs(yList[x])
        if yList[x] > 0:
            sumup = sumup + (xxList[x] - xxList[x-1]) * yList[x]
    print(sumup / sum)

#
def PlotFundListFreq(numtype):
    GetFunStockCodeList()
    AllFreq = ReadAllRateFreqFromList(numtype,GetFunStockCodeList())
    xIndex=0
    xList=[]
    yList=[]
    i = 0
    for F in AllFreq:
        xIndex = xIndex + F
        xList.append(xIndex)
        yList.append((i-110)*0.1+0.05)
        i = i + 1
    xxList = [c * 100 / xIndex for c in xList]
    XYDataPlot(xxList,yList,numtype+'_List')
    sum = 0
    sumup = 0
    for x in range(1,len(xxList)):
        sum = sum + (xxList[x] - xxList[x-1])* abs(yList[x])
        if yList[x] > 0:
            sumup = sumup + (xxList[x] - xxList[x-1]) * yList[x]
    print(sumup / sum)


def RunDoubleFunction(numtype):
    data = GetAllMeanFromFreqTables(numtype)
    data = GetAllMeanFromTablesList(numtype, GetFunStockCodeList())


