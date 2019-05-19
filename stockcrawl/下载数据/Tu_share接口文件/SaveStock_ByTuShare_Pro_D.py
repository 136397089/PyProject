# -*- coding:utf-8 -*-
import pandas as pd
import os
import datetime
from datetime import datetime
import tushare as ts
import numpy as np

# 最后合并的数据出错，需要进一步整理
# 需要有一个可以方便显示数据拆线图的工具
DataFile = 'd:\\StockFile\\AllCompanyCode.csv'
TestFile = 'D:\\StockFile\\StockData_D_Pro'
OriginalDay = '19910101'
StockDatapath = 'd:\\StockFile\\StockData_D_h1991'
StockDatapathW = 'd:\\StockFile\\StockData_W_h'
StockDatapathM = 'd:\\StockFile\\StockData_M_h'

if __name__ == "__main__":


# 下载保存上证指数数据
StockData = ts.get_hist_data('sh')
StockData.sort_index().T.to_csv('d://StockFile//sh.csv')
#########################################################################################################








