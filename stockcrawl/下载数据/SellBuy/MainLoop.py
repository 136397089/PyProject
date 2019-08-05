import sys
sys.path.append(r'D:/MyProjects/python/stockcrawl/下载数据/SellBuy')
import os
sys.path.append(os.getcwd())
import datetime
import TreadToGetStock
import time
import PriceLoop


if __name__ == '__main__':
	thread1 = TreadToGetStock.ThreadToChackStockPrice(1,'000001')
	thread1.LoadTodayCode('D:/MyProjects/python/stockcrawl/下载数据/SellBuy/codefile.csv')
	thread1.start()




