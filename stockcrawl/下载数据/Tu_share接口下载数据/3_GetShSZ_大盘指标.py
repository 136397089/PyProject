
import pandas as pd
import os
import datetime
import tushare as ts
import numpy as np


if __name__=="__main__":
    cur = datetime.datetime.now()
    OriginalDay = '1997-01-01'
    today = str(cur.year) + '-' + str(cur.month) + '-' + str(cur.day)
    data = ts.get_k_data('sh',start=OriginalDay, end=today).set_index(['date']).sort_index()
    data.columns.name = 'date'
    data.T.to_csv('d://StockFile//whole//sh.csv')
    
    data = ts.get_k_data('sz',start=OriginalDay, end=today).set_index(['date']).sort_index()
    data.columns.name = 'date'
    data.T.to_csv('d://StockFile//whole//sz.csv')
    
    data = ts.get_k_data('399006',start=OriginalDay, end=today).set_index(['date']).sort_index()
    data.columns.name = 'date'
    data.T.to_csv('d://StockFile//whole//CYB.csv')
    
    data = ts.get_k_data('399005',start=OriginalDay, end=today).set_index(['date']).sort_index()
    data.columns.name = 'date'
    data.T.to_csv('d://StockFile//whole//ZXB.csv')
    
    # data = ts.get_k_data('sh50',start=OriginalDay, end=today).set_index(['date']).sort_index()
    # data.columns.name = 'date'
    # data.T.to_csv('d://StockFile//whole//sh50.csv')
	





