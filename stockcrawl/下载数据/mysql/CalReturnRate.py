import MySQLdb
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import MySQLdb




def GetAllDate(tablename,engine):
    sql = 'select * from ' + tablename+' ; '
    data = pd.read_sql_query(sql, engine)
    data.set_index(['indexname'],inplace=True)
    return data


def InsertChangeRate(tablename,engine,cursor):
    datas = GetAllDate(tablename,engine)
    Frontdata = datas[0:len(datas)-1]['close']
    CurrentData=datas[1:len(datas)]['close']
    Frontdata.index = CurrentData.index
    rate = ((CurrentData / Frontdata) - 1) * 100
    datas['changerate']=0
    datas['changerate'] = datas['changerate']+rate
    sql = 'drop table '+tablename+';'
    cursor.execute(sql)
    datas.to_sql(tablename,engine)


def UopdateChangeRate():
    engine = create_engine('mysql://root:@localhost/stockdata?charset=utf8')
    databaseConnect = MySQLdb.connect("localhost", "root", "", "stockdata", charset='utf8')
    cursor = databaseConnect.cursor()
    sql = 'show tables;'
    tables = pd.read_sql_query(sql, engine)
    for tablename in tables['Tables_in_stockdata']:
        if tablename.find('_day_data') > 0:
            print(tablename)
            InsertChangeRate(tablename,engine,cursor)
    cursor.close()
    databaseConnect.close()


###############################
sql = 'select close from 000001_data_freq;'
engine = create_engine('mysql://root:@localhost/stockdata?charset=utf8')
db = MySQLdb.connect("localhost", "root", "", "stockdata", charset='utf8')
cursor = db.cursor()

