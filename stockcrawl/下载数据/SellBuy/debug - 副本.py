python

import sys
sys.path.append(r'D:/MyProjects/python/stockcrawl/下载数据/SellBuy')
import os
sys.path.append(os.getcwd())
import datetime
import TreadToGetStock
import time
import PriceLoop
thread1 = TreadToGetStock.ThreadToChackStockPrice(1,'000001')
thread1.LoadTodayCode('D:/MyProjects/python/stockcrawl/下载数据/SellBuy/codefile.csv')
thread1.start()


thread1.ReFlushPrice

if __name__ == '__main__':
	thread1 = TreadToGetStock.ThreadToChackStockPrice(1,'000001')
	thread1.LoadTodayCode('D:/MyProjects/python/stockcrawl/下载数据/SellBuy/codefile.csv')
	thread1.start()

	

	
	
	
	
import sys
sys.path.append(r'D:/MyProjects/python/stockcrawl/下载数据/SellBuy')
import TreadToGetStock
gg = TreadToGetStock.AccountGroup()
gg.FInitionAccount(500)
gg.PrintAllBalance('可用资金')




	
python d:\MyProjects\python\stockcrawl\下载数据\SellBuy\Printing_Loop.py	
python d:\MyProjects\python\stockcrawl\下载数据\SellBuy\Printing_TrackStock.py	
python d:\MyProjects\python\stockcrawl\下载数据\SellBuy\Printing.py	
	
	
XmlPath=r'D:/MyProjects/python/stockcrawl/下载数据/SellBuy/AccountLog/'	

mycopyfile(XmlPath+'ac01Log.xml',XmlPath+'ac01Logtt.xml')


'''

group = TreadToGetStock.AccountGroup()
time.sleep(1)
group.FSetTodayCodeList([['000001'],datetime.datetime.strptime('2019-07-24','%Y-%m-%d')])

l=PriceLoop.PriceLoopFactory().GetPriceLoop()
l.DebugPrice['300428'] = {'price':'12.7','name':'四通新材'}

ttime = datetime.datetime.now()
datetime.datetime.now() - tttime
thread1.Stop()
thread1.UserAccount.ReFlushPrice()
thread1.UserAccount.PrintAllBalance('总资产')


thread1.stockStateList.Element_FClearAccountStock('000001')
thread1.UserAccount.FindAccountHasTradableStockCode('000001')



thread1.UserAccount.ValueAccountCount#
len(thread1.UserAccount.ValueTodayBuyCode)#今天买入多少个股票
thread1.UserAccount.ValueAccountCanBuy
thread1.UserAccount.UnfreezingAll()
thread1.UserAccount.ValueAllAcList[0].GetP()


ac = XMLAccount.Account('Account1',123456)


dom = XMLAccount.SecurityDOM()
ac = XMLAccount.Account('Account1',dom)







ts.get_k_data('000001',start='2019-07-01', end='2019-07-25',ktype = '60')
ts.get_hist_data('000001',start='2019-07-01', end='2019-07-25',ktype = '60')















'''