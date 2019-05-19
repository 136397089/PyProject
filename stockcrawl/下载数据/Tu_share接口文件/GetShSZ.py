
import pandas as pd
import os
import datetime
import tushare as ts
import numpy as np


if __name__=="__main__":
    cur = datetime.datetime.now()
    OriginalDay = '1997-01-01'
    today = str(cur.year) + '-' + str(cur.month) + '-' + str(cur.day)
    ts.get_k_data('sh',start=OriginalDay, end=today).sort_index().T.to_csv('d://StockFile//whole//sh.csv')
    ts.get_k_data('sz',start=OriginalDay, end=today).sort_index().T.to_csv('d://StockFile//whole//sz.csv')
    ts.get_k_data('399006',start=OriginalDay, end=today).sort_index().T.to_csv('d://StockFile//whole//CYB.csv')
    ts.get_k_data('399005',start=OriginalDay, end=today).sort_index().T.to_csv('d://StockFile//whole//ZXB.csv')
    ts.get_k_data('sh50',start=OriginalDay, end=today).sort_index().T.to_csv('d://StockFile//whole//sh50.csv')





