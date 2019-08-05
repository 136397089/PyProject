import sys
import pandas as pd
import os
import datetime
import tushare as ts
import numpy as np


StockDatapath2 = 'd:\\StockFile\\StockData_30\\000002.csv'
StockDatapath1 = 'd:\\StockFile\\StockData_30\\000001.csv'

# 读CSV文件，转置之后的文件
# mFilename：目标文件名
# 返回值：读出的数据
def Read_Csv_File(mFilename):
	if mFilename.find('csv') == -1:
		return
	filedata = pd.read_csv(mFilename).T
	filedata.columns = filedata.iloc[0]  # columns更新为首行
	if filedata.columns.name != 'date':
		filedata.set_index(['date'], inplace=True)#将date列设置为index
		filedata.columns.name = 'date'
	filedata = filedata.drop(['date'])  # 去除首行
#	filedata = filedata.loc[filedata.index[1:-1]]  # 去除首行
	if filedata.columns.contains('amount'):
		filedata = filedata.drop(['amount'], axis=1)
	if filedata.columns.contains('code'):
		filedata = filedata.drop(['code'], axis=1)
	filedata = filedata.drop_duplicates(['close', 'high', 'low', 'open','volume'])  # 去除重复的行
	return filedata

	
class dataUpdate():
	def __init__(self,ktype):
		self.dalteDay = 0
		self.ktype = ktype
		self.OriginalDay = '1997-01-01'
		self.CodeFile = 'd:\\StockFile\\whole\\StockCode.csv'
	def UpdataStockData(self,FilePath):
		files = os.listdir(FilePath)  # 打开路径文件夹下所有文件
		for dfile in files:
			self.updateFile(FilePath + '\\' + dfile,dfile[0:6])
		print("Done!")
	def updateFile(self,FilePath,StockCode):
		print(StockCode+' begin.')
		filedata = Read_Csv_File(FilePath)  # 读取每个文件的数据
		filedata = filedata[:-1]
		lastDay = filedata.index.max()  #文件记录的最近一天
		beginday = filedata.index.min()
		print('From:' + lastDay)
		print(self.ktype)
		if lastDay.find('/') > 0 and (not self.ktype == 'D'):
			lastdayTemp = datetime.datetime.strptime(lastDay, "%Y/%m/%d %H:%M")
		elif lastDay.find('-') > 0 and (not self.ktype == 'D'):
			lastdayTemp = datetime.datetime.strptime(lastDay, "%Y-%m-%d %H:%M")
		elif lastDay.find('/') > 0 and (self.ktype == 'D'):
			lastdayTemp = datetime.datetime.strptime(lastDay, "%Y/%m/%d")
		elif lastDay.find('-') > 0 and (self.ktype == 'D'):
			lastdayTemp = datetime.datetime.strptime(lastDay, "%Y-%m-%d")
		lastdayTemp = lastdayTemp + datetime.timedelta(days=-1)
		lastDay = str(lastdayTemp.year) + '-' + str(lastdayTemp.month) + '-' + str(lastdayTemp.day)
		cur = datetime.datetime.now()  # 当前时间
		cur = cur + datetime.timedelta(days=self.dalteDay)
		today = str(cur.year) + '-' + str(cur.month) + '-' + str(cur.day)
		if lastDay.replace('0', '') != today.replace('0', ''):
			try:
				StockData = ts.get_hist_data(StockCode[0:6], start=lastDay, end=today,ktype = self.ktype)  # 取得数据
			except:
				print('Error')
			else:
				if not StockData is None:
					StockData.columns.name = 'date'
					StockData = pd.concat([filedata, StockData])  # 合并数据
					StockData.columns.name = 'date'
					StockData = StockData.sort_index()  # 排序
					StockData = StockData.dropna(axis=1)  # 去除有空值的列
					StockData = StockData[StockData.index > self.OriginalDay]#只保留97年以后的数据
					StockData['date'] = StockData.index
					StockData = StockData.drop_duplicates(['date'])  # 去除重复的行
					StockData.drop(['date'],axis=1,inplace=True)
					StockData.T.to_csv(FilePath)  # 保存数据
					print(StockCode)
				else:
					print(StockCode + " Is Stop.")
		print(StockCode+' finish.')
		print('........')


if __name__=="__main__":
	StockDatapath30 = 'd:\\StockFile\\StockData_30'
	StockDatapath60 = 'd:\\StockFile\\StockData_60'
	StockDatapathD = 'd:\\StockFile\\StockData_D'
	StockDatapathW = 'd:\\StockFile\\StockData_W'
	StockDatapathM = 'd:\\StockFile\\StockData_M'
	TestFile = 'D:\\StockFile\\test'
	datatype = 'D'
	FilePath = StockDatapathD
	datatypecom = 1
	command = 'N'
	print(sys.argv)
	if len(sys.argv) == 3:
		datatype = sys.argv[1]
		command = sys.argv[2]
	else:
		print('1:更新30分钟线.')
		print('2:更新60分钟线.')
		print('3:更新日线.默认')
		datatypecom = input('请输入:')
		if datatypecom == str(1):
			datatype = '30'
		elif datatypecom == str(2):
			datatype = '60'
		elif datatypecom == str(3):
			datatype = 'D'
		command = input('是否更新今天的数据？输入Y或N:')
	if datatype == '30':
		FilePath = StockDatapath30
	if datatype == '60':
		FilePath = StockDatapath60
	if datatype == 'D':
		FilePath = StockDatapathD
	typelist = ['30','60','D']
	if datatype in typelist: 
		tool = dataUpdate(datatype)
		tool.CodeFile = 'd:\\StockFile\\StockCode.csv'
		tool.OriginalDay = '1997-01-01'
		if command == 'N':
			tool.dalteDay = -1
		tool.UpdataStockData(FilePath)
	
	
	

