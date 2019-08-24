import sys
sys.path.append(r'D:/MyProjects/python/stockcrawl/下载数据/SellBuy')
import os
sys.path.append(os.getcwd())
import PriceLoop
from PriceLoop import PriceLoopFactory
import XMLAccount
import threading
import time
import tushare as ts
import datetime
import easytrader
import pandas as pd
from enum import Enum
import MmapPrint
import csv
from Tradingday import StockTimer,TimeType
import random
import logging
import queue
from PriceLoop import logger



	
BAL_RMV = '参考市值'
BAL_AFu = '可用资金'
BAL_CUR = '币种'
BAL_TAs = '总资产'
BAL_ARPL = '股份参考盈亏'
BAL_CBa = '资金余额' 
BAL_CAN = '资金帐号'
POS_SCo ='证券代码'
POS_SNa = '证券名称'
POS_SBa = '股票余额'
POS_ABa = '可用余额'
POS_FQu = '冻结数量'
POS_CPr = '成本价'
POS_GPr = '保本价'
POS_MPr ='市价'
POS_PLR = '盈亏比'
POS_PLo = '盈亏'
POS_MVa = '市值'
POS_TMa = '交易市场'
POS_SAc = '股东帐户'
POS_QOTW = '在途数量'


	
	
	



class CDPState(Enum):
	Out = 1
	UP = 2 
	Down = 3
	Mid = 4
	AUP = 5
	ADown = 6

def ReadCsv(filepath):
	birth_data = []
	with open(filepath) as csvfile:
		csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
		#birth_header = next(csv_reader)  # 读取第一行每一列的标题
		for row in csv_reader:  # 将csv 文件中的数据保存到birth_data中
			birth_data.append(row)
	datadir={}
	for row in birth_data:
		if len(row) > 2:
			datadir [row[0]] = row[1:]
	return datadir

def GetCDP(code):
	Fac=PriceLoopFactory()
	loop = Fac.GetPriceLoop()
	pricedata = loop.GetFrontDayData(code)
	if len(pricedata) == 0:
		return False
	high = float(pricedata['high'])
	low = float(pricedata['low'])
	close = float(pricedata['close'])
	cdp = (high + low + 2*close)/4
	AH = cdp + high - low
	NH = cdp*2 - low
	NL = cdp*2-high
	AL = cdp + low -high
	return [AH,NH,cdp,NL,AL]


	
	
	
	

