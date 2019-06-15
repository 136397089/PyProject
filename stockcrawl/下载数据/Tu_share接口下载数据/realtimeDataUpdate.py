import MySQLdb
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame
import numpy as np
import math
import MySQLdb
from datetime import datetime


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
    filedata = filedata.drop_duplicates(['close', 'high', 'low', 'open','volume'])  # 去除重复的行
    return filedata


resourceData=DataFrame({'time':[datetime.strptime('1991-1-1 0:0','%Y-%m-%d %H:%M')],'close':[0],'high':[0],'low':[0],'open':[0],'volumw':[0]})
resourceData.set_index(['time'],inplace=True)

resourceData = pd.DataFrame(columns=['time','close','high','open','volumw'])