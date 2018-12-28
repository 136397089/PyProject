
#没有验证

import numpy as np
import pandas as pd
 
low='low'
high='high'

def KDJ(date,N=9,M1=3,M2=3):  
    low_list=pd.rolling_min(date[low],N)
    low_list.fillna(value=pd.expanding_min(date[low]),inplace=True)
    high_list=pd.rolling_max(date[high],N)
    high_list.fillna(value=pd.expanding_max(date[high]),inplace=True)
    rsv=(date['close']-low_list)/(high_list-low_list)*100
    date['KDJ_K']=pd.ewma(rsv,com=2)
    date['KDJ_D']=pd.ewma(date['KDJ_K'],com=2)
    date['KDJ_J']=3*date['KDJ_K']-2*date['KDJ_D']


def main():
    a=ts.get_hist_data('000001')
    KDJ(a)


	