import pandas as pd
import os
import datetime
import tushare as ts
import numpy as np

# 最后合并的数据出错，需要进一步整理
# 需要有一个可以方便显示数据拆线图的工具

DataFile = 'd:\\StockFile\\StockCode.csv'
TestFile = 'D:\\StockFile\\test'
OriginalDay = '1991-01-01'
StockDatapath = 'd:\\StockFile\\StockData_D'
StockDatapathW = 'd:\\StockFile\\StockData_W'
StockDatapathM = 'd:\\StockFile\\StockData_M'




if __name__=="__main__":
    CurrentStockData = ts.get_today_all()
    CurrentStockData = CurrentStockData.set_index('code')
    CurrentStockData.to_csv('D:\\StockFile\\whole\\today.csv',encoding='utf_8_sig')





