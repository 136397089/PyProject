# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 00:03:46 2018
@author: South
"""
import os
import datetime
from datetime import datetime
import tushare as ts
import numpy as np
import pandas as pd
import MySQLdb
from sqlalchemy import create_engine

if __name__=="__main__":
    DDD=''




codeFile='D:\\StockFile\\whole\\AllCompanyCode.csv'
def GetTop10Holder(mFilename,startDate,endDate):
    engine = create_engine('mysql://root:@localhost/Financedata?charset=utf8')  # 连接数据库
    codes= pd.read_csv(mFilename)
    pro = ts.pro_api()
    for codename in codes['ts_code']:
        df = pro.top10_floatholders(ts_code=codename, start_date=startDate, end_date=endDate)
        df.to_csv('D:\\StockFile\\HolderData\\' + codename+'.csv',encoding='utf_8_sig')
        #df.to_sql(codename, engine, if_exists='append')
        datetime.sleep(1)