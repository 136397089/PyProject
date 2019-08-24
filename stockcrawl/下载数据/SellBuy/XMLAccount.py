import sys
sys.path.append(r'D:/MyProjects/python/stockcrawl/下载数据/SellBuy')
import os
sys.path.append(os.path.dirname(__file__))
from PriceLoop import PriceLoopFactory
from xml.dom.minidom import Document
import datetime
import copy
import xml.dom.minidom as xmldom	
import threading
import xml  
from xml.dom import minidom  
import codecs  
import logging
from PriceLoop import logger
import shutil




from xml.sax.handler import ContentHandler
from xml.sax import make_parser
 
 
def parseFile(fileName):
	parser = make_parser()
	parser.setContentHandler(ContentHandler())
	parser.parse(fileName)

def mymovefile(srcfile,dstfile):
	if not os.path.isfile(srcfile):
		print(srcfile + " not exist!")
	else:
		fpath,fname=os.path.split(dstfile)	#分离文件名和路径
		if not os.path.exists(fpath):
			os.makedirs(fpath)				#创建路径
		shutil.move(srcfile,dstfile)		  #移动文件
		#print('move '+ srcfile + ' -> ' + dstfile)

def mycopyfile(srcfile,dstfile):
	if not os.path.isfile(srcfile):
		print(srcfile + "not exist!")
	else:
		fpath,fname=os.path.split(dstfile)	#分离文件名和路径
		if not os.path.exists(fpath):
			os.makedirs(fpath)				#创建路径
		try:#如果XML文件是合法的，才可以备份
			parseFile(srcfile)
			print(srcfile+' is OK!')
			shutil.copyfile(srcfile,dstfile)	  #复制文件
			return True
		except Exception as e:
			print('Error found in file:'+srcfile)
			return False
		#print('copy '+srcfile+' -> ' + dstfile)






FilePath = 'D:/MyProjects/python/stockcrawl/下载数据/SellBuy/'
XmlPath='D:/MyProjects/python/stockcrawl/下载数据/SellBuy/AccountLog/'	



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



iniBalance = {BAL_RMV:1000000, BAL_AFu:1000000,BAL_CUR:0,BAL_TAs:1000000,BAL_ARPL:0.0,BAL_CBa:1000000,BAL_CAN:'AcHHHHHHH'}
IniPosition={POS_SCo:0,POS_SNa:0,POS_SBa:0,POS_ABa:0,POS_FQu:0,POS_CPr:0,POS_GPr:0,POS_MPr:0,POS_PLR:0,POS_PLo:0,POS_MVa:0,POS_TMa:0,POS_SAc:0,POS_QOTW:0}
strNode = [POS_SCo,POS_SNa,POS_TMa,POS_SAc,BAL_CAN]
floatNode = [POS_SBa,POS_ABa,POS_FQu,POS_CPr,POS_GPr,POS_MPr,POS_PLR,POS_PLo,POS_MVa,POS_QOTW,BAL_RMV, BAL_AFu,BAL_CUR,BAL_TAs,BAL_ARPL,BAL_CBa]




# ==由于minidom默认的writexml()函数在读取一个xml文件后，修改后重新写入如果加了newl='\n',会将原有的xml中写入多余的行  
#　 ==因此使用下面这个函数来代替  
def fixed_writexml(self, writer, indent="", addindent="", newl=""):  
	writer.write(indent+"<" + self.tagName)  
	attrs = self._get_attributes()  
	a_names = attrs.keys()  
	#a_names.sort()  
	for a_name in a_names:  
		writer.write(" %s=\"" % a_name)  
		minidom._write_data(writer, attrs[a_name].value)  
		writer.write("\"")  
	if self.childNodes:  
		if len(self.childNodes) == 1 and self.childNodes[0].nodeType == minidom.Node.TEXT_NODE:  
			writer.write(">")  
			self.childNodes[0].writexml(writer, "", "", "")  
			writer.write("</%s>%s" % (self.tagName, newl))  
			return  
		writer.write(">%s"%(newl))  
		for node in self.childNodes:  
			if node.nodeType is not minidom.Node.TEXT_NODE:  
				node.writexml(writer,indent+addindent,addindent,newl)  
		writer.write("%s</%s>%s" % (indent,self.tagName,newl))  
	else:  
		writer.write("/>%s"%(newl)) 

minidom.Element.writexml = fixed_writexml


