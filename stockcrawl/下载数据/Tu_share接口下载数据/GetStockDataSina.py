import pandas as pd
import re
import requests
import time
import datetime
from sqlalchemy import create_engine
import os
import threading
from requests.adapters import HTTPAdapter

emptydata=[]
getmin = lambda x: x.min()
getmax = lambda x: x.max()
engine = create_engine('mysql://root:@localhost/stockdata?charset=utf8')  # 连接数据库
#'u1','u2'无用
columnsList=['code', 'name', 'open', 'frontclose', 'current', 'high', 'low', 'buy', 'sell', 'amount', 'volume', 'buynumber1', 'buy1', 'buynumber2', 'buy2', 'buynumber3', 'buy3', 'buynumber4', 'buy4', 'buynumber5', 'buy5', 'sellnumber1', 'sell1', 'sellnumber2', 'sell2', 'sellnumber3', 'sell3', 'sellnumber4', 'sell4', 'sellnumber5', 'sell5', 'datetime']
#含义
#'股票代码','股票名字','今日开盘价','昨日收盘价','当前价格','今日最高价','今日最低价','竞买价，即“买一“报价','竞卖价，即“卖一“报价',
#'成交的股票数，由于股票交易以一百股为基本单位，所以在使用时，通常把该值除以一百','成交金额，单位为“元“，为了一目了然，通常以“万元“为成交金额的单位，所以通常把该值除以一万',
#'买一申请624253股，即6243手','买一报价','买二申报股数','买二报价','买三申报股数','买三报价','买四申报股数','买四报价','买五申报股数','买五报价','卖一申报股数','卖一报价','卖二申报股数','卖二报价','卖三申报股数','卖三报价','卖四申报股数','卖四报价','卖五申报股数','卖五报价','"日期"','时间',

#
releaseCodeCile = 'D:\\StockFile\\whole\\AllCompanyCode_Sina.csv'
debugCodeFile = 'D:\\\StockFile\\AllCompanyCode_Sina_debug.csv'
codefile = releaseCodeCile
#下载所以股票的
def GetAllDStockData():
    filedata = pd.read_csv(codefile)#本地股票代码路径
    filedata.set_index(['Unnamed: 0'],inplace=True)
    allstockCoed=''#上证指数代码
    codenumber=0
    alldata=[]
    for stockname in filedata.values:
        data = stockname[0].split('.')
        newstock = data[1] + data[0]
        allstockCoed = allstockCoed+','+newstock
        codenumber = codenumber+1
        if codenumber > 100:
            alldata = alldata + GetStockDataSig(allstockCoed.lower())
            allstockCoed=''
            codenumber = 0
    alldata = alldata + GetStockDataSig(allstockCoed.lower())
    listdata=[]
    for strlist in alldata:
        splitdata=re.split(',|_|=',strlist.replace('sh','').replace('sz',''))
        if len(splitdata) < len(columnsList):
            continue
        splitdata = splitdata[2:-1]
        splitdata[-2] = splitdata[-2] + ' ' + splitdata[-1]
        #splitdata[-2] = pd.datetime.strptime(splitdata[-2] + ' ' + splitdata[-1],'%Y-%m-%d %H:%M:%S')
        listdata.append(splitdata[:-1])
    alldata=pd.DataFrame(listdata,columns=columnsList)
    alldata['code'] = alldata['code'].astype(int)
    alldata.set_index(['code'],inplace=True)
    alldata.drop(['name'], axis=1,inplace=True)
    alldata.dropna(inplace=True)
    alldata[['open', 'frontclose', 'current', 'high', 'low', 'amount', 'volume']] = alldata[['open', 'frontclose', 'current', 'high', 'low', 'amount', 'volume']].astype(float)
    return alldata[['open', 'frontclose', 'current', 'high', 'low', 'volume','datetime']]



#下载单个股票的数据
def GetStockDataSig(stockName):
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=5))
    s.mount('https://', HTTPAdapter(max_retries=5))
    try:
        r = s.get('http://hq.sinajs.cn/list=' +stockName, timeout=5)
    except requests.exceptions.RequestException as e:
        print(e)
        print(time.strftime('%Y-%m-%d %H:%M:%S'))
    r = s.get('http://hq.sinajs.cn/list=' +stockName)
    res = r.text.split(";\n")
    return res[:-1]

#调试，读文件的的数据
#def GetStockDataSig(stockName):
#    f = open("D:\\StockFile\\debugdata.csv",'r', encoding='UTF-8')
#    res = f.read()
#    f.close()
#    res = res.split(";")
#    return res[:-1]


#