class ThreadToChackStockPrice(threading.Thread):
	def __init__(self, threadID, StockCode):#
		threading.Thread.__init__(self)
		self.threadID = threadID
		PriceLoopFactory().GetPriceLoop().AddStockCode(StockCode)
		self.stockCDPListMutex = threading.Lock()
		self.stockCDPList = {}
		self.stockStateList = {}
		self.AddStockData(StockCode)
		self.ProcePrint = MmapPrint.MmapClass('TrackStock')
		self.UnunsfulCodeTimes = {}#记录在循环中有多少次没有成功读取到价格
		self.__FrontLoopCount = 0 #上一次的心跳
		self.__StopHeartBeat = 0#停止心跳的次数
		self.Loopflag = True
		self.UserDataFlag = False
		self.UserAccount = AccountGroup()
		self.UserAccount.FInitionAccount(500)
		self.curtime = datetime.datetime.now()
		self.MorningBeginTime = datetime.datetime.strptime(self.curtime.strftime('%Y-%m-%d') + ' 9:29:00','%Y-%m-%d %H:%M:%S')
	def Stop(self):#退出线程
		self.Loopflag = False
	def AddStockData(self,StockCode):
		CDPData = GetCDP(StockCode)
		if type(CDPData) == type(False):
			return
		tempDir = {'code':StockCode,'up':CDPData[1],'down':CDPData[3],'Aup':CDPData[0],'Adown':CDPData[4],'time':datetime.datetime.today()}
		if self.stockCDPListMutex.acquire(1):
			try:
				self.stockCDPList[StockCode] = tempDir
			finally:
				self.stockCDPListMutex.release()
	def LoadTodayCode(self,fileParh):
		if not os.path.exists(fileParh):
			return
		codeReadFromFile = ReadCsv(fileParh)
		curtime = datetime.datetime.now()
		try:
			for key in codeReadFromFile:
				temptime = datetime.datetime.strptime(key,'%Y-%m-%d')
				if temptime.strftime('%Y-%m-%d') == curtime.strftime('%Y-%m-%d'):
					for code in codeReadFromFile[key]:
						CDPData = GetCDP(code)
						if type(CDPData) == type(False):
							continue
						tempDir = {'code':code,'up':CDPData[1],'down':CDPData[3],'Aup':CDPData[0],'Adown':CDPData[4],'time':datetime.datetime.today()}
						self.stockCDPList[code] = tempDir
						#self.AddStockData(code)
					self.UserAccount.FSetTodayCodeList([codeReadFromFile[key],datetime.datetime.strptime(key,'%Y-%m-%d')])
					return
		except:
			logger.info('LoadTodayCode出错。', exc_info=True)

	def RemoveStockData(self,StockCode):
		if StockCode in self.stockCDPList:
			self.stockCDPList.pop(StockCode)
		if StockCode in self.stockStateList:
			self.stockStateList.pop(StockCode)
	def UserDataPrintFlag(self,Flag):
		self.UserDataFlag = Flag
	def __TrackAllStock(self):
		if self.stockCDPListMutex.acquire(1):
			try:
				for key in self.stockCDPList:
					if not self.CheckUnusefuleCount(key):
						continue
					datadir = self.stockCDPList[key]
					CurrentPrice = float(PriceLoopFactory().GetPriceLoop().GetPriceData(key)['price'])
					if not CurrentPrice == 0:
						self.__TrackStockPrice(datadir['code'],datadir['up'],datadir['down'],datadir['Aup'],datadir['Adown'],datadir['time'],CurrentPrice)
					else:
						self.UnunsfulCodeTimes[key] = self.UnunsfulCodeTimes[key] + 1
						logger.warning('无法获得'+ key + '的价格。')
				#logger.info('进入操作程序。')
				self.UserAccount.OperationByCDPState(self.stockStateList)
				self.PrintUserData()
			except:			
				logger.error('__TrackAllStock 出错退出。',exc_info = True)
			finally:
				self.stockCDPListMutex.release()
	def CheckUnusefuleCount(self,stockcode):
		if stockcode not in self.UnunsfulCodeTimes:
			self.UnunsfulCodeTimes[stockcode] = 0
		if self.UnunsfulCodeTimes[stockcode] < 5:
			return True
		else:
			return False
	def __TrackStockPrice(self, StockCode, CDPUp, CDPDown,  AUP, ADown,  CDPDataTime,CurrentPrice):#分析一个股票的当前价格是不是在CDP的区间之外，在CDP的上区间还是下区间
		if(not(self.curtime.strftime('%Y-%m-%d') == CDPDataTime.strftime('%Y-%m-%d'))):
			logger.warning(StockCode,' 输入数据不是今天的 CDP 参数.')
			return
		CDPUpRate = CDPUp / CurrentPrice
		CDPDownRate = CDPDown / CurrentPrice
		if(CDPUpRate > 1.2 or CDPUpRate < 0.8 or CDPDownRate > 1.2 or CDPDownRate < 0.8):
			logger.warning (StockCode+' 价格为'+str(CurrentPrice)+'的CDP上限或者下限超出范围,CDPUpRate:'+str(round(CDPUpRate,4))+'CDPDownRate:'+str(round(CDPDownRate,4)))
		elif ( not (CurrentPrice > 0.01 and CurrentPrice < 10000)):
			self.stockStateList[StockCode] = CDPState.Out
			self.ProcePrint.write_mmap_info(StockCode + ':'+' 当前价格:' + str(CurrentPrice)  +' 已经超出合理范围，检查数据是否出错。')
		elif(CDPUp < CurrentPrice and CurrentPrice < AUP):
			self.stockStateList[StockCode] = CDPState.UP
			self.ProcePrint.write_mmap_info(StockCode+' CDPUp:'+ str(round(CDPUp,4))+' 当前价格:'+ str(round(CurrentPrice,4)) )
		elif(CDPDown > CurrentPrice and CurrentPrice > ADown):
			self.stockStateList[StockCode] = CDPState.Down
			self.ProcePrint.write_mmap_info(StockCode + ' CDPDown:' + str(round(CDPDown,4)) + ' 当前价格:' + str(round(CurrentPrice,4)))
		elif CurrentPrice < ADown:
			self.stockStateList[StockCode] = CDPState.ADown
			self.ProcePrint.write_mmap_info(StockCode + ' ADown:' + str(round(ADown,4)) + ' 当前价格:' + str(round(CurrentPrice,4)))
		elif CurrentPrice > AUP:
			self.stockStateList[StockCode] = CDPState.AUP
			self.ProcePrint.write_mmap_info(StockCode + ' AUP:' + str(round(AUP,4)) + ' 当前价格:' + str(round(CurrentPrice,4)))
		else:
			self.stockStateList[StockCode] = CDPState.Mid
			self.ProcePrint.write_mmap_info(StockCode+' 没有发现可以满足CDP的交易条件。'+' CDPUp:'+str(round(CDPUp,4))+' CDPDown:'+str(round(CDPDown,4))+' 当前价格:'+str(round(CurrentPrice,4)))
	def PrintUserData(self):
		if self.UserDataFlag:
			pass
	def __CheckLoopHearBrat(self):
		newCount = PriceLoopFactory().GetPriceLoop().GetLoopCount()
		if newCount - self.__FrontLoopCount == 0:
			print('price loop 心跳停止。')
			self.__StopHeartBeat = self.__StopHeartBeat + 1
		else:
			self.__StopHeartBeat = 0
			self.__FrontLoopCount = newCount
		if self.__StopHeartBeat > 10:
			print('price loop 心跳停止超过10次。')
			self.Loopflag = False
	def ReFlushPrice(self):
		self.UserAccount.ReFlushPrice()#收盘刷新所有股票价格
		self.UserAccount.FSaveToXML()#		
	def run(self):#
		self.Loopflag = True
		print ("开始线程：")
		if not StockTimer.TodayIsTradingday():
			print('今天不是交易日，退出。')
			self.Loopflag = False
		else:
			print('今天是开盘日，进入下一步。')
		self.__FrontLoopCount = PriceLoopFactory().GetPriceLoop().GetLoopCount()
		while(self.Loopflag):
			self.curtime = datetime.datetime.now()
			if((StockTimer.TradTime(self.curtime) == TimeType.Mon) or (StockTimer.TradTime(self.curtime) == TimeType.Aft)):
				#正常交易时间内
				self.ProcePrint.write_mmap_info(self.curtime.strftime('%Y-%m-%d %H:%M:%S'))
				self.__TrackAllStock()
				time.sleep(3)
				self.__CheckLoopHearBrat()
			elif(StockTimer.TradTime(self.curtime) == TimeType.Pre):
				deltaTime = self.MorningBeginTime - self.curtime
				print('早上还未开市，等待开市。',deltaTime.seconds,'秒后重试。','开市时间',self.MorningBeginTime.strftime('%Y-%m-%d %H:%M:%S'),'当前时间',self.curtime.strftime('%Y-%m-%d %H:%M:%S'))
				#time.sleep(deltatime.seconds)
				time.sleep(10)
				continue
			elif(StockTimer.TradTime(self.curtime) == TimeType.Clo):
				self.Loopflag = False
				self.UserAccount.ReFlushPrice()#收盘刷新所有股票价格
				self.UserAccount.UnfreezingAll()#收盘后将所有股票解冻
				self.UserAccount.FSaveToXML()#
				print('今天已经收盘.解冻所有股票并退出。')
			elif(StockTimer.TradTime(self.curtime) == TimeType.Noo):
				print('午间休市期间.等待10秒重试。',self.curtime.strftime('%Y-%m-%d %H:%M:%S'))
				time.sleep(10)
		print ("退出线程：\n" )







