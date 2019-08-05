import MySQLdb
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
from random import randrange


engine = create_engine('mysql://root:@localhost/stockdata?charset=utf8')
def GetAllReturnRateDate(tablename,engine,NumberT):
	sql = 'select * from '+tablename+' where GroupType0=' + NumberT+ ';'
	stockCode = pd.read_sql_query(sql, engine)
	stockCode.set_index(['CodeName'],inplace=True)
	Tdata=stockCode.T[2:]
	Tdata[Tdata[:]==1000] = np.nan
	Tdata = np.log(Tdata).T
	Tdata = Tdata.dropna(axis=0, how='all')
	return Tdata

def GetLogReturnRateDate(tablename,engine,sotckcode,numbertype):
    sql = 'select * from ' + tablename+' where codename='+sotckcode+' and GroupType0=' + numbertype + ';'
    data = pd.read_sql_query(sql, engine)
    data.set_index(['CodeName'],inplace=True)
    Tdata = data.T[4:]
    Tdata[Tdata[:] == 1000] = np.nan
    return np.log(Tdata)

def GetReturnRateDate(tablename,engine,sotckcode,numbertype):
    sql = 'select * from ' + tablename+' where codename='+sotckcode+' and GroupType0=' + numbertype + ';'
    data = pd.read_sql_query(sql, engine)
    data.set_index(['CodeName'],inplace=True)
    Tdata=data.T[4:]
    Tdata[Tdata[:]==1000] = np.nan
    return Tdata


def GetStatisticalResults(data,codename):
	result = pd.Series([codename,len(data.dropna()),data.min().iloc[0],data.quantile(0.25).iloc[0],data.median().iloc[0],data.quantile(0.75).iloc[0],data.max().iloc[0],data.max().iloc[0]-data.min().iloc[0],data.mean().iloc[0],data.var().iloc[0],data.std().iloc[0],data.std().iloc[0]/data.mean().iloc[0],data.skew().iloc[0],data.kurt().iloc[0]],index=['codename','Count','Min','quantile1-4','Mid','quantile3-4','Max','Range','Mean','Var','Std','CV','Skewness','Kurtosis'])
	return result.to_frame().T.set_index('codename')


def MyPlotFunction(stockmean,titlename):
	plt.rcParams['savefig.dpi'] = 300#图片像素
	plt.rcParams['figure.dpi'] = 300#分辨率
	#stockmean['D2mean'].plot()
	stockmean.plot(linewidth=0.2)
	plt.title(titlename)
	plt.grid()
	plt.show()

	


def GetAllStatisticalResults(numbert,filter=False):
	datas=GetAllReturnRateDate(tablename,engine,numbert)
	meanData=datas.T.mean().to_frame('mean')
	meanData.insert(1,'Count',datas.T.notnull().sum())
	meanData.insert(2,'Min',datas.T.min().to_frame('Min'))
	meanData.insert(3,'quantile2-10',datas.T.quantile(0.2).to_frame('quantile2-10'))
	meanData.insert(4,'Mid',datas.T.median().to_frame('Mid'))
	meanData.insert(5,'quantile8-10',datas.T.quantile(0.8).to_frame('quantile8-10'))
	meanData.insert(6,'Max',datas.T.max().to_frame('Max'))
	meanData.insert(7,'Range',(datas.T.max()-datas.T.min()).to_frame('Range'))
	meanData.insert(8,'Mean',datas.T.mean().to_frame('Mean'))
	meanData.insert(9,'Var',datas.T.var().to_frame('Var'))
	meanData.insert(10,'Std',datas.T.std().to_frame('Std'))
	meanData.insert(10,'Mean-Var',(datas.T.mean()/datas.T.var()).to_frame('Mean-Var'))
	meanData.insert(11,'CV',(datas.T.std()/datas.T.mean()).to_frame('CV'))
	meanData.insert(12,'Skewness',datas.T.skew().to_frame('Skewness'))
	meanData.insert(13,'Kurtosis',datas.T.kurt().to_frame('Kurtosis'))
	if filter:
		meanData = FilterDataBetween(0.3,0.8,'Mean',meanData)
		meanData = FilterDataBetween(0.2,0.8,'Min',meanData)
		meanData = FilterDataBetween(0.2,0.8,'Max',meanData)
		meanData.dropna(axis=0)
	return meanData

def GetSingleStockAndPlot_LogReturnRate(sotckcode,numbertype):
	stockdata = GetLogReturnRateDate(tablename,engine,sotckcode,numbertype)
	stockdata.index = range(0,len(stockdata))
	MyPlotFunction(stockdata.cumsum(),sotckcode)

def GetSingleStockAndPlot(sotckcode,numbertype):
	stockdata = GetReturnRateDate(tablename,engine,sotckcode,numbertype)
	stockdata.index = range(0,len(stockdata))
	MyPlotFunction(stockdata.cumprod(),sotckcode)


#过滤极大和极小的数据
def FilterDataBetween(beginNode,endNode,TagerColumn,DataInput):
	DataRange = DataInput[TagerColumn]
	Q1 = DataRange.quantile(beginNode)
	Q3 = DataRange.quantile(endNode)
	q1 = Q1-1.5*(Q3-Q1)
	q3 = Q3+1.5*(Q3-Q1)
	returnData = DataInput[DataRange.between(q1, q3)]
	return returnData

