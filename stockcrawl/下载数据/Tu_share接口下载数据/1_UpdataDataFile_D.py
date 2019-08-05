# -*- coding:utf-8 -*-
import pandas as pd
import os
import datetime
import tushare as ts
import numpy as np






#
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
	filedata = filedata.drop_duplicates(['close', 'high', 'low', 'open', 'volume'])  # 去除重复的行
	return filedata

################################################调用get_hist_data###########################################
# 下载DataFile里面的股票数据
# 读取目标文件下'code'列中的股票代码，下载对应代码的数据
class dayUpdate():
	def __init__(self,ktype = 'D'):
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
		print(lastDay)
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
				StockData = ts.get_hist_data(StockCode[0:6], start = lastDay, end = today,ktype = self.ktype)  # 取得数据
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
					print('........')
					print(StockCode)
				else:
					print(StockCode + " Is Stop.")
	def DownloadAllDataAndSave(self,DataFiles, SavePath):#下载所有
		FileList = pd.read_csv(DataFiles)
		for StockCode in FileList['code']:
			cur = datetime.datetime.now()  # 当前时间
			today = str(cur.year) + '-' + str(cur.month) + '-' + str(cur.day)
			strStoceCade = '0' * (6 - len(str(StockCode))) + str(StockCode)
			try:
				StockData = ts.get_hist_data(strStoceCade, self.OriginalDay, today)
			except:
				print('Error')
			else:
				if not StockData is None:
					StockData.columns.name = 'date'
					filename = SavePath + '//' + strStoceCade + '.csv'
					print(filename)
					StockData = StockData.sort_index()  #
					StockData = StockData.T.to_csv(filename)
				else:
					print(filename)
		print('Done!')
	def RepairFrontStockData(self,FilePath):#补全
		files = os.listdir(FilePath)  # 打开路径文件夹下所有文件
		for dfile in files:
			filedata = Read_Csv_File(FilePath + '\\' + dfile)  # 读取每个文件的数据
			lastDay = filedata.index.max()  # 最近的那一天
			beginday = filedata.index.min()
			cur = datetime.datetime.now()  # 当前时间
			today = str(cur.year) + '-' + str(cur.month) + '-' + str(cur.day)
			if OriginalDay.replace('0', '') != beginday.replace('0', ''):
				try:
					# print('from:' + lastDay +' to:' + today)
					StockData = ts.get_hist_data(dfile[0:6], start=self.OriginalDay, end=today)  # 取得数据
				except:
					print('Error')
				else:
					StockData = pd.concat([filedata, StockData])  # 合并数据
					StockData = StockData.sort_index()  #
					StockData.dropna(axis=1)# 去除有空值的列
					StockData.T.to_csv(FilePath + '\\' + dfile)  # 保存数据
					print('........')
					print(dfile)
		print("Done!")


	
		
		
		
#########################################################################################################


if __name__=="__main__":
	StockDatapath30 = 'd:\\StockFile\\StockData_30'
	StockDatapath60 = 'd:\\StockFile\\StockData_60'
	StockDatapathD = 'd:\\StockFile\\StockData_D'
	StockDatapathW = 'd:\\StockFile\\StockData_W'
	StockDatapathM = 'd:\\StockFile\\StockData_M'
	TestFile = 'D:\\StockFile\\test'	
	command=input('是否将目录 ' + StockDatapathD + ' 下的股票数据全部更新到今天。(y：是 n:否)  本程序自动补全之前没有下载的数据。')
	if command == 'y' or command == 'Y':
		tool = dayUpdate()
		tool.UpdataStockData(StockDatapathD)
		#cur = datetime.datetime.now()
		#OriginalDay = '1997-01-01'
		#today = str(cur.year) + '-' + str(cur.month) + '-' + str(cur.day)
		#data = ts.get_k_data('sh',start=OriginalDay, end=today).set_index(['date']).sort_index()
		#data.columns.name = 'date'
		#data = data.T.to_csv('d://StockFile//whole//sh'+'.csv')
		## 下载保存上证指数数据
		#StockData = ts.get_hist_data('sh')
		#StockData.sort_index().T.to_csv('d://StockFile//sh.csv')
		





