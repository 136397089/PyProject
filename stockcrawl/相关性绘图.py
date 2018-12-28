
import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline


#ts.get_hist_data('sh'）#获取上证指数k线数据，其它参数与个股一致，下同
#ts.get_hist_data('sz'）#获取深圳成指k线数据
#ts.get_hist_data('hs300'）#获取沪深300指数k线数据
#ts.get_hist_data('sz50'）#获取上证50指数k线数据
#ts.get_hist_data('zxb'）#获取中小板指数k线数据
#ts.get_hist_data('cyb'）#获取创业板指数k线数据

#get_h_data调用数据
def Relevanceplot(tagecode,stockcode,shindex):
    quotes = ts.get_h_data(tagecode,start='2000-01-01', end='2017-06-15')
    sh = ts.get_h_data(stockcode,index=True,start='2000-01-01', end='2017-06-15')
    quotes.rename(columns={shindex:'stock'},inplace = True)
    alldata = sh.join(quotes['stock'])
    tempall = alldata.dropna(axis=0,how='any')#df.dropna()：删除所有包含空值的行
    plt.scatter(tempall[shindex],tempall['stock'])
    model=pd.ols(y=tempall[shindex],x=tempall['stock'])
    print model
    alldata = alldata.loc[:,[shindex, 'stock']]
    return [alldata,alldata[alldata['stock'].isnull()]]

#get_hist_datay调用数据
def Relevanceplot(tagecode,stockcode,shindex):
    quotes = ts.get_hist_data(tagecode)
    sh = ts.get_hist_data(stockcode)
    quotes.rename(columns={shindex:'stock'},inplace = True)
    alldata = sh.join(quotes['stock'])
    tempall = alldata.dropna(axis=0,how='any')#df.dropna()：删除所有包含空值的行
    plt.scatter(tempall[shindex],tempall['stock'],vmin=0, vmax=20, s=35, cmap=cm)
    model=pd.ols(y=tempall[shindex],x=tempall['stock'])
    print model
    alldata = alldata.loc[:,[shindex, 'stock']]#只取[shindex, 'stock']两列
    return [alldata,alldata[alldata['stock'].isnull()],model]#
	
#Read_Csv_File调用数据
def RelevanceplotFromCSV(tagecode,stockcode,shindex):
    quotes = Read_Csv_File('D:\\StockFile\\StockData\\'+tagecode+'.csv')
    sh = Read_Csv_File('D:\\StockFile\\StockData\\'+stockcode+'.csv')
    quotes.rename(columns={shindex:'stock'},inplace = True)
    alldata = sh.join(quotes['stock'])
    tempall = alldata.dropna(axis=0,how='any')#df.dropna()：删除所有包含空值的行
    plt.scatter(tempall[shindex],tempall['stock'])
    model=pd.ols(y=tempall[shindex],x=tempall['stock'])
    print model
    alldata = alldata.loc[:,[shindex, 'stock']]
    return [alldata,alldata[alldata['stock'].isnull()]]
	
def Read_Csv_File(mFilename):
    filedata = pd.read_csv(mFilename).T
    filedata.columns = filedata.ix[0]#columns更新为首行
    filedata.index.name = 'date'
    filedata.columns.name = None
    filedata = filedata.ix[filedata.index[1:-1]]#去除首行
    filedata = filedata.drop_duplicates()#去除重复
    return filedata
	
	
	
	