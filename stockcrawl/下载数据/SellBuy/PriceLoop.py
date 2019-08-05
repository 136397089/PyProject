import sys
sys.path.append(r'D:/MyProjects/python/stockcrawl/下载数据/SellBuy')
import os
sys.path.append(os.getcwd())
import MmapPrint
import threading
import time
import tushare
import datetime
import pandas as pd
import copy
import urllib
import importlib
import sys
import logging
import Tradingday
from Tradingday import StockTimer,TimeType
from logging.handlers import RotatingFileHandler



LogPath = "D:/MyProjects/python/stockcrawl/下载数据/SellBuy/PriceLoopLog.txt"
RLogPath = "D:/MyProjects/python/stockcrawl/下载数据/SellBuy/RotatingLog.txt"
logger = logging.getLogger(__name__)
if not logger.hasHandlers():
	logging.basicConfig(filename=LogPath,level=logging.INFO,datefmt='%Y/%m/%d %H:%M:%S',format='%(asctime)s-%(name)s-%(levelname)s-line:%(lineno)d:\t%(message)s')
	formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-line:%(lineno)d:\t%(message)s')
	concleH = logging.StreamHandler()
	concleH.setFormatter(formatter)  
	concleH.setLevel(logging.WARNING)
	logger.addHandler(concleH)
	
	#定义一个RotatingFileHandler，最多备份3个日志文件，每个日志文件最大1K
	rHandler = RotatingFileHandler(RLogPath,maxBytes = 1*1024*1024,backupCount = 3)
	rHandler.setLevel(logging.INFO)
	rHandler.setFormatter(formatter)
	logger.addHandler(rHandler)



PriceMutex = threading.Lock()
PriceMutexCount = 0




