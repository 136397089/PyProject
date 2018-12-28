##2017-06-25
##文件主要功能：python计算MACD数据
##
##
##
##
from pandas import Series, DataFrame
import pandas as pd
import os
import tushare as ts
import pandas.io.data as web
import matplotlib.pyplot as plt
import numpy as np
%matplotlib inline

def getMvgAvg(quotes, points, title):
    quotes[title] = float(0)
    fromindex = quotes.index[-1]
    for n in quotes.index[::-1]:
        if n == quotes.index[-1]:
            quotes[title][n] = 0
        else:
            quotes[title][n] = quotes['close'][n]*(2.0/(float(points)+1.0))+quotes[title][fromindex]*(float(points-1.0)/float(points+1.0))
        fromindex = n

def getDEA(quotes, DiffTitle, EDATitle):
    quotes[EDATitle] = float(0)
    fromindex = quotes.index[-1]
    quotes[EDATitle][-1]=0
    for n in quotes.index[-2::-1]:
        quotes[EDATitle][n] = quotes[EDATitle][fromindex]*(8.0/10.0)+quotes[DiffTitle][n]*(2.0/10.0)
        fromindex = n
	

def getDiff(quotes,title12,title26,title):
    quotes[title]=quotes[title12]-quotes[title26]
	
	
def getBAR(quotes,Title,DiffTitle,EDATitle):
    quotes[Title] = 2*(quotes[DiffTitle]-quotes[EDATitle])

def getMACD(quotes):
    getMvgAvg(quotes,12,'MvgAvg12')
    getMvgAvg(quotes,26,'MvgAvg26')
    getDiff(quotes,'MvgAvg12','MvgAvg26','Diff')
    getDEA(quotes,'Diff','DEA')
    getBAR(quotes,'BAR','Diff','DEA')


def DrawPic(Code):
    quotes=ts.get_hist_data(Code)
    if quotes.size < 100:
        print 'Stock date size is too small.'
        return
    getMACD(quotes)
    plt.figure(figsize=(15,4))
    #plt.plot(range(len(quotes['BAR'][-100::-1])),quotes['BAR'][-100::-1],range(len(quotes['BAR'][-100::-1])),quotes['Diff'][-100::-1])
    plt.bar(np.arange(len(quotes['BAR'][-100::-1])),quotes['BAR'][-100::-1],color='r')
	
#-------------------------------------------------------------------------------
#Main():





