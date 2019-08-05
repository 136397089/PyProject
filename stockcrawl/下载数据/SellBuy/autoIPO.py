import easytrader
import sys
sys.path.append(r'D:/MyProjects/python/stockcrawl/下载数据/SellBuy')
import os
sys.path.append(os.getcwd())
import Account_easytrader
import datetime
import time
import Tradingday
from easytrader import helpers
import tushare as ts


def ShutDownFun():
	print('警告，将在60秒后自动关机。退出本程序可以阻止关机进程。')
	time.sleep(60)
	os.system('shutdown -s -f -t 30')
	

def AutoIPO():
	cur = datetime.datetime.now()
	AutoBeginTime = datetime.datetime.strptime(cur.strftime('%Y-%m-%d ') + '10:15:00','%Y-%m-%d %H:%M:%S')
	AutoEndTime = datetime.datetime.strptime(cur.strftime('%Y-%m-%d ') + '10:45:00','%Y-%m-%d %H:%M:%S')
	timmer = Tradingday.Tradingday()
	CheckhasIPOCode = False
	if not timmer.TodayIsTradingday():
		print('今天不是交易日。')
		os.system('pause')
		return
	if timmer.CurTradTime() == Tradingday.TimeType.Clo:
		print('今天已经收盘。')
		os.system('pause')
		return
	while True:
		cur = datetime.datetime.now()
		if timmer.CurTradTime() == Tradingday.TimeType.Pre:
			print('今天是交易日，早上还没有开盘。')
			time.sleep(10)
			continue
		if timmer.CurTradTime() == Tradingday.TimeType.Mon and cur < AutoBeginTime:#已经开盘，还没有到打新时间点
			print('已经开盘，还没有到程序设定的打新时间点')
			if not CheckhasIPOCode:
				CheckhasIPOCode = True
				print( '等待5分钟后检查今天是否有可以打新的股票。')
				time.sleep(600)
				pro = ts.pro_api()
				todaystr = datetime.datetime.now().strftime('%Y%m%d')
				df = pro.new_share(start_date = todaystr, end_date = todaystr)
				if len(ipo_data) == 0:
					print('今天没有可以打新的股票。')
					os.system('pause')
					return
				print('今天有可以打新的股票，等待打新。')
			time.sleep(10)
			continue
		if AutoBeginTime < cur and cur < AutoEndTime:
			account = Account_easytrader.Account_easytrader()
			RtInfo = account.userAccount.auto_ipo()
			print('已经一键打新')
			print(RtInfo)
			os.system('pause')
			return
		if timmer.CurTradTime() == Tradingday.TimeType.Clo or datetime.datetime.now() > AutoEndTime:
			print('今天交易时间结束，退出。')
			os.system('pause')
			return

if __name__=="__main__":
	AutoIPO()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	