class StockOperation():
	def __init__(self):
		self.StockCode = 0
		self.StockNumber = 0
		self.CostPrice = 0
		self.OtherExpenses = 0
		self.Time = 0
	def SetbyOperation(self,Operation):
		self.StockCode = Operation.getElementsByTagName('StockCode')[0].firstChild.data
		self.StockNumber = int(float(Operation.getElementsByTagName('StockNumber')[0].firstChild.data))
		self.CostPrice = float(Operation.getElementsByTagName('CostPrice')[0].firstChild.data)
		self.OtherExpenses = float(Operation.getElementsByTagName('OtherExpenses')[0].firstChild.data)
		self.Time = Operation.getElementsByTagName('Time')[0].firstChild.data
	def Set(self,StockCode,StockNumber,CostPrice,OtherExpenses,Time):
		self.StockCode = StockCode
		self.StockNumber = StockNumber
		self.CostPrice = CostPrice
		self.OtherExpenses = OtherExpenses
		self.Time = Time
	def GetXmlDOM(self,dom,FatherName):
		FatherEle = dom.createElement(FatherName)
		StockCodeEle = dom.createElement('StockCode')
		StockCodeEle.appendChild(dom.createTextNode(self.StockCode))
		StockNumberEle = dom.createElement('StockNumber')
		StockNumberEle.appendChild(dom.createTextNode(str(self.StockNumber)))
		CostPriceEle = dom.createElement('CostPrice')
		CostPriceEle.appendChild(dom.createTextNode(str(self.CostPrice)))
		OtherExpensesEle = dom.createElement('OtherExpenses')
		OtherExpensesEle.appendChild(dom.createTextNode(str(self.OtherExpenses)))
		TimeEle = dom.createElement('Time')
		TimeEle.appendChild(dom.createTextNode(self.Time))
		FatherEle.appendChild(StockCodeEle)
		FatherEle.appendChild(StockNumberEle)
		FatherEle.appendChild(CostPriceEle)
		FatherEle.appendChild(OtherExpensesEle)
		FatherEle.appendChild(TimeEle)
		return FatherEle


class HoldingStock():
	def __init__(self):
		self.StockCode = 0
		self.StockNumber = 0
		self.CostPrice = 0
		self.OtherExpenses = 0
	def SetbyHolding(self,HoldingEle):
		self.StockCode = HoldingEle.getElementsByTagName('StockCode')[0].firstChild.data
		self.StockNumber = int(float(HoldingEle.getElementsByTagName('StockNumber')[0].firstChild.data))
		self.CostPrice = float(HoldingEle.getElementsByTagName('CostPrice')[0].firstChild.data)
		self.OtherExpenses = float(HoldingEle.getElementsByTagName('OtherExpenses')[0].firstChild.data)
	def Set(self,StockCode,StockNumber,CostPrice,OtherExpenses):
		self.StockCode = StockCode
		self.StockNumber = StockNumber
		self.CostPrice = CostPrice
		self.OtherExpenses = OtherExpenses
	def GetXmlDOM(self,dom,FatherName):
		FatherEle = dom.createElement(FatherName)
		StockCodeEle = dom.createElement('StockCode')
		StockCodeEle.appendChild(dom.createTextNode(self.StockCode))
		StockNumberEle = dom.createElement('StockNumber')
		StockNumberEle.appendChild(dom.createTextNode(str(self.StockNumber)))
		CostPriceEle = dom.createElement('CostPrice')
		CostPriceEle.appendChild(dom.createTextNode(str(self.CostPrice)))
		OtherExpensesEle = dom.createElement('OtherExpenses')
		OtherExpensesEle.appendChild(dom.createTextNode(str(self.OtherExpenses)))
		FatherEle.appendChild(StockCodeEle)
		FatherEle.appendChild(StockNumberEle)
		FatherEle.appendChild(CostPriceEle)
		FatherEle.appendChild(OtherExpensesEle)
		return FatherEle


