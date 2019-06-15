import MySQLdb
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import MySQLdb
from statsmodels.tsa.stattools import adfuller



#从MYSQL中读收益率数据
def GetChangeRateDate(tablename,engine):
    sql = 'select date,changerate from ' + tablename+' ; '
    data = pd.read_sql_query(sql, engine)
    data.set_index(['date'],inplace=True)
    return data

#平稳化处理
#  一阶差分
def ts_diff(ts):
    return ts.diff(1).dropna(how=any)
#  自然对数
def ts_log(ts):
    return np.log(ts)

#
def GetCloseDate(tablename,engine):
    sql = 'select date,close from ' + tablename+' ; '
    data = pd.read_sql_query(sql, engine)
    data.set_index(['date'],inplace=True)
    return data


#求移动平均值
def GetMoveMa(data,N):
    n=np.ones(N)
    weights=n/N
    sma=np.convolve(weights,data)[N-1:-N+1]
    return sma



#绘图函数
def MyPlotFunction(stockmean,titlename):
    plt.rcParams['savefig.dpi'] = 300#图片像素
    plt.rcParams['figure.dpi'] = 300#分辨率
    plt.plot(range(0, len(stockmean)), stockmean,linewidth=0.5)
    plt.title(titlename)
    plt.grid()
    plt.show()

#
def PlotStockReturnRateDiff(tablename,N,engine):
    shdata = GetChangeRateDate('sh_day_data',engine)
    stockdata = GetChangeRateDate(tablename,engine)
    diferData = (stockdata-shdata).dropna()
    sma = GetMoveMa(diferData['changerate'].values,N)
    MyPlotFunction(sma,tablename+'_diff')

#
def PlotStockReturnRateSum(tablename,engine):
    shdata = GetChangeRateDate('sh_day_data',engine)
    stockdata = GetChangeRateDate(tablename,engine)
    diferData = ((stockdata-shdata).dropna())/100
    sma = diferData['changerate'].cumsum()
    MyPlotFunction(sma,tablename+'_diff')

def PlotStockReturnRateProd(tablename,engine):
    shdata = GetChangeRateDate('sh_day_data',engine)
    stockdata = GetChangeRateDate(tablename,engine)
    diferData = ((stockdata-shdata).dropna())/100+1
    sma = diferData['changerate'].cumprod()
    MyPlotFunction(sma,tablename+'_diff')

#将上证指数的收益率移动平均值显示成图表
def PlotShReturnRate(tablename,N,engine):
    shdata = GetChangeRateDate('sh_day_data',engine)
    stockdata = GetChangeRateDate(tablename,engine)
    diferData = (shdata-stockdata+stockdata).dropna()
    sma = GetMoveMa(diferData['changerate'].values,N)
    MyPlotFunction(sma,tablename+'_diff')


#求相关系数和协方差
def GetCombinData(tablename1,tablename2,engine):
    data1 = GetChangeRateDate(tablename1, engine)
    data2 = GetChangeRateDate(tablename2, engine)
    ComData = pd.concat([data1, data2], axis=1, ignore_index=True).dropna()
    print('pearson相关系数')
    print(ComData.corr())
    print('Kendall Tau相关系数')
    print(ComData.corr('kendall'))
    print('spearman秩相关')
    print(ComData.corr('spearman'))
    print('协方差')
    print(ComData.cov())



#求自相关系数和自协方差
def GetSelfCombinData(tablename1,N,engine,MAn):
    data1 = GetChangeRateDate(tablename1, engine)
    covList=[]
    for n in range(1,N):
        ComData = pd.concat([pd.DataFrame(data1.values[0:len(data1)-n]), pd.DataFrame(data1.values[n:len(data1)])], axis=1, ignore_index=True).dropna()
        covList.append(ComData.corr().loc[0,1])
    covList = GetMoveMa(covList,MAn)
    #covList = pd.DataFrame(covList).cumprod()
    MyPlotFunction(covList,tablename1+'_SelfCorr')
    return covList
    #print('协方差')
    #print(ComData.cov())
    #print('pearson相关系数')
    #print(ComData.corr().loc[0,1])
    #print('Kendall Tau相关系数')
    #print(ComData.corr('kendall'))
    #print('spearman秩相关')
    #print(ComData.corr('spearman'))




