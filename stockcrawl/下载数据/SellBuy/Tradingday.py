import sys
sys.path.append(r'D:/MyProjects/python/stockcrawl/下载数据/SellBuy')
import os
sys.path.append(os.getcwd())
import datetime
import time
import threading
import pandas as pd


from enum import Enum


class TimeType(Enum):
	Pre = 1
	Mon = 2
	Noo = 3
	Aft = 4
	Clo = 5
	TransactionTime = 5
	NotTransactionTime = 6




class Tradingday():
	_Tradingday_lock = threading.Lock()
	def __new__(cls, *args, **kwargs):#实现单例
		if not hasattr(Tradingday, "_instance"):
			with Tradingday._Tradingday_lock:
				if not hasattr(Tradingday, "_instance"):
					Tradingday._instance = threading.Thread.__new__(cls)  
		return Tradingday._instance
	def __init__(self):
		cur = datetime.datetime.now()
		self.MorningBeginTime = datetime.datetime.strptime(cur.strftime('%Y-%m-%d ') + '9:29:00','%Y-%m-%d %H:%M:%S')
		self.MorningEndTime = datetime.datetime.strptime(cur.strftime('%Y-%m-%d ') + '11:30:05','%Y-%m-%d %H:%M:%S')
		self.AfternoonBeginTime = datetime.datetime.strptime(cur.strftime('%Y-%m-%d ') + '12:59:55','%Y-%m-%d %H:%M:%S')
		self.AfternoonEndTime = datetime.datetime.strptime(cur.strftime('%Y-%m-%d ') + '15:00:05','%Y-%m-%d %H:%M:%S')
	def TodayIsTradingday(self):
		today = datetime.datetime.today()
		return self.IsTradingDay(today)
	def IsTradingDay(self,tageDay):
		TradindDayPath = 'd:/StockFile/tradingdays.csv'
		ReloadTraingDay = False
		if os.path.exists(TradindDayPath):
			tradingdays = pd.read_csv(TradindDayPath)
			lastDate = datetime.datetime.strptime(tradingdays.iloc[-1]['calendarDate'], '%Y-%m-%d')
			if(tageDay > lastDate):
				ReloadTraingDay = True
		else:
			ReloadTraingDay = True
		if ReloadTraingDay:
			alldays = ts.trade_cal()
			tradingdays = alldays[alldays['isOpen'] == 1]
			tradingdays.to_csv(TradindDayPath)
		tageDay = tageDay.strftime('%Y-%m-%d')
		if tageDay in tradingdays['calendarDate'].values:
			return True
		else:
			return False
	def NowIsTransactionTime(self):
		cur = datetime.datetime.now()
		timedata = self.TradTime(cur)
		if timedata == TimeType.Mon or timedata == TimeType.Aft:
			return True
		else:
			return False
	def TradTime(self,tageTime):
		if (tageTime < self.MorningBeginTime):
			return TimeType.Pre
		elif (self.MorningBeginTime <= tageTime  and tageTime <= self.MorningEndTime):
			return TimeType.Mon
		elif (self.MorningEndTime < tageTime and tageTime < self.AfternoonBeginTime):
			return TimeType.Noo
		elif (self.AfternoonBeginTime <= tageTime  and tageTime <= self.AfternoonEndTime):
			return TimeType.Aft
		elif (self.AfternoonEndTime < tageTime):
			return TimeType.Clo
	def CurTradTime(self):
		return self.TradTime(datetime.datetime.now())
	def GetFrontTradingDay(self,tagDay):
		oneday = datetime.timedelta(days=1)
		frontTradeDay = tagDay - oneday
		while not self.IsTradingDay(frontTradeDay):
			frontTradeDay = frontTradeDay - oneday
		return frontTradeDay


		
		



class debugTradingDay():
	_debugTradingDay_lock = threading.Lock()
	def __new__(cls, *args, **kwargs):#实现单例
		if not hasattr(debugTradingDay, "_instance"):
			with debugTradingDay._debugTradingDay_lock:
				if not hasattr(debugTradingDay, "_instance"):
					debugTradingDay._instance = threading.Thread.__new__(cls)  
		return debugTradingDay._instance
	def __init__(self):
		cur = datetime.datetime.now()
		self.MorningBeginTime = datetime.datetime.strptime(cur.strftime('%Y-%m-%d ') + '9:25:00','%Y-%m-%d %H:%M:%S')
		self.MorningEndTime = datetime.datetime.strptime(cur.strftime('%Y-%m-%d ') + '11:30:05','%Y-%m-%d %H:%M:%S')
		self.AfternoonBeginTime = datetime.datetime.strptime(cur.strftime('%Y-%m-%d ') + '12:59:55','%Y-%m-%d %H:%M:%S')
		self.AfternoonEndTime = datetime.datetime.strptime(cur.strftime('%Y-%m-%d ') + '15:00:05','%Y-%m-%d %H:%M:%S')
	def TodayIsTradingday(self):
		return True
	def IsTradingDay(self,tageDay):
		return True
	def NowIsTransactionTime(self):
		return True
	def TradTime(self,tageTime):
			return TimeType.Aft
			return TimeType.Mon
	def CurTradTime(self):
		return self.TradTime(datetime.datetime.now())
	def GetFrontTradingDay(self,tagDay):
		oneday = datetime.timedelta(days=1)
		frontTradeDay = tagDay - oneday
		while not self.IsTradingDay(frontTradeDay):
			frontTradeDay = frontTradeDay - oneday
		return frontTradeDay



StockTimer = Tradingday()