#求移动平均值
def GetMoveMa(data,N):
	n=np.ones(N)
	weights=n/N
	sma=np.convolve(weights,data)[N-1:-N+1]
	return sma

def GetCloumnsMoveMa(data,N):
	data.index = range(0,len(data))
	data.dropna()
	data.index.name = 'CodeName'
	n = np.ones(N)
	weights = n/N
	returnData = data.index.to_frame('CodeName')
	for colName in data.columns:
		sma = np.convolve(weights,data[colName])[N-1:-N+1]
		returnData[colName] = pd.DataFrame(sma,index=data.index[N-1:])
	returnData.set_index('CodeName',inplace=True)
	return returnData

def RunData(columnsType,N):
	DataCombin = datas1[columnsType].to_frame(Group1)
	#DataCombin[Group2] = datas2[columnsType]
	#DataCombin[Group3] = datas3[columnsType]
	DataCombin.index=range(0,len(DataCombin))
	DataCombin.index.name='CodeName'
	MyPlotFunction(DataCombin,columnsType)
	#MyPlotFunction(GetCloumnsMoveMa(DataCombin,N),columnsType)

#主要调用函数
def ChackDataAndPlot(TGroup):
	datas = GetAllStatisticalResults(TGroup,filter=False)
	#MyPlotFunction(GetCloumnsMoveMa(datas.loc[:,['Count']],2),TGroup+'_'+TNP+'_'+TpriceType)
	#MyPlotFunction(GetCloumnsMoveMa(datas.loc[:,['Mean-Var']],2),TGroup+'_'+TNP+'_'+TpriceType)
	MyPlotFunction(GetCloumnsMoveMa(datas.loc[:,['Mean','Min','quantile2-10','quantile8-10','Max','Mid']],20),"Group_"+TGroup)

#将全部的收益率拼接起来计算统计量
def GetAllDataIndex(_tablename,_engine,_Group1):
    datas = GetAllReturnRateDate(_tablename,_engine,_Group1)
    newdatas = pd.concat(datas.iloc[:,i] for i in range(datas.shape[1]))
    newdatas = newdatas.dropna()
    dataindex = {}
    dataindex['max'] = newdatas.max()
    dataindex['min'] = newdatas.min()
    dataindex['mean'] = newdatas.mean()
    dataindex['var'] = newdatas.var()
    dataindex['std'] = newdatas.std()
    dataindex['quantile2-10'] = newdatas.quantile(0.2)
    dataindex['mid'] = newdatas.quantile(0.5)
    dataindex['quantile8-10'] = newdatas.quantile(0.8)
    dataindex['Mean-Var'] = (newdatas.mean()/newdatas.var())
    dataindex['count'] = newdatas.size
    for i in dataindex:
        print(i+'\t:   '+str(dataindex[i]))
    return newdatas

def randSum(datalist,count):
	dataSum = 0
	SumList=[]
	for i in range(0,count):
		random_index = randrange(0,len(datalist))
		dataSum = dataSum + (datalist[random_index])
		SumList.append(dataSum)
	return  SumList


def CheckAndSimulation(times):
    data = GetAllDataIndex(tablename,engine,Group1)
    print(randSum(data.values,times)[-1])
    print(randSum(data.values,times)[-1])
    print(randSum(data.values,times)[-1])
    print(randSum(data.values,times)[-1])
    print(randSum(data.values,times)[-1])
    print(randSum(data.values,times)[-1])
    print(randSum(data.values,times)[-1])

###############################
Group1 = '1'
NP1 = '16'
Group1 = '2'
NP1 = '2'
Group3 = '17408'
NP3 = '17408'
Group4 = '272'
NP4 = '272'


closeType = '4'
highType = '1'
lowType = '2'
CLHType = '4026531839'
priceType = CLHType
tablename = 'cdpincomerate'

Group1 = '2'
NP1 = '2'
tablename = 'progrouprate_DIFF_DAY'

datas1 = GetAllStatisticalResults('32768')  # 计算所有股票的统计量
datas1 = GetAllStatisticalResults(Group1)  # 计算所有股票的统计量
ChackDataAndPlot(Group1)


GetCloumnsMoveMa(datas1.loc[:, ['Mean', 'quantile9-10', 'quantile1-10']], 5)
datasH = GetAllStatisticalResults('16777346', '4')  # 计算所有股票的统计量
MyPlotFunction(datasH.loc[:, ['Mean', 'quantile9-10', 'quantile1-10']], 'Mean')

datas1 = GetAllStatisticalResults('16777346', '1')  # 计算所有股票的统计量
MyPlotFunction(datas1.loc[:, ['Mean', 'quantile9-10', 'quantile1-10']], 'Mean')
datas1 = GetAllStatisticalResults('2', '2', priceType)  #





MyPlotFunction(GetCloumnsMoveMa(datas1.loc[:, ['Mean', 'Min', 'quantile1-10', 'quantile9-10', 'Max']], 60),
			   Group1 + '_' + NP1 + '_' + priceType)
MyPlotFunction(GetCloumnsMoveMa(datas3.loc[:, ['Mean-Std']], 5), 'Count')


GetSingleStockAndPlot('1', Group1)  # 绘制单个股票的收益率曲线图
GetSingleStockAndPlot_LogReturnRate('20', Group1, NP1, '4026531839')  # 绘制单个股票的收益率曲线图