#ADF检验
#检验数据平稳性，如果检验输出的 p-value 较大，就表明数据不具有平稳性。
from statsmodels.tsa.stattools import adfuller
def adf_test(ts):
    adftest = adfuller(ts)
    adf_res = pd.Series(adftest[0:4], index=['Test Statistic','p-value','Lags Used','Number of Observations Used'])
    for key, value in adftest[4].items():
        adf_res['Critical Value (%s)' % key] = value
    # adf_res['Lags Used'] 响应的阶数
    return adf_res



import pandas as pd
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import acf,pacf,plot_acf,plot_pacf
from statsmodels.tsa.arima_model import ARMA, ARIMA
#定阶
def get_pdq(time_series):
    plot_acf(time_series)
    plot_pacf(time_series)
    plt.show()
    r,rac,Q = sm.tsa.acf(time_series, qstat=True)
    prac = pacf(time_series,method='ywmle')
    table_data = np.c_[range(1,len(r)), r[1:],rac,prac[1:len(rac)+1],Q]
    table = pd.DataFrame(table_data, columns=['lag', "AC","Q", "PAC", "Prob(>Q)"])
    print(table)


from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
import matplotlib.pyplot as plt

def draw_acf_pacf(ts, w):
    plt.clf()
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    plot_acf(ts, ax = ax1, lags=w)
    ax2 = fig.add_subplot(212)
    plot_pacf(ts, ax=ax2, lags=w)
    plt.show()
    #plt.savefig('./PDF/test_acf_pacf.pdf', format='pdf')




#AR模型预测,w是传入的阶数
from statsmodels.tsa.arima_model import ARMA, ARIMA
def draw_ar(ts, w):
    arma = ARMA(ts, order=(w,0)).fit(disp=-1)
    ts_predict = arma.predict()
    plt.clf()
    plt.plot(ts_predict, label="PDT")
    plt.plot(ts, label = "ORG")
    plt.legend(loc="best")
    plt.title("AR Test %s" % w)
    plt.show()
    return arma#arma.conf_int() 置信水平


def draw_arma(ts, w):
    #ma = ARMA(ts, order=(0, w)).fit(disp = -1)
    #ts_predict_ma = ma.predict()
    arma = ARMA(ts, order=(w,w)).fit(disp=-1)
    ts_predict_ar = arma.predict()
    plt.clf()
    plt.plot(ts_predict_ar, label="AR")
    #plt.plot(ts_predict_ma, label="MA")
    #plt.plot(ts, label = "ORG")
    plt.legend(loc="best")
    plt.title("MA Test %s" % w)
    plt.show()
    #plt.savefig("./PDF/test_ma_"+ str(w) +".pdf", format='pdf')
    return [arma,ts_predict_ar]

#模型预测
def ts_arma(ts, p, q):
    arma = ARMA(ts, order=(p, q)).fit(disp=-1)
    ts_predict_arma = arma.predict()
    return ts_predict_arma

#模型预测
# 加入差分的 ARMA 模型
def ts_arima(ts, p, d, q):
    arima = ARIMA(ts, (0, 1)).fit(disp=-1, maxiter=100)
    ts_predict_arima = arima.predict(start=str(1979), end=str(2010 + 3), dynamic=False)
    return ts_predict_arima

###############################
sql = 'select close from 000001_data_freq;'
engine = create_engine('mysql://root:@localhost/stockdata?charset=utf8')
db = MySQLdb.connect("localhost", "root", "", "stockdata", charset='utf8')
cursor = db.cursor()

PlotStockReturnRateSum('300001_day_data',engine)
PlotStockReturnRateProd('300001_day_data',engine)


plot_acf(GetChangeRateDate('sh_day_data',engine)['changerate'])
