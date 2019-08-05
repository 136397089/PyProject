
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
    data.T.to_csv('d://StockFile//whole//1In_sh.csv')
    
    data = ts.get_k_data('sz',start=OriginalDay, end=today).set_index(['date']).sort_index()
    data.columns.name = 'date'
    data.T.to_csv('d://StockFile//whole//1In_sz.csv')
    
    data = ts.get_k_data('399006',start=OriginalDay, end=today).set_index(['date']).sort_index()
    data.columns.name = 'date'
    data.T.to_csv('d://StockFile//whole//1In_CYB.csv')
    
    data = ts.get_k_data('399005',start=OriginalDay, end=today).set_index(['date']).sort_index()
    data.columns.name = 'date'
    data.T.to_csv('d://StockFile//whole//1In_ZXB.csv')
    
    data = ts.get_k_data('hs300',start=OriginalDay, end=today).set_index(['date']).sort_index()
    data.columns.name = 'date'
    data.T.to_csv('d://StockFile//whole//1In_HS300.csv')
    
    data = ts.get_k_data('sz50',start=OriginalDay, end=today).set_index(['date']).sort_index()
    data.columns.name = 'date'
    data.T.to_csv('d://StockFile//whole//1In_sz50.csv')



def tempfunction():
    ts.get_hist_data('600848', ktype='W') #获取周k线数据
    ts.get_hist_data('600848', ktype='M') #获取月k线数据
    ts.get_hist_data('600848', ktype='5') #获取5分钟k线数据
    ts.get_hist_data('600848', ktype='15') #获取15分钟k线数据
    ts.get_hist_data('600848', ktype='30') #获取30分钟k线数据
    ts.get_hist_data('600848', ktype='60') #获取60分钟k线数据
    ts.get_hist_data('sh')#获取上证指数k线数据，其它参数与个股一致，下同
    ts.get_hist_data('sz')#获取深圳成指k线数据
    ts.get_hist_data('hs300')#获取沪深300指数k线数据
    ts.get_hist_data('sz50')#获取上证50指数k线数据
    ts.get_hist_data('zxb')#获取中小板指数k线数据
    ts.get_hist_data('cyb')#获取创业板指数k线数据
   
   
   
   
   
   
   
