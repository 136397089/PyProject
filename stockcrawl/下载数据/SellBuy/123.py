from ctypes import *  
import numpy as np 
import codecs
import datetime

SHM_SIZE = 1024*1024*20
SHM_KEY = 123559
OUTFILE="httpd_cdorked_config.bin"  
try:  
	rt = CDLL('librt.so')  
except:  
	rt = CDLL('librt.so.1')  
shmget = rt.shmget  
shmget.argtypes = [c_int, c_size_t, c_int]  
shmget.restype = c_int  
shmat = rt.shmat  
shmat.argtypes = [c_int, POINTER(c_void_p), c_int]  
shmat.restype = c_void_p  
	 
shmid = shmget(SHM_KEY, SHM_SIZE, 0o666)
if shmid < 0:  
	print ("System not infected")  
else:   
	begin_time=datetime.datetime.now()
	addr = shmat(shmid, None, 0)  
	f=open(OUTFILE, 'wb')
	rate=int.from_bytes(string_at(addr,4), byteorder='little', signed=True)   #这里数据文件是小端int16类型
	len_a=int.from_bytes(string_at(addr+4,4), byteorder='little', signed=True)   
	len_b=int.from_bytes(string_at(addr+8,4), byteorder='little', signed=True)
	print(rate,len_a,len_b)
	f.write(string_at(addr+12,SHM_SIZE))
	f.close()  
#print ("Dumped %d bytes in %s" % (SHM_SIZE, OUTFILE))
print("Success!",datetime.datetime.now()-begin_time)


messages = 'cmd\n', 'This is Console2'

processes = [Popen([sys.executable, "-c", ],  stdin=PIPE, bufsize=1, universal_newlines=True,   creationflags=CREATE_NEW_CONSOLE) for _ in range(len(messages))]






import logging

logging.basicConfig(level=logging.DEBUG, filename='D:\\MyProjects\\python\\stockcrawl\\下载数据\\SellBuy\\log.txt',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logger.info('This is a log info')
logger.debug('Debugging')
logger.warning('Warning exists')
logger.info('Finish')	
	
	
	
	
	
	
import socket

HOST = 'localhost'   # use '' to expose to all networks
PORT = 1900
{}
def incoming(host, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind((HOST, PORT))
	sock.listen(0)   # do not queue connections
	request, addr = sock.accept()
	return request.makefile('r', 0)



for line in incoming(HOST, PORT):
	print('123')
	print(line)

	
	
	
f = open('D:\\MyProjects\\python\\stockcrawl\\下载数据\\SellBuy\\log1.txt', 'w')
while True:
	data = input('Enter some text:')
	f.seek(0)
	f.write(data)
	f.truncate()
	f.flush()
	
m = mmap.mmap(os.open('xxx', os.O_RDWR), 1)
last = None

while True:
	data = m.readline()
	if data != last:
		print(data)
		last = data
	time.sleep(5)

	
	
	
	
	
	
	
	
from multiprocessing import Process,Value
import time
import random

def save_money(money):
	for i in range(100):
		time.sleep(0.1)
		money.value += random.randint(1,200)

def take_money(money):
	for i in range(100):
		time.sleep(0.1)
		money.value -= random.randint(1,150)

# money为共享内存对象,给他一个初始值2000，类型为正型“i”
# 相当于开辟了一个空间，同时绑定值2000，
money = Value('i',2000)

d = Process(target=save_money,args=())#这里面money是全局的，不写也可
d.start()
w = Process(target=take_money,args=(money,))#这里面money是全局的，不写也可
w.start()
	
	
	
	
logging.basicConfig(level=logging.INFO,datefmt='%Y/%m/%d %H:%M:%S',format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')
	
	
	
	
'''
模块测试代码
'''
import sys
sys.path.append(r'D:/MyProjects/python/stockcrawl/下载数据/SellBuy')
import os
sys.path.append(os.getcwd())
import datetime
import TreadToGetStock
	
UUU = Account_easytrader()

import importlib
importlib.reload(PriceLoop)


thread1 = TreadToGetStock.ThreadToChackStockPrice(1,'000001')
thread1.start()
thread1.LoadTodayCode()
thread1.AddStockData('000333')
thread1.AddStockData('000004')
thread1.AddStockData('000005')
thread1.UserDataPrintFlag(False)
thread1.ExitRunFun()
thread1.stockStateList
l=PriceLoopFactory().GetPriceLoop().Stop()

PriceLoopFactory().GetPriceLoop().stockList

thread1.price=14
tushare.get_hist_data('333000','2019-07-15','2019-07-15')

FilePath='D:/MyProjects/python/stockcrawl/下载数据/SellBuy/'
codefile='codefile.csv'
thread1.LoadTodayCode(FilePath + codefile)
csv_data = pd.read_csv('D:\\StockFile\\StockData_D_Current\\000001.csv')

for key in thread1.stockStateList:
	if thread1.stockStateList[key] == CDPState.Mid:
		print(key)



group = TreadToGetStock.AccountGroup()
group.FSetTodayCodeList([['000001'],datetime.datetime.strptime('2019-07-23','%Y-%m-%d')])
group.OperationByCDPState(thread1.stockStateList)
CDPData = GetCDP('000005')






















	
	
	
	
	
	
	
	
	
	
	