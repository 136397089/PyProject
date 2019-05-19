import pandas as pd
import tushare as ts
import numpy as np
import datetime
import time
import os
import MySQLdb
from sqlalchemy import create_engine



FunPath='D:\\StockFile\\whole\\FundData\\'

#下载所有基金的持仓记录
def GetfundAndSave():
    FunPath = 'D:\\StockFile\\whole\\FundData\\'#基金持仓记录保存的文件夹
    pro = ts.pro_api()
    fundList = pro.fund_basic(market='o')
    for num in fundList['ts_code']:
        try:
            pro.fund_portfolio(ts_code=num).to_csv(FunPath + num+'.csv',encoding='utf_8_sig')#保存为csv文件
            time.sleep(1)
        except IOError:
            print(num + 'error')
        else:
            print(num+' finish')



def StaticFileData(filename,stockDict):
    cur = datetime.datetime.now()
    filedata = pd.read_csv(filename).drop(['Unnamed: 0'], axis=1)
    if (len(filedata) == 0):  # 如果基金的持仓数据为空，则进行下个基金的数据统计
        print(filename+':File data is empty.')
        return
    if(filedata['end_date'].max() < cur.year*10000):
        return
    filedata = filedata.groupby('end_date').get_group(filedata['end_date'].max())
    top5Data = filedata.sort_values(axis=0, ascending=False, by='mkv')[0:5]#只统计每个基金前5个重仓股
    for stockCode in top5Data['symbol']:
        if stockCode.find('SH') > 0 or stockCode.find('SZ') > 0:
            if stockCode[0:6] not in stockDict.keys():
                stockDict[stockCode[0:6]] = 1
            else:
                stockDict[stockCode[0:6]] += 1
    return stockDict

filePath = 'D:\\StockFile\\whole\\FundData\\'
filePathtemp = 'D:\\StockFile\\whole\\Fundatatemp\\'

def GetTopStockFromFund(FundDatafilePath):
    codeCount={}
    for filename in os.listdir(FundDatafilePath):
        StaticFileData(FundDatafilePath+filename, codeCount)
    codeCount = pd.DataFrame.from_dict(codeCount, orient='index')
    codeCount = codeCount.rename(columns={0:'count'})
    codeCount = codeCount.sort_values(axis=0, ascending=False, by='count')
    codeCount.to_csv('D:\\StockFile\\whole\\FundCount.csv')
    codeCount.insert(0, 'code', codeCount.index)
    codeCount.index = pd.core.indexes.range.RangeIndex(start=0, stop=len(codeCount), step=1)
    engine = create_engine('mysql://root:@localhost/Financedata?charset=utf8')
    codeCount.to_sql('fundstockcount_2019_03_31',engine)
    return (codeCount)

if __name__=="__main__":
    GetTopStockFromFund(filePath)


#for filename in os.listdir(filePathtemp):
#    filedata = pd.read_csv(filePathtemp+filename).drop(['Unnamed: 0'], axis=1)
#    if (len(filedata) == 0):  # 如果基金的持仓数据为空，则进行下个基金的数据统计
#        continue
#    print(filedata['end_date'].max())