class DayLog():
	def __init__(self):
		self.date = ''
		self.BeginAvailable = 0
		self.EndAvailable = 0
		self.BeginHolding = []
		self.EndHolding = []
		self.Buy=[]
		self.Sell=[]
		self.ResourceEle = ''
	def SetByDOM(self ,DayLogEle):#由Dom节点解释成DayLog
		self.ResourceEle = DayLogEle
		self.date = DayLogEle.getAttribute("date")
		self.BeginAvailable = float(DayLogEle.getElementsByTagName('BeginAvailable')[0].firstChild.data)
		self.EndAvailable = float(DayLogEle.getElementsByTagName('EndAvailable')[0].firstChild.data)
		self.BeginHolding = []
		self.EndHolding = []
		self.Buy=[]
		self.Sell=[]
		tempStock = DayLogEle.getElementsByTagName('BeginHolding')[0].getElementsByTagName('Stock')
		for Holding in tempStock:
			tempHoldStock = HoldingStock()
			tempHoldStock.SetbyHolding(Holding)
			self.BeginHolding.append(tempHoldStock)
		tempStock = DayLogEle.getElementsByTagName('EndHolding')[0].getElementsByTagName('Stock')
		for Holding in tempStock:
			tempHoldStock = HoldingStock()
			tempHoldStock.SetbyHolding(Holding)
			self.EndHolding.append(tempHoldStock)
		tempStock = DayLogEle.getElementsByTagName('BuyOperation')
		for Operation in tempStock:
			tempHoldStock = StockOperation()
			tempHoldStock.SetbyOperation(Operation)
			self.Buy.append(tempHoldStock)
		tempStock = DayLogEle.getElementsByTagName('SellOperation')
		for Operation in tempStock:
			tempHoldStock = StockOperation()
			tempHoldStock.SetbyOperation(Operation)
			self.Sell.append(tempHoldStock)
	def AddToXMLDom(self ,dom):#由DayLog转为Dom节点
		RootEle = dom.documentElement
		LogEle = dom.createElement('DailyLog')
		LogEle.setAttribute('date', self.date)
		DateEle = dom.createElement('date')
		DateEle.appendChild(dom.createTextNode(self.date))
		LogEle.appendChild(DateEle)
		#Begin Data
		BeginAvailableEle = dom.createElement('BeginAvailable')
		BeginAvailableEle.appendChild(dom.createTextNode(str(self.BeginAvailable)))
		BeginHoldingEle = dom.createElement('BeginHolding')
		BeginHoldingEle.setAttribute('Hold', 'Hold')
		for holding in self.BeginHolding:
			BeginHoldingEle.appendChild(holding.GetXmlDOM(dom,'Stock'))
		LogEle.appendChild(BeginAvailableEle)
		LogEle.appendChild(BeginHoldingEle)
		#Buy And Sell Operation
		for holding in self.Buy:
			LogEle.appendChild(holding.GetXmlDOM(dom,'BuyOperation'))
		for holding in self.Sell:
			LogEle.appendChild(holding.GetXmlDOM(dom,'SellOperation'))
		#End Data
		EndAvailableEle = dom.createElement('EndAvailable')
		EndAvailableEle.appendChild(dom.createTextNode(str(self.EndAvailable)))
		EndHoldingEle = dom.createElement('EndHolding')
		EndHoldingEle.setAttribute('Hold', 'Hold')
		for holding in self.EndHolding:
			EndHoldingEle.appendChild(holding.GetXmlDOM(dom,'Stock'))
		LogEle.appendChild(EndAvailableEle)
		LogEle.appendChild(EndHoldingEle)
		RootEle.appendChild(LogEle)
		self.RemoveOwnFromDom(dom)
		self.ResourceEle = LogEle
	def RemoveOwnFromDom(self,dom):#
		RootEle = dom.documentElement
		dayEleList = RootEle.getElementsByTagName('DailyLog')
		if self.ResourceEle in dayEleList:
			RootEle.removeChild(self.ResourceEle)
	def GetNextDayStartLog(self ,NextDate,dom):#
		temPOS_PLog = copy.deepcopy(self)
		temPOS_PLog.date = NextDate
		temPOS_PLog.BeginAvailable = self.EndAvailable
		temPOS_PLog.BeginHolding = copy.deepcopy(self.EndHolding)
		temPOS_PLog.EndAvailable = self.EndAvailable
		temPOS_PLog.EndHolding = copy.deepcopy(self.EndHolding)
		temPOS_PLog.Buy = []
		temPOS_PLog.Sell = []
		temPOS_PLog.AddToXMLDom(dom)
		return temPOS_PLog
	def Print(self):#
		print('date:'+self.date)
		print('BeginAvailable:'+str(self.BeginAvailable))
		print('EndAvailable:'+str(self.EndAvailable))
		for data in self.BeginHolding:
			print('BeginHolding: StockCode-',data.StockCode,'StockNumber-',data.StockNumber,'CostPrice-',data.CostPrice,'OtherExpenses-',data.OtherExpenses)
		for data in self.Buy:
			print('Buy: StockCode-',data.StockCode,'StockNumber-',data.StockNumber,'CostPrice-',data.CostPrice,'OtherExpenses-',data.OtherExpenses,'Time-',data.Time)
		for data in self.Sell:
			print('Sell: StockCode-',data.StockCode,'StockNumber-',data.StockNumber,'CostPrice-',data.CostPrice,'OtherExpenses-',data.OtherExpenses,'Time-',data.Time)
		for data in self.EndHolding:
			print('EndHolding: StockCode-',data.StockCode,'StockNumber-',data.StockNumber,'CostPrice-',data.CostPrice,'OtherExpenses-',data.OtherExpenses)
	def BuyOper(self,Code,Count,Price,Cost):#
		addHold = False
		for hold in self.EndHolding:
			if hold.StockCode == Code:
				hold.CostPrice = (hold.CostPrice*hold.StockNumber + Count*Price) / (hold.StockNumber + Count)
				hold.StockNumber = hold.StockNumber + Count
				hold.OtherExpenses = hold.OtherExpenses + Cost
				addHold = True
		if not addHold:
			hold = HoldingStock()
			hold.Set(Code,Count,Price,Cost)
			self.EndHolding.append(hold)
		Operation = StockOperation()
		Operation.Set(Code,Count,Price,Cost,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.Buy.append(Operation)
		self.EndAvailable = self.EndAvailable - Count * Price - Cost
	def SellOper(self,Code,count,price):#
		reduceHold = False
		TagHold = 0
		for hold in self.EndHolding:
			if hold.StockCode == Code and hold.StockNumber == 0:
				logger.warning('股票数量为空，不继续操作。')
				return
			if hold.StockCode == Code and hold.StockNumber > count:
				logger.warning('正常卖出股票')
				hold.CostPrice = (hold.CostPrice * hold.StockNumber - count * price) / (hold.StockNumber - count)
				hold.StockNumber = hold.StockNumber - count
				print(hold.StockCode,' ',hold.StockNumber)
				reduceHold = True
				TagHold = hold
			elif hold.StockCode == Code and hold.StockNumber == count:
				logger.warning('正常卖出股票')
				hold.CostPrice = 0
				hold.StockNumber = 0
				print(hold.StockCode,' ',hold.StockNumber)
				reduceHold = True
				TagHold = hold
			elif hold.StockCode == Code and hold.StockNumber < count:
				logger.warning('股票数量不足，以卖出所有计算。')
				hold.CostPrice = 0
				hold.StockNumber = 0
				reduceHold = True
				TagHold = hold
		if not reduceHold:
			logger.warning('拥有的股票数量不足，不可以正常操作。')
			return False
		if TagHold.StockNumber < 1:
			self.EndHolding.remove(TagHold)
		logger.info('清除股票完成。')
		Operation = StockOperation()
		Operation.Set(Code,count,price,0,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.Sell.append(Operation)
		self.EndAvailable = self.EndAvailable + count * price
	def Inition(self,Available,datestr,dom):#
		self.date = datestr
		self.BeginAvailable = Available
		self.EndAvailable = Available
		self.BeginHolding = []
		self.EndHolding = []
		self.Buy=[]
		self.Sell=[]
		self.RemoveOwnFromDom(dom)
		self.AddToXMLDom(dom)
	def AddHold(self,Code,Count,Price,Cost):#
		addHold = False
		for hold in self.EndHolding:
			if hold.StockCode == Code:
				hold.CostPrice = (hold.CostPrice * hold.StockNumber + Count*Price) / (hold.StockNumber + Count)
				hold.StockNumber = hold.StockNumber + Count
				hold.OtherExpenses = hold.OtherExpenses + Cost
				addHold = True
		if not addHold:
			hold = HoldingStock()
			hold.Set(Code,Count,Price,Cost)
			self.EndHolding.append(hold)

def ChangeTextNode(FatherEle,ChildEleName,NewText,eleInedx = 0):#将FatherEle下的ChildEleName子节点文本改为NewText
	FatherEle.getElementsByTagName(ChildEleName)[eleInedx].childNodes[0].data = NewText



class XMLAccountLog():
	def __init__(self, AccountName, PassWord):#
		self.dom = 0
		self.Account = 0
		self.PassWord = 0
		self.InitialFunds = 0
		TodayDate = datetime.datetime.now()
		self.LogCount = 0
		self.TodayLog = DayLog()
		self.EleDir={}
		self.keylist = []
		self.LogPath = XmlPath+'log/'
		if os.path.exists(self.LogPath + AccountName + 'Log.xml'):
			self.LoadTodayDomFromFile(AccountName, PassWord)
		else:
			self.LoadTodayDomFromFile('Inition','123456')
			RootEle = self.dom.documentElement
			RootEle.setAttribute('account', AccountName)
			AcEle = RootEle.getElementsByTagName('Account')[0]
			AcEle.setAttribute('number',AccountName)
			paswEle = AcEle.getElementsByTagName('PassWord')[0]
			self.Account = AccountName
			self.PassWord = PassWord
	def LoadTodayDomFromFile(self, AccountName, PassWord):#加载
		if not os.path.exists(self.LogPath + AccountName + 'Log.xml'):
			logger.warning('Can not find the file:' + self.LogPath + AccountName + 'Log.xml')
			return
		self.dom = xmldom.parse(self.LogPath + AccountName + 'Log.xml')
		RootEle = self.dom.documentElement
		self.Account = RootEle.getElementsByTagName('Account')[0].getAttribute('number')
		self.PassWord = RootEle.getElementsByTagName('Account')[0].getElementsByTagName('PassWord')[0].firstChild.data
		self.InitialFunds = RootEle.getElementsByTagName('Account')[0].getElementsByTagName('InitialFunds')[0].firstChild.data
		TodayDate = datetime.datetime.now()
		[lastdate, lastEle] = self.GetLastLog(RootEle)
		if lastdate.strftime('%Y-%m-%d') == TodayDate.strftime('%Y-%m-%d'):
			self.TodayLog.SetByDOM(lastEle)
		else:
			tempLog = DayLog()
			tempLog.SetByDOM(lastEle)
			self.TodayLog = tempLog.GetNextDayStartLog(TodayDate.strftime('%Y-%m-%d'),self.dom)
			self.TodayLog.AddToXMLDom(self.dom)
	def GetLastLog(self,RootEle):#
		lastEle= 0
		self.EleDir={}
		self.LogCount = 0
		for Ele in RootEle.getElementsByTagName('DailyLog'):
			TempDate = Ele.getAttribute("date")
			TempDate = datetime.datetime.strptime(TempDate,'%Y-%m-%d')
			self.EleDir[TempDate] = Ele
			self.LogCount = self.LogCount + 1
		self.keylist = sorted(self.EleDir)
		return [self.keylist[-1],self.EleDir[self.keylist[-1]]]
	def SaveAccountLog(self):#保存
		self.TodayLog.AddToXMLDom(self.dom)
		while len(self.dom.documentElement.getElementsByTagName('DailyLog')) > 100:#限制log的总数
			y = self.dom.documentElement.getElementsByTagName('DailyLog')[0]
			self.dom.documentElement.removeChild(y)
		with open(self.LogPath + self.Account + 'Log.xml', 'w', encoding = 'utf-8') as f:
			self.dom.writexml(f, addindent='\t', newl='\n',encoding = 'utf-8')
	def FindLogByDate(self ,Date):#
		TagDate = Date
		if type(Date) == type('aaa'):
			TagDate =  datetime.datetime.strptime(Date,'%Y-%m-%d')
		for Ele in self.dom.documentElement.getElementsByTagName('DailyLog'):
			EleDate = Ele.getAttribute("date")
			tempDate = datetime.datetime.strptime(EleDate,'%Y-%m-%d')
			if tempDate == TagDate:
				temPOS_PLog = DayLog()
				temPOS_PLog.Set(Ele)
				return temPOS_PLog
		return False



class Account():
	def __init__(self, nume, dom):
		self.Number=''
		self.passWord=''
		self.position =[]
		self.StockCodeList=[]
		self.balance = {}
		self.__AccountEle = 0
		self.LoadAccount(nume, dom)
		self.XMLLog = 0
		#self.LoadLogFile()
	def __NodeToData(self, key ,data):
		if key in strNode:
			return data
		elif key in floatNode:
			return float(data)
		else:
			logger.info('key-%s do not find',key)
	def __DictAddToDOM(self,dom,Dict,Father):#
		for key in Dict:
			childEle = dom.createElement(key)
			childEle.appendChild(dom.createTextNode(str(Dict[key])))
			Father.appendChild(childEle)
	def __B_CheckMarketPrice(self,price,stockcode):#当前价格是否可以买入
		PriceConditions = False
		Fac = PriceLoopFactory()
		loop = Fac.GetPriceLoop()
		pricedata = loop.GetPriceData(stockcode)
		if not type(pricedata) == type(0):
			if price >= float(pricedata['price']):
				return True
			else:
				logger.warning('出价太低，无法以%f元购入%s，股票当前价%s.',price, stockcode, pricedata['price'])
		return False
	def __B_CheckFinancialConditions(self,price,count,stockcode):#资金是否足够
		CapitalReq = price * count + self.__B_GetCost(price,count,stockcode)
		if CapitalReq <= self.balance[BAL_AFu]:
			return True
		logger.warning('资金不足，无法以%f元购入%d股%s',price,count,stockcode)
		return False
	def __B_GetCost(self,price,count,stockcode):#交易费用－－－买卖共同的费用
		return price * count / 1000.0 * 1.6
	def __B_AddPositionStock(self,price,count,stockcode):#买入成功后，将股票添加到持仓记录中
		tempDir = {}
		for dir in self.position:
			if dir[POS_SCo] == stockcode:
				tempDir = dir
				break
		if not len(tempDir) == 0:
			tempDir[POS_CPr] = (tempDir[POS_CPr] * tempDir[POS_SBa] + count * price) / (tempDir[POS_SBa] + count)
			tempDir[POS_GPr] = (tempDir[POS_GPr] * tempDir[POS_SBa] + count * price + self.__B_GetCost(price,count,stockcode)) / (tempDir[POS_SBa] + count)
			tempDir[POS_SBa] = tempDir[POS_SBa] + count
			tempDir[POS_QOTW] = tempDir[POS_QOTW] + count
		else:
			tempDir = copy.deepcopy(IniPosition)
			tempDir[POS_SCo] = stockcode
			tempDir[POS_CPr] = price
			tempDir[POS_GPr] = ( count * price + self.__B_GetCost(price,count,stockcode)) / count
			tempDir[POS_SBa] = count
			tempDir[POS_QOTW] = count
			self.__AddToPosition(tempDir)
		return
	def __S_CheckMarketPrice(self, price, count, stockcode):#检查当前价格是否可以成功交易
		Fac = PriceLoopFactory()
		loop = Fac.GetPriceLoop()
		pricedata = loop.GetPriceData(stockcode)
		if not type(pricedata) == type(0):
			if price <= float(pricedata['price']):
				return True
			else:
				logger.warning('出价太高，无法以%f元卖出%s，股票当前价%s.',price, stockcode, pricedata['price'])
		return False
	def __S_ReduceStock(self,price, count, stockcode):#卖出股票成功后，减少持仓
		logger.warning('__S_ReduceStock输入参数：%f %d %s',price, count, stockcode)
		tempDir = {}
		for dir in self.position:
			if dir[POS_SCo] == stockcode:
				tempDir = dir
				break
		if len(tempDir) == 0:
			logger.warning('找不到股票%s', stockcode)
			return False
		elif tempDir[POS_ABa] < count:
			logger.warning('%s股票数据不足。', stockcode)
			return False
		elif tempDir[POS_SBa] > count:
			tempDir[POS_CPr] = (tempDir[POS_CPr] * tempDir[POS_SBa] - count * price) / (tempDir[POS_SBa] - count)
			tempDir[POS_GPr] = (tempDir[POS_GPr] * tempDir[POS_SBa] - count * price ) / (tempDir[POS_SBa] - count)
			tempDir[POS_ABa] = tempDir[POS_ABa] - count
			tempDir[POS_SBa] = tempDir[POS_SBa] - count
		elif tempDir[POS_SBa] == count:
			tempDir[POS_CPr] = 0
			tempDir[POS_GPr] = 0
			tempDir[POS_ABa] = tempDir[POS_ABa] - count
			tempDir[POS_SBa] = tempDir[POS_SBa] - count	
		return True
	def __AddToPosition(self,tempDir):
		self.position.append(tempDir)
		self.StockCodeList.append(tempDir[POS_SCo])
	def AccountInitionAssets(self):#将账户的资产初始化
		self.balance = iniBalance
		self.position =[]
		self.StockCodeList=[]
	def LoadAccount(self, nume, dom):#从dom中加载账户的资金和股票数据
		self.position =[]
		self.StockCodeList=[]
		self.balance = {}
		self.__AccountEle = 0
		RootEle = dom.GetDocumentElement()
		for Ele in RootEle.getElementsByTagName('Account'):
			AccountNumber = Ele.getAttribute("number")
			if (len(AccountNumber) == 0):
				logger.warning('错误：number 属性为空')
			elif AccountNumber == nume and type(self.__AccountEle) == type(0):
				self.Number = AccountNumber
				self.__AccountEle = Ele
			elif( not (self.__AccountEle) == type(0) and AccountNumber == nume):
				self.Number = ''
				self.__AccountEle = 0
				logger.warning('记录文件中发现相同账号:%s  请检查文件是否合法。', self.Number)
				return False
		if len(self.Number) == 0:#没有找到对应的账号记录
			return False
		for key in iniBalance:
			if(len(self.__AccountEle.getElementsByTagName(key)) == 0):
				logger.warning('错误：无法找到'+key+'节点')
			else:
				self.balance[key] = self.__NodeToData(key,self.__AccountEle.getElementsByTagName(key)[0].firstChild.data)
		self.passWord = self.__AccountEle.getElementsByTagName('PassWord')[0].firstChild.data
		self.StockCodeList = []
		for hold in self.__AccountEle.getElementsByTagName('Stock'):#Stock层次解析
			tempDir={}
			for key in IniPosition:
				tempDir[key] = self.__NodeToData(key,hold.getElementsByTagName(key)[0].firstChild.data)
			self.__AddToPosition(tempDir)
	def SaveToDom(self,dom):#将账户的资金和股票数据转为dom,删除原有的dom
		domSource = Document()
		AccountEle = domSource.createElement('Account')
		AccountEle.setAttribute('number', self.Number)
		NumberEle = domSource.createElement('Number')
		NumberEle.appendChild(domSource.createTextNode(self.Number))
		PassWordEle = domSource.createElement('PassWord')
		PassWordEle.appendChild(domSource.createTextNode(self.passWord))
		AccountEle.appendChild(NumberEle)
		AccountEle.appendChild(PassWordEle)
		self.__DictAddToDOM(domSource,self.balance,AccountEle)
		for hold in self.position:
			stockEle  = domSource.createElement('Stock')
			self.__DictAddToDOM(domSource,hold,stockEle)
			AccountEle.appendChild(stockEle)
		dom.removeChild(self.__AccountEle)
		dom.appendChild(AccountEle)
		self.__AccountEle = AccountEle
		self.XMLLog.SaveAccountLog()
		return
	def AddThisNodeToDOM(self,dom):#将账户的资金和股票数据转为dom,不删除原有的dom
		for childDom in dom.GetDocumentElement().getElementsByTagName('Account'):
			if childDom.getAttribute("number") == self.Number:
				logger.warning('已经相同账号，不可以再添加。')
				return False
		domSource = Document()
		AccountEle = domSource.createElement('Account')
		AccountEle.setAttribute('number', self.Number)
		NumberEle = domSource.createElement('Number')
		NumberEle.appendChild(domSource.createTextNode(self.Number))
		PassWordEle = domSource.createElement('PassWord')
		PassWordEle.appendChild(domSource.createTextNode(self.passWord))
		AccountEle.appendChild(NumberEle)
		AccountEle.appendChild(PassWordEle)
		self.__DictAddToDOM(domSource,self.balance,AccountEle)
		for hold in self.position:
			stockEle  = domSource.createElement('Stock')
			self.__DictAddToDOM(domSource,hold,stockEle)
			AccountEle.appendChild(stockEle)
		dom.appendChild(AccountEle)
		self.__AccountEle = AccountEle
		return
	def GetB(self):#获取账户的资金数据
		balance=[]
		balance.append(copy.deepcopy(self.balance))
		return  balance
	def GetP(self):#获取账户当前拥有股票的详细数据
		position = copy.deepcopy(self.position)
		return  position
	def GetStockCodeList(self):#获取账户当前拥有的股票列表
		return self.StockCodeList
	def HasStock(self,code):#判断当前账号是否持有对应股票
		return code in self.StockCodeList
	def BuyStock(self,price,count,stockcode):#买入股票,会自动判断是否可以买入，正常买入返回true
		if not (count % 100 == 0):
			logger.warning('不是购买100的整数倍股。不可以操作。')
			return False
		elif not self.__B_CheckFinancialConditions(price,count,stockcode):
			return False
		if not self.__B_CheckMarketPrice(price,stockcode):
			return False
		else:
			cost = self.__B_GetCost(price,count,stockcode)
			self.balance[BAL_AFu] = self.balance[BAL_AFu] - price * count - cost#可用资金下调
			self.balance[BAL_CBa] = self.balance[BAL_CBa] - price * count - cost#资金余额下调
			self.__B_AddPositionStock(price,count,stockcode)
			self.XMLLog.TodayLog.BuyOper(stockcode,count,price,cost)
			logger.info('购入股票成功')
			self.CalAllData()
			return True
	def SellStock(self,price,count,stockcode):#卖出股票,会自动判断是否可以卖出，正常卖出返回true
		if not (count % 100 == 0):
			logger.warning('不是卖出100的整数倍股。不可以操作。')
			return False
		TradableCount = self.GetPositionStockTradableCount(stockcode)
		if TradableCount == 0:
			return False
		elif not self.__S_CheckMarketPrice(price, count, stockcode):
			return False
		elif TradableCount > count:
			TradableCount = count
		self.balance[BAL_AFu] = self.balance[BAL_AFu] + price * TradableCount#增加可用资金
		self.balance[BAL_CBa] = self.balance[BAL_CBa] + price * TradableCount#增加资金余额
		self.__S_ReduceStock(price, TradableCount, stockcode)
		logger.info('卖出股票%s成功',stockcode)
		self.XMLLog.TodayLog.SellOper(stockcode,count,price)
		self.CalAllData()
		self.RemoveEmptyStock()
		return True
	def ClearStock(self,code):#以当前市场价清空对应的股票
		if code in self.StockCodeList:
			tempDir = {}
			for dir in self.position:
				if dir[POS_SCo] == code:
					tempDir = dir
					break
			Fac = PriceLoopFactory()
			loop = Fac.GetPriceLoop()
			pricedata = loop.GetPriceData(code)
			CurrentPrice = float(pricedata['price'])
			ableCount = tempDir[POS_ABa]
			if ableCount == 0:
				return False
			self.balance[BAL_AFu] = self.balance[BAL_AFu] + CurrentPrice * ableCount#增加可用资金
			self.balance[BAL_CBa] = self.balance[BAL_CBa] + CurrentPrice * ableCount#增加资金余额
			self.__S_ReduceStock(CurrentPrice, ableCount, code)
			self.CalAllData()
			self.RemoveEmptyStock()
			logger.info('卖出股票%s成功',code)
			self.XMLLog.TodayLog.SellOper(code, ableCount, CurrentPrice)
			return True
		else:
			inofr = self.Number + '未拥有股票：' + code + ' 无法卖出。'
			logger.info(inofr)
			return False
	def GetPositionStockTradableCount(self, stockcode):#返回股票的可用股票数量
		tempDir = {}
		for dir in self.position:
			if dir[POS_SCo] == stockcode:
				tempDir = dir
				break
		if len(tempDir) == 0:
			#logger.info('未持有股票%s', stockcode)
			return 0
		elif tempDir[POS_ABa] <1:
			logger.info('无可用股票，当前%s股票,拥有%d股，可用共%f股。', stockcode, tempDir[POS_SBa], tempDir[POS_ABa])
			return 0
		else:
			logger.info('有可用股票，当前%s股票，拥有%d股，可用共%f股。', stockcode, tempDir[POS_SBa], tempDir[POS_ABa])
			return tempDir[POS_ABa]
	def CalAllData(self):
		Fac = PriceLoopFactory()
		loop = Fac.GetPriceLoop()
		StockMarketValue = 0
		for dir in self.position:
			pricedata = loop.GetPriceData(dir[POS_SCo])
			if not type(pricedata) == type(0):
				if not (dir[POS_SBa] == dir[POS_ABa] + dir[POS_FQu] + dir[POS_QOTW])  :
					logger.warning('股票数量不对，股票余额：%d 可用余额:%d 冻结数量%d 在途数量:%d ' ,dir[POS_SBa] ,dir[POS_ABa] ,dir[POS_FQu] ,dir[POS_QOTW])
					logger.warning('程序自动更正股票余额。')
				dir[POS_SBa] = dir[POS_ABa] + dir[POS_FQu] + dir[POS_QOTW]
				dir[POS_MPr] = float(pricedata['price'])
				dir[POS_SNa] = pricedata['name']
				dir[POS_MVa] = dir[POS_MPr] * dir[POS_SBa]
				dir[POS_PLo] = dir[POS_MVa] - dir[POS_GPr] * dir[POS_SBa]
				if dir[POS_SBa] == 0 or dir[POS_GPr] == 0:
					dir[POS_PLR] = 0
				else:
					dir[POS_PLR] = dir[POS_PLo] / (dir[POS_GPr] * dir[POS_SBa]) * 100
				StockMarketValue = StockMarketValue + dir[POS_MVa]
		self.balance[BAL_RMV] = StockMarketValue
		self.balance[BAL_TAs] = StockMarketValue + self.balance[BAL_CBa]
	def UnfreezingStocks(self):#将所有股票解冻
		for dir in self.position:
			dir[POS_ABa] = dir[POS_ABa] + dir[POS_QOTW]
			dir[POS_QOTW] = 0
			dir[POS_ABa] = dir[POS_ABa] + dir[POS_FQu]
			dir[POS_FQu] = 0
	def RemoveEmptyStock(self):#删除空的股票
		tempposition = []
		codeList=[]
		logger.info('开始清除无用股票。')
		for dir in self.position:
			if dir[POS_SBa] > 1:
				tempposition.append(dir)
				codeList.append(dir[POS_SCo])
			else:
				logger.info('%s股票余额为空，清除。',dir[POS_SCo])
		self.position = tempposition
		self.StockCodeList = codeList
	def StockOnTheWay(self):#返回在途股票代码  
		OnTheWayStock = []
		for hold in self.position:
			if hold[POS_QOTW] > 0:
				OnTheWayStock.append(hold[POS_SCo])
		return OnTheWayStock
	def LoadLogFile(self):#
		self.XMLLog = XMLAccountLog(self.Number,self.passWord)
		self.XMLLog.TodayLog.BeginAvailable = self.balance[BAL_AFu]
		self.XMLLog.TodayLog.EndAvailable = self.balance[BAL_AFu]
		self.XMLLog.TodayLog.EndHolding=[]
		for stock in self.position:
			self.XMLLog.TodayLog.AddHold(stock[POS_SCo],stock[POS_SBa],stock[POS_CPr],(stock[POS_GPr]-stock[POS_CPr])*stock[POS_SBa])
		self.XMLLog.SaveAccountLog()
		
		
		
DomMutex = threading.Lock()	
class SecurityDOM():
	_DOM_lock = threading.Lock()
	def __new__(cls, *args, **kwargs):#实现单例
		if not hasattr(SecurityDOM, "_instance"):
			with SecurityDOM._DOM_lock:
				if not hasattr(SecurityDOM, "_instance"):
					cls.__AccountFileName = 'Account.xml'
					cls.__XMLFilePath = XmlPath
					SecurityDOM._instance = threading.Thread.__new__(cls)  
		return SecurityDOM._instance
	def __init__(self):
		print(XmlPath  + self.__AccountFileName)
		if DomMutex.acquire(3):
			try:
				self.dom = xmldom.parse(XmlPath  + self.__AccountFileName)
			except:
				logger.info('解析文件出错，检查文件是否合法。')
			finally:
				DomMutex.release()
	def Reload(self,mode='Buck'):
		if DomMutex.acquire(3):
			try:
				if mode == 'Buck':#从备份文件中重新加载
					self.dom = xmldom.parse(XmlPath  + 'BackUp' + self.__AccountFileName)
				elif mode == '':
					self.dom = xmldom.parse(XmlPath + self.__AccountFileName)
			except:
				logger.info('解析文件出错，检查文件是否合法。')
			finally:
				DomMutex.release()
	def DOMSave(self):
		with open(XmlPath + self.__AccountFileName, 'w', encoding = 'utf-8') as file:
			self.dom.writexml(file, addindent='\t', newl='\n',encoding = 'utf-8')#
		if not mycopyfile(XmlPath + self.__AccountFileName,XmlPath + 'BackUp' + self.__AccountFileName):
			logger.warning('保存XMl文件出错，重新加载备份的文件。')
			self.Reload()#如果保存不成功，则重新加载备份数据
		#保存后备份一个文件，防止写文时意外退出导致数据丢失。
	def GetDocumentElement(self):
			return self.dom.documentElement
	def removeChild(self,childNode):
		if DomMutex.acquire(3):
			try:
				self.dom.documentElement.removeChild(childNode)
			except:
				logger.info('移除节点出错。')
			finally:
				DomMutex.release()
	def appendChild(self,childNode):
		if DomMutex.acquire(3):
			try:
				self.dom.documentElement.appendChild(childNode)
			except:
				logger.info('添加节点出错。')
			finally:
				DomMutex.release()

				
				
				
class LogChecker():
	def __init__(self):
		pass
	def PrintData(self):
		for index in range(1,501):
			#print('Account'+str(index))
			Log = XMLAccountLog('Account'+str(index),'123456')
			for buydata in Log.TodayLog.EndHolding :
				print(buydata)


dom = SecurityDOM()



'''
创建文档:
dom = minidom.getDOMImplementation().createDocument(None,'Root',None) 
获得根节点：root = dom.documentElement 
创建节点：element = dom.createElement('Name') 
给这个节点添加文本：element.appendChild(dom.createTextNode('default')) 
注意：这里的节点文本值是存成另外一个节点的，是createTextNode 
设置属性：element.setAttribute('age', '20') 
添加到节点：root.appendChild(element) 
# 保存文件account
with open('default.xml', 'w', encoding='utf-8') as f:
	dom.writexml(f, addindent='\t', newl='\n',encoding='utf-8')


读取文档：dom = minidom.parse('default.xml') 
获得根节点：root = dom.documentElement 
按照名称查找子节点，注意这里会递归查找所有子节点：names = root.getElementsByTagName('Name') 
所有的子节点：root.childNodes 
注意：每个节点的文本值存在TextNode节点中，也就是最后一个节点的第一个子节点 
查看是否含有属性：name.hasAttribute('age') 
查看属性：name.getAttribute('age') 
'''


if __name__ == '__main__':
	logger.info(FilePath)




def GetCost(count,price):
	stampDuty = count*price*0.001#印花税
	CertificateManagementFee = count*price*0.002/100*2#证管费
	HandlingExpenses = count*price*0.00487/100*2#经手费
	TransferFee = count*price*0.02/1000*2#过户费
	Commission  = count*price*0.0006#佣金
	cost = stampDuty + CertificateManagementFee + HandlingExpenses + TransferFee + Commission
	return cost / count / price * 100 #费率
	
	
	
	
	
	
	
	
	
	
	
	
	
	