#
def DataRecord():
    curTime = datetime.datetime.now()
    MorningBegin = datetime.datetime(curTime.year, curTime.month, curTime.day, 9, 29, 0)
    AfternoonEnd = datetime.datetime(curTime.year, curTime.month, curTime.day, 15, 10, 0)
    while curTime < MorningBegin:
        print('Wait for ' + MorningBegin.strftime('%Y_%m_%d_%H_%M'))
        time.sleep(10)
        curTime = datetime.datetime.now()
    recordData= pd.DataFrame(columns=['code', 'type', 'time', 'open', 'high', 'low', 'close', 'volume'])
    data = GetAllDStockData()
    emptydata = data[['open','current','high','low','volume','datetime']].copy(deep=True)
    emptydata.rename(columns={'current': 'close'}, inplace=True)
    emptydata.loc[:,:] = 0
    GroupData={}
    i = 0
    while True:
        data = GetAllDStockData()
        RefleshData(GroupData, data,emptydata)
        i +=1
        print("Round%d : Wait 5s"%i)
        time.sleep(5)
        curTime = datetime.datetime.now()
        if curTime > AfternoonEnd:
            print(curTime)
            return
    return GroupData

#根据新数据更新之前的价格记录
def RefleshData(CurrentGroupData,ResourceData,emptydata):
    [GroupIndex,FrontIndex] = GetListTimeIndex(30, ResourceData['datetime'])
    if GroupIndex == False:
        return
    if GroupIndex not in CurrentGroupData.keys():
        CurrentGroupData[GroupIndex] = emptydata.copy(deep=True)
        CurrentGroupData[GroupIndex][['close', 'low', 'high']] = ResourceData[['current', 'current', 'current']]
    CurrentGroupData[GroupIndex]['close'] = ResourceData['current']
    CurrentGroupData[GroupIndex]['low'] = CurrentGroupData[GroupIndex][['close','low']].apply(getmin,axis=1)
    CurrentGroupData[GroupIndex]['high'] = CurrentGroupData[GroupIndex][['close','high']].apply(getmax,axis=1)
    if FrontIndex not in CurrentGroupData.keys():
        CurrentGroupData[GroupIndex]['volume'] = ResourceData['volume']
        CurrentGroupData[GroupIndex]['open'] = ResourceData['frontclose']
    else:
        CurrentGroupData[GroupIndex]['volume'] = ResourceData['volume'] - CurrentGroupData[FrontIndex]['volume']
        CurrentGroupData[GroupIndex]['open'] = CurrentGroupData[FrontIndex]['close']
    CurrentGroupData[GroupIndex]['datetime'] = GroupIndex
    #CurrentGroupData[GroupIndex].to_csv('D:\\StockFile\\CurrentTemp\\'+'Type30_'+ GroupIndex.strftime('%Y_%m_%d_%H_%M')+'.csv')
    CurrentGroupData[GroupIndex].to_sql('cycletype30_'+ GroupIndex.strftime('%Y_%m_%d_%H_%M'),engine,if_exists='replace')



#计算时间点
def GetListTimeIndex(Timetype ,timeList):
    curTime = datetime.datetime.now()
    for sigTime in timeList:
        date_time = datetime.datetime.strptime(sigTime, '%Y-%m-%d %H:%M:%S')
        if (date_time.year == curTime.year and date_time.month == curTime.month and date_time.day == curTime.day) or True:
            date_time = GetTimeIndex(Timetype,date_time)
            return date_time
    return [False,False]

def GetTimeIndex(inputtype,inputTime):
    # 开盘收盘时间
    curTime = datetime.datetime.now()
    MorningBegin = datetime.datetime(curTime.year, curTime.month, curTime.day, 9, 30, 0)
    MorningEnd = datetime.datetime(curTime.year, curTime.month, curTime.day, 11, 30, 0)
    AfternoonBegin = datetime.datetime(curTime.year, curTime.month, curTime.day, 13, 0, 0)
    AfternoonEnd = datetime.datetime(curTime.year, curTime.month, curTime.day, 15, 0, 0)
    groupTime = inputTime
    if groupTime < MorningBegin:
        groupTime = MorningBegin + datetime.timedelta(minutes = inputtype)
    elif groupTime > MorningEnd and groupTime < AfternoonBegin:
        groupTime = MorningEnd
    elif groupTime > AfternoonEnd:
        groupTime = AfternoonEnd
    elif (groupTime > MorningBegin and groupTime < MorningEnd) or (groupTime > AfternoonBegin and groupTime < AfternoonEnd):
        timeMinute = (int((inputTime.minute)/inputtype)+1)*inputtype
        if timeMinute == 60:
            groupTime = datetime.datetime(inputTime.year, inputTime.month, inputTime.day, inputTime.hour+1, 0, 0)
        else:
            groupTime = datetime.datetime(inputTime.year,inputTime.month,inputTime.day,inputTime.hour,timeMinute,0)
    frontTime = groupTime-datetime.timedelta(minutes = inputtype)
    if frontTime <= AfternoonBegin and frontTime >= MorningEnd:
        frontTime = MorningEnd - datetime.timedelta(minutes = inputtype)
    return [groupTime,frontTime]

if __name__=="__main__":
    DataRecord()




