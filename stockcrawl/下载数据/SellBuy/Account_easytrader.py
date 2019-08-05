import sys
sys.path.append(r'D:/MyProjects/python/stockcrawl/下载数据/SellBuy')
import os
sys.path.append(os.getcwd())
import easytrader
import threading
from PriceLoop import logger





iniPosiData=[{'证券代码':'','证券名称':'','股票余额':0,'可用余额':0,'冻结数量':0,'成本价':0,'保本价':0,'市价':0,'盈亏比':0,'盈亏':0,'市值':0,'交易市场':'','股东帐户':'','在途数量':0}]


class Account_easytrader():
	_Account_easytrader_lock = threading.Lock()
	def __new__(cls, *args, **kwargs):#实现单例
		if not hasattr(Account_easytrader, "_instance"):
			with Account_easytrader._Account_easytrader_lock:
				if not hasattr(Account_easytrader, "_instance"):
					cls.InitFlag = False
					Account_easytrader._instance = threading.Thread.__new__(cls)  
		return Account_easytrader._instance
	def __init__(self):
		if not self.InitFlag:
			self.InitFlag = True
			self.userMutex = threading.Lock()
			self.userAccount = 0
			self.__UserInition()
			self.PosiData = iniPosiData
			self.TodayTrades = 0
			self.balanceData = 0
	def __UserInition(self):
		if self.userMutex.acquire(1):
			if (self.userAccount == 0):
				print('初始化并登录账号.账号类型：华泰客户端')
				try:
					self.userAccount = easytrader.use('ht_client')#华泰客户端
					self.userAccount.prepare(user='666600641060', password='457204', comm_password='241155',exe_path='D:/Program Files/htzqzyb2/xiadan.exe')
					print('账号登录完成.可进入监控程序。')
				finally:
					self.userMutex.release()
			else:
				print('账号已经初始化。可进入监控程序。')
				self.userMutex.release()
	def GetBalanceData(self):#资金情况
		if self.userMutex.acquire(3):
			self.balanceData = self.userAccount.balance
			self.userMutex.release()
	def GetPosiData(self):#持仓情况
		if self.userMutex.acquire(3):
			try:
				self.PosiData = self.userAccount.position
			except:
				self.userMutex.release()
			else:
				self.userMutex.release()
	def GetTodayTrades(self):#今日委托
		if self.userMutex.acquire(3):
			self.TodayTrades = self.userAccount.today_trades
			self.userMutex.release()
	def GetAvailable(self):
		return self.balanceData['可用金额']
	def GetTotalAssets(self):
		return self.balanceData['总资产']
	def GetCapitalBalance(self):
		return self.balanceData['资金余额']
	def GettMarketValue(self):
		return self.balanceData['股票市值']
	def GettFreezingFunds(self):
		return self.balanceData['冻结资金']
	def GetHoldingProportion(self):#持仓比例
		return self.balanceData['股票市值'] / self.balanceData['总资产']
	def GetOTWProportion(self):#买入冻结比例
		BuyingFreeze = 0
		for oneStock in self.PosiData:
			BuyingFreeze = oneStock['在途数量'] * oneStock['市价'] + BuyingFreeze
		return BuyingFreeze / self.balanceData['总资产']
	def GetFreezeProportion(self):#卖出冻结比例
		SellFreeze = 0
		for oneStock in self.PosiData:
			SellFreeze = oneStock['冻结数量'] * oneStock['市价'] + SellFreeze
		return SellFreeze / self.balanceData['总资产']



