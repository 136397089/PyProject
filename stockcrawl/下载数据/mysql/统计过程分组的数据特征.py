import MySQLdb
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
from random import randrange


engine = create_engine('mysql://root:@localhost/stockdata?charset=utf8')
def GetAllLogReturnRateDate(tablename,engine,NumberT,Rate=1):
	GroupTypeStr=' where GroupType0='+str(NumberT[0])
	for i in range(1,len(NumberT)):
		GroupTypeStr = GroupTypeStr + ' and ' + 'GroupType'+str(i) + '=' + str(NumberT[i])
	sql = 'select * from '+tablename + GroupTypeStr + ';'
	stockCode = pd.read_sql_query(sql, engine)
	stockCode.set_index(['CodeName'],inplace=True)
	Tdata=stockCode.T[len(NumberT)+1:]
	Tdata[Tdata[:]==1000] = np.nan
	Tdata=(Tdata-1)*Rate+1
	Tdata = np.log(Tdata).T
	Tdata = Tdata[~(Tdata[:] < -10)]
	return Tdata

def GetLogReturnRateDate(tablename,engine,sotckcode,NumberT):
	GroupTypeStr=' where GroupType0='+str(NumberT[0])
	for i in range(1,len(NumberT)):
		GroupTypeStr = GroupTypeStr + ' and ' + 'GroupType'+str(i) + '=' + str(NumberT[i])
	sql = 'select * from '+tablename + GroupTypeStr + ';'
	data = pd.read_sql_query(sql, engine)
	data.set_index(['CodeName'],inplace=True)
	Tdata = data.T[len(NumberT)+1::]
	Tdata[Tdata[:] == 1000] = np.nan
	return np.log(Tdata)

def GetReturnRateDate(tablename,engine,sotckcode,NumberT):
	GroupTypeStr=' where GroupType0='+str(NumberT[0])
	for i in range(1,len(NumberT)):
		GroupTypeStr = GroupTypeStr + ' and ' + 'GroupType'+str(i) + '=' + str(NumberT[i])
	sql = 'select * from '+tablename + GroupTypeStr + ';'
	data = pd.read_sql_query(sql, engine)
	data.set_index(['CodeName'],inplace=True)
	Tdata=data.T[len(NumberT)+1::]
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

	


def GetAllStatisticalResults(tablename,numbert,filter=False):
	datas=GetAllLogReturnRateDate(tablename,engine,numbert)
	meanData=datas.T.mean().to_frame('mean')
	meanData.insert(1,'Count',datas.T.notnull().sum())
	meanData.insert(2,'Min',datas.T.min().to_frame('Min'))
	meanData.insert(3,'quantile1-10',datas.T.quantile(0.1).to_frame('quantile2-10'))
	meanData.insert(3,'quantile2-10',datas.T.quantile(0.2).to_frame('quantile2-10'))
	meanData.insert(4,'Mid',datas.T.median().to_frame('Mid'))
	meanData.insert(5,'quantile8-10',datas.T.quantile(0.8).to_frame('quantile8-10'))
	meanData.insert(5,'quantile9-10',datas.T.quantile(0.9).to_frame('quantile8-10'))
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
def ChackDataAndPlot(tablename,TGroup,MapTittle):
	datas = GetAllStatisticalResults(tablename,TGroup,filter=False)
	print("Get Data Finished")
	#MyPlotFunction(GetCloumnsMoveMa(datas.loc[:,['Count']],2),TGroup+'_'+TNP+'_'+TpriceType)
	#MyPlotFunction(GetCloumnsMoveMa(datas.loc[:,['Mean-Std']],2),TGroup+'_'+TNP+'_'+TpriceType)
	MyPlotFunction(GetCloumnsMoveMa(datas.loc[:,['Mean','Min','quantile1-10','quantile2-10','quantile8-10','quantile9-10','Max','Mid']],20),MapTittle)

#主要调用函数
def ChackMean_StdAndPlot(tablename,TGroup,TNP,TpriceType):
	datas = GetAllStatisticalResults(tablename,TGroup,TNP,TpriceType,filter=False)
	datas.index = range(0,len(datas))
	datas.dropna()
	datas.index.name = 'CodeName'
	MyPlotFunction(datas.loc[:,['Mean-Var']],TGroup+'_'+TNP+'_'+TpriceType)