class PriceLoop(threading.Thread):
	def __init__(self,threadID,threadName):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.logger = logger
		self.logger.info('PriceLoop 初始化.')
		self.name = threadName
		self.stockList=['sz']
		self.sleepTime = 2
		self.historyData={}
		self.ProcePrint = MmapPrint.MmapClass('PriceLoop')
		self.__loopCount=0
		self.__price = pd.DataFrame()
		self.__flag = True
		self.DebugPrice = {}
	def run(self):
		self.__loopCount = 0
		if not StockTimer.TodayIsTradingday():
			self.logger.warning('PriceLoop-今天不是交易日。')
			self.__flag = False
		else:
			self.logger.info('今天是交易日，进入循环。')
		while self.__flag:
			if StockTimer.CurTradTime() == TimeType.Mon or StockTimer.CurTradTime() == TimeType.Aft:
				if PriceMutex.acquire(1):
					try:
						self.__loopCount = self.__loopCount +1
						self.__price = tushare.get_realtime_quotes(self.stockList).set_index('code')
						information = '***' + str(self.__loopCount) +'***'
						#self.logger.info(information)
						self.ProcePrint.write_mmap_info(information)
					except urllib.error.URLError:
						#self.logger.warning('PriceLoop:获取实时股票数据失败。')
						self.ProcePrint.write_mmap_info('PriceLoop:获取实时股票数据失败。')
					finally:
						PriceMutex.release()
			else:
				self.ProcePrint.write_mmap_info('不是交易时间，不再循环下载。')
			time.sleep(self.sleepTime)
		self.logger.warning('PriceLoop-退出线程：%s ',self.name)
	def Stop(self):#设置self.flag退出线程
		self.__flag = False
	def AddStockCode(self,Scode):
		if not (len(Scode) == 6):#股票代码只能是6位
			self.logger.warning('非法的股票代码。')
			return
		if PriceMutex.acquire(1):
			try:
				self.stockList.append(Scode)
				self.stockList = list(set(self.stockList))#去重
				self.__price = tushare.get_realtime_quotes(self.stockList).set_index('code')
			finally:
				PriceMutex.release()
	def GetPriceData(self,Scode):
		returndata = 0
		if Scode in self.DebugPrice:
			return self.DebugPrice[Scode]
		if PriceMutex.acquire(1):
			try:
				if Scode not in self.__price.index:
					self.logger.warning('没有%s的数据。添加查询列表中。',Scode)
					self.stockList.append(Scode)
					self.stockList = list(set(self.stockList))#去重
					self.__price = tushare.get_realtime_quotes(self.stockList).set_index('code')
				if Scode in self.__price.index:
					returndata = self.__price.loc[Scode]	
			finally:
				PriceMutex.release()
		return returndata
	def GetAllPriceData(self):
		ReturnPriceData = 0
		if PriceMutex.acquire(3):
			try:
				ReturnPriceData = copy.deepcopy(self.__price)
			finally:
				PriceMutex.release()
		return ReturnPriceData
	def GetLoopCount(self):
		return self.__loopCount
	def SuspendGetStockPrice(self):
		global PriceMutexCount
		if PriceMutexCount == 0:
			PriceMutexCount = 1
			PriceMutex.acquire(1)
	def ReStartGetStockPrice(self):
		global PriceMutexCount
		if PriceMutexCount == 1:
			PriceMutexCount = 0
			PriceMutex.release()
		return
	def SetSleepTime(self,time):
		if time < 0.2:
			return
		self.sleepTime = time
	def GetFrontDayData(self,code):
		if code in self.historyData:
			return self.historyData[code]
		data = pd.DataFrame()
		FrontDay = datetime.datetime.today()
		timeIndex = 0
		while len(data.index) == 0:
			FrontDay = StockTimer.GetFrontTradingDay(FrontDay)
			try:
				data = tushare.get_hist_data(code,start=FrontDay.strftime('%Y-%m-%d'),end=FrontDay.strftime('%Y-%m-%d'))
			finally:
				if type(data) == type(None):
					data = pd.DataFrame()
				timeIndex = timeIndex +1
				if timeIndex > 50:
					break
		if FrontDay.strftime('%Y-%m-%d') in data.index:
			self.historyData[code] = data.loc[FrontDay.strftime('%Y-%m-%d')]
			return self.historyData[code]
		else:
			self.logger.warning('下载不到%s前一天的数据。',code)
			return pd.DataFrame()
	def SetDebugPrice(self,code,price):
		self.DebugPrice[code] = {'price':price}


class PriceLoopFactory():
	_instance_lock = threading.Lock()
	def __new__(cls, *args, **kwargs):
		if not hasattr(PriceLoopFactory, "_instance"):
			with PriceLoopFactory._instance_lock:
				if not hasattr(PriceLoopFactory, "_instance"):
					cls.priceLoop = 0
					PriceLoopFactory._instance = object.__new__(cls)  
		return PriceLoopFactory._instance
	def __init__(self):
		pass
	def GetPriceLoop(self):
		codelist=0
		if self.priceLoop == 0:
			try:
				self.priceLoop = PriceLoop(1,'Ts_GetStock')
			except Exception as e:
				logger.warning('新建线程失败。')
			else:
				self.priceLoop.start()
		elif not self.priceLoop.isAlive():
			try:
				codelist = copy.deepcopy(self.priceLoop.stockList)
				self.priceLoop = PriceLoop(1,'Ts_GetStock')
				self.priceLoop.stockList = codelist
			except Exception as e:
				logger.warning('新建线程失败。')
			else:
				self.priceLoop.start()
		return self.priceLoop


if __name__=="__main__":
	logger.info('mian run.')

'''
#单例模式,dome代码
class Singleton(object):
	_instance_lock = threading.Lock()
	def __init__(self):
		pass
	def __new__(cls, *args, **kwargs):
		if not hasattr(Singleton, "_instance"):
			with Singleton._instance_lock:
				if not hasattr(Singleton, "_instance"):
					Singleton._instance = object.__new__(cls)  
		return Singleton._instance
'''