class AccountGroup():
	AccountGroup_lock = threading.Lock()
	def __new__(cls, *args, **kwargs):#实现单例
		if not hasattr(AccountGroup, "_instance"):
			with AccountGroup.AccountGroup_lock:
				if not hasattr(AccountGroup, "_instance"):
					cls.__ValueDOM = XMLAccount.SecurityDOM()
					cls.ValueAllAcList=[]
					AccountGroup._instance = threading.Thread.__new__(cls)  
		return AccountGroup._instance
	def __init__(self):
		self.ValueTodayTrackedCodeList = []
		self.ValueAccountCount = 0
		self.FrontBuyTime = datetime.datetime.now()
		self.ValueTodayBuyCode = {}
		self.ValueTodaySellCode = []
		self.ValueAccountCanBuy = []
		self.OneDayStockCount = 250 #一天可以买入的股票数量
		self.minuteTime = 50 #每多少秒可以买一次
		self.oneStockLimit = 2 #单个股票最多买入多少次
		self.TodayBuyCount = 0 #记录今天总共买入了多少次
		self.ProcePrint = MmapPrint.MmapClass()
		self.ValueTaskList = queue.Queue()#带有Element为元操作函数，操作无成功将可进入任务队列当中
	def __FGetRandprobability(self,mean):#
		Denominator = 1000
		reandomIndex = random.randint(1,Denominator)
		if reandomIndex <= mean * Denominator:
			return True
		else:
			return False
	def __FRandGetAccountCanBuy(self):#随机获得一个可以用于交易的账号
		if len(self.ValueAccountCanBuy) == 0:
			return False
		acIndex = random.randint(0, len(self.ValueAccountCanBuy)-1)
		Ac =  self.ValueAccountCanBuy.pop(acIndex)
		balance = Ac.GetB()[0]
		stockOnTheWay = Ac.StockOnTheWay()
		if balance[BAL_AFu] / balance[BAL_TAs] > 0.2 and len(stockOnTheWay) > 0:
			logger.warning('随机找到的账号没有足够资金用于交易。')
			return False
		return Ac
	def Element_FClearAccountStock(self,code):#清空所有账号当中对应的所有股票
		for ac in self.ValueAllAcList:
			if ac.GetPositionStockTradableCount(code) > 0:#如果有可用的股票，则执行清空
				logger.info('执行清空股票%s操作',code)
				ac.ClearStock(code)
		if len(self.FindAccountHasTradableStockCode(code)) > 0:
			logger.info('股票%s还未清空完成。',code)
			self.ValueTaskList.put([self.Element_FClearAccountStock,code])
			return True
		else :
			return False
	def TodayBuyCodeAddIndex(self,stockCode):#今天买入的股票加1
		if stockCode in self.ValueTodayBuyCode:
			self.ValueTodayBuyCode[stockCode] = self.ValueTodayBuyCode[stockCode] + 1
		else:
			self.ValueTodayBuyCode[stockCode] = 1
		if self.TodayBuyCount == 0:
			for code in self.ValueTodayBuyCode:
				self.TodayBuyCount = self.TodayBuyCount + self.ValueTodayBuyCode[code]
		else:
			self.TodayBuyCount = self.TodayBuyCount + 1
	def ClearAllAccount(self):#清除账号的所有数据，
		InitAc = XMLAccount.Account('AcInition',self.__ValueDOM)
		index = 1
		for ac in self.ValueAllAcList:
			ac.Number = InitAc.Number+str(index)
			ac.passWord = InitAc.passWord
			ac.position = InitAc.position
			ac.StockCodeList = InitAc.StockCodeList
			ac.balance = InitAc.balance
			ac.SaveToDom(self.__ValueDOM)
			inedx = index + 1
		self.__ValueDOM.DOMSave()
	def FInitionAccount(self,count):#将所有的账号初始化，并保存
		self.ValueTodayBuyCode = {}
		self.ValueAllAcList=[]
		for index in range (1,count+1):
			newAc = XMLAccount.Account('Account'+str(index),self.__ValueDOM)
			if len(newAc.Number) == 0:
				newAc = XMLAccount.Account('AcInition',self.__ValueDOM)
				newAc.Number = 'Account'+str(index)
				newAc.AddThisNodeToDOM(self.__ValueDOM)
			balance = newAc.GetB()[0]
			stockOnTheWay = newAc.StockOnTheWay()
			for stockcode in stockOnTheWay:
				self.TodayBuyCodeAddIndex(stockcode)
			if balance[BAL_AFu] / balance[BAL_TAs] > 0.2 and len(stockOnTheWay) == 0:#找到有余额买入新股票的账号
				self.ValueAccountCanBuy.append(newAc)
			newAc.LoadLogFile()
			self.ValueAllAcList.append(newAc)
		self.ValueAccountCount = count
		self.__ValueDOM.DOMSave()
	def FSaveToXML(self):#将当前的数据保存
		if len(self.ValueAllAcList) == 0:
			return False
		for ac in self.ValueAllAcList:
			ac.SaveToDom(self.__ValueDOM)
		self.__ValueDOM.DOMSave()
		return True
	def FindAccountHasTradableStockCode(self,code):#检查code股票是否在其中一个账号当中
		findAccountList = []
		for ac in self.ValueAllAcList:
			if ac.GetPositionStockTradableCount(code) > 1:
				findAccountList.append(ac)
		return findAccountList
	def FSetTodayCodeList(self,value):#设置今天需要跟踪的股票代码value[0]--codelist value[1]---date
		if not datetime.datetime.now().strftime('%Y-%m-%d') == value[1].strftime('%Y-%m-%d'):
			logger.warning('不是今天的codelist，不操作')
			return False#
		value[0] = list(set(value[0]))
		self.ValueTodayTrackedCodeList = value[0]
		return self.Element_FClearCodeNotInCodeLiat()
	def Element_FClearCodeNotInCodeLiat(self):#清除今天不需要跟踪的所有股票
		if not StockTimer.NowIsTransactionTime():
			self.ValueTaskList.put(self.Element_FClearCodeNotInCodeLiat)
			logger.warning('不是交易时间，不操作')
			return False#
		for ac in self.ValueAllAcList:#清空不在股票池当中的所有股票
			surplusStockCode = set(ac.GetStockCodeList()) - set(self.ValueTodayTrackedCodeList)
			for code in surplusStockCode:
				logger.info('股票%s不在今日的列表，清空。',code)
				ac.ClearStock(code)
		if not self.FTodayCodeListCleanUp():
			logger.warning('检查发现还没有清空非今日可操作的股票。')
			self.ValueTaskList.put(self.Element_FClearCodeNotInCodeLiat)
			return False
		else:
			return True
	def FTodayCodeListCleanUp(self):#检查今天还在跟踪列表当中，需要清空的股票是否已经清空
		for ac in self.ValueAllAcList:
			surplusStockCode = set(ac.GetStockCodeList()) - set(self.ValueTodayTrackedCodeList)
			if len(surplusStockCode) > 0:
				print(surplusStockCode)
				return False
		return True
	def __FBuyStock(self, code):#value[0]－－stockcode  value[1] 
		Ac = self.__FRandGetAccountCanBuy()
		if type(Ac) == type(False):
			return False
		balance = Ac.GetB()[0]
		AvailableFunds = balance[BAL_AFu]
		Ploop=PriceLoop.PriceLoopFactory().GetPriceLoop()
		pricedata = Ploop.GetPriceData(code)['price']
		if type(pricedata) == type(0):
			logger.warning('无法获得%s的价格。',code)
			return 
		price = float(Ploop.GetPriceData(code)['price'])
		count = 0
		Position = Ac.GetP()
		ableBlance = balance[BAL_AFu]
		allBlance = balance[BAL_TAs]
		if ableBlance/allBlance < 0.8:#如果当前账号已经持有股票，将全部的可用资金买入股票
			count = int(AvailableFunds / price / 100) *100
		else:#如果当前账号没有持有股票，只使用一半的可用资金买入
			count = int(AvailableFunds / 2 / price / 100) *100
		if Ac.BuyStock(price,count,code):
			self.TodayBuyCodeAddIndex(code)
			return True
		else:
			logger.warning(code + '买入操作不成功。')
			self.ValueAccountCanBuy.append(Ac)#如果操作不成功，将可用账号放回，以便后面使用
			return False
	def OperationByCDPState(self,stockStateList):#
		self.ProcePrint.write_mmap_info('操作开始.')
		for key in stockStateList:
			if (datetime.datetime.now() - self.FrontBuyTime) < datetime.timedelta( seconds = self.minuteTime): #限制多久可以进行一次操作
				self.ProcePrint.write_mmap_info('5分钟内不再进行第二次买入.')
				break
			if stockStateList[key] == CDPState.Mid or stockStateList[key] == CDPState.Out:#不在可操作状态的股票跳过
				#logger.warning('跳过不可操作股票.')
				continue
			if stockStateList[key] == CDPState.UP:#卖出操作
				#logger.info('尝试卖出.股票：%s',key)
				if self.Element_FClearAccountStock(key):
					logger.info('成功卖出.股票：%s',key)
					self.ValueTodaySellCode.append(key)
					self.FSaveToXML()
				#else:
					#logger.warning('卖出股票：%s失败',key)
				continue
			if self.TodayBuyCount > self.OneDayStockCount:
				self.ProcePrint.write_mmap_info('今天买入的股票数已经到达上限，不再进行买入操作。')
				return 
			if key in self.ValueTodayBuyCode and self.ValueTodayBuyCode[key] > self.oneStockLimit:#今天买过的次数走过限制的股票不可以再买入
				#logger.warning('今天已经买过的股票不可以再买入.')
				continue 
			if not self.__FGetRandprobability(1/3):#随机跳过部分股票
				self.ProcePrint.write_mmap_info('随机跳过部分股票' + key)
				continue
			if stockStateList[key] == CDPState.Down:
				logger.info('买入股票:%s',key)
				self.__FBuyStock(key)
				self.FrontBuyTime = datetime.datetime.now()
				self.FSaveToXML()
		self.ProcePrint.write_mmap_info('操作结束.')
		return True
	def FDoTack(self):#完成之前没有完成的任务
		if self.ValueTaskList.qsize() > 0:
			T = self.ValueTaskList.get()
			if len(T) == 1:
				result = T[0]()
			elif len(T) == 2:
				result = T[0](T[1])
			if not result:
				TackIndexlist.put(T)
		return self.ValueTaskList.qsize() == 0
	def PrintAllBalance(self,dataindex):#打印
		logger.info('%s data',dataindex)
		for ac in self.ValueAllAcList:
			temp_balance = ac.GetB()[0]
			if dataindex in temp_balance:
				logger.info(temp_balance[dataindex])
	def Print(self):#打印
		for ac in self.ValueAllAcList:
			for data in ac.Log.TodayLog.EndHolding:
				print('EndHolding: StockCode-',data.StockCode,'StockNumber-',data.StockNumber,'CostPrice-',data.CostPrice,'OtherExpenses-',data.OtherExpenses)
	def ReFlushPrice(self):#刷新所有股票价格
		for ac in self.ValueAllAcList:
			temp_balance = ac.CalAllData()
	def UnfreezingAll(self):#将所有股票解冻
		for ac in self.ValueAllAcList:
			ac.UnfreezingStocks()