#将全部的收益率拼接起来计算统计量
def GetAllDataIndex(_tablename,_engine,_Group1,_Rate=1):
	data = GetAllLogReturnRateDate(_tablename,_engine,_Group1,_Rate)
	newdatas = pd.concat(data.iloc[:,i] for i in range(data.shape[1]))
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
	return [newdatas,dataindex['Mean-Var']]

def randSum(datalist,count):
	dataSum = 0
	SumList=[0]
	for i in range(0,count):
		random_index = randrange(0,len(datalist))
		dataSum = dataSum + (datalist[random_index])
		SumList.append(dataSum)
	return  SumList

def CheckAndSimulation(tablename,GroupType):
	[data,meanVar] = GetAllDataIndex(tablename,engine,GroupType)#
	randList = []
	LastresultList = []
	AnaTime = 1000
	rangeTime = 30
	for i in range(0,rangeTime):
		randList.append(randSum(data.values,AnaTime))
	i = 1
	dfdata = pd.DataFrame(index=range(0,AnaTime+1))
	for OneList in randList:
		LastresultList.append(OneList[-1])
		dfdata.insert(0,'L'+str(i),OneList)
		i = i+1
	print(LastresultList)
	MyPlotFunction(dfdata,'Res_inComeRate')
	[data,meanVar] = GetAllDataIndex(tablename,engine,GroupType,meanVar)#
	randList = []
	LastresultList = []
	for i in range(0,rangeTime):
		randList.append(randSum(data.values,AnaTime))
	i = 1
	dfdata = pd.DataFrame(index=range(0,AnaTime+1))
	for OneList in randList:
		LastresultList.append(OneList[-1])
		dfdata.insert(0,'L'+str(i),OneList)
		i = i+1
	print(LastresultList)
	MyPlotFunction(dfdata,'inComeRate')

###############################




_Mid2MidType = str(1 << 0)
_BClose = str(1 << 1)
_BHigh = str(1 << 2)
_BLow = str(1 << 3)
_BFClose = str(1 << 4)
_BFHigh = str(1 << 5)
_BFLow  = str(1 << 6)
_EHigh = str(1 << 7)
_EClose = str(1 << 8)
_ELow = str(1 << 9)
_EFClose = str(1 << 10)
_EFHigh = str(1 << 11)
_EFLow = str(1 << 12)
_Max = str(1 << 13)
_Min = str(1 << 14)

priceType = _Mid2MidType

# 收益结果比较好的几个类型
tablename='progrouprate45056'
GroupType=(0,0,0,0,56,56,0,0,0,0,0,0,0,0,0,0,1)
ChackDataAndPlot('progrouprate45056',GroupType,'111')
CheckAndSimulation('progrouprate45056',(0,0,0,0,56,56,0,0,0,0,0,0,0,0,0,0,1))
CheckAndSimulation('progrouprate34816',(0,0,0,0,34816,34816,0,0,0,0,2048,2048,0,0,0,0,1))
CheckAndSimulation('progrouprate45056',(0,0,32768,32768,32768,32768,0,0,0,0,0,0,0,0,0,0,1))
CheckAndSimulation('progrouprate45056',(0,0,0,0,56,56,0,0,0,0,64,64,0,0,0,0,1))
CheckAndSimulation('progrouprate45056',(0,0,64,64,64,64,0,0,0,0,64,64,0,0,0,0,1))
CheckAndSimulation('progrouprate45056',(0,0,32768,32768,32768,32768,0,0,0,0,64,64,0,0,0,0,1))
CheckAndSimulation('progrouprate45056',(0,0,32832,32832,32768,32768,0,0,0,0,64,64,0,0,0,0,1))
CheckAndSimulation('progrouprate45056',(0,0,32832,32832,32768,32768,0,0,0,0,64,64,0,0,0,0,1))

sels

CheckAndSimulation('cdpincomerate',[1])
ChackDataAndPlot('cdpincomerate',[1],'111')



data = GetAllLogReturnRateDate('progrouprate45056',engine,GroupType)




