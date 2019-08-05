from multiprocessing import Process, Queue
import mmap
import time
import _thread






XMLAclogger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,datefmt='%Y/%m/%d %H:%M:%S',format='%(asctime)s-%(name)s-%(levelname)s-line:%(lineno)d:\t%(message)s')
concleH = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-line:%(lineno)d:\t%(message)s')
concleH.setFormatter(formatter)  
concleH.setLevel(logging.WARNING)
if not XMLAclogger.hasHandlers():
	XMLAclogger.addHandler(concleH)
logging.QueueHandler()
logging.QueueListener()
	
	
	
	
	
	

import csv
import os
import numpy as np
import random
import requests
# name of data file
FilePath='D:/MyProjects/python/stockcrawl/下载数据/SellBuy/'
codefile='codefile.csv'
# 数据集名称
birth_weight_file = FilePath+codefile

# download data and create data file if file does not exist in current directory
# 如果当前文件夹下没有birth_weight.csv数据集则下载dat文件并生成csv文件
if not os.path.exists(birth_weight_file):
    birthdata_url = 'https://github.com/nfmcclure/tensorflow_cookbook/raw/master/01_Introduction/07_Working_with_Data_Sources/birthweight_data/birthweight.dat'
    birth_file = requests.get(birthdata_url)
    birth_data = birth_file.text.split('\r\n')
    # split分割函数,以一行作为分割函数，windows中换行符号为'\r\n',每一行后面都有一个'\r\n'符号。
    birth_header = birth_data[0].split('\t')
    # 每一列的标题，标在第一行，即是birth_data的第一个数据。并使用制表符作为划分。
    birth_data = [[float(x) for x in y.split('\t') if len(x) >= 1] for y in birth_data[1:] if len(y) >= 1]
    print(np.array(birth_data).shape)
    # (189, 9)
    # 此为list数据形式不是numpy数组不能使用np,shape函数,但是我们可以使用np.array函数将list对象转化为numpy数组后使用shape属性进行查看。
    with open(birth_weight_file, "w", newline='') as f:
    # with open(birth_weight_file, "w") as f:
        writer = csv.writer(f)
        writer.writerows([birth_header])
        writer.writerows(birth_data)
        f.close()

def ReadCsv():
	birth_data = []
	with open(birth_weight_file) as csvfile:
		csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
		#birth_header = next(csv_reader)  # 读取第一行每一列的标题
		for row in csv_reader:  # 将csv 文件中的数据保存到birth_data中
			birth_data.append(row)
	datadir={}
	for row in birth_data:
		datadir [row[0]] = row[1:]
	return datadir
 

birth_data = [[float(x) for x in row[1:]] for row in birth_data]  # 将数据从string形式转换为float形式


birth_data = np.array(birth_data)  # 将list数组转化成array数组便于查看数据结构
birth_header = np.array(birth_header)
print(birth_data.shape)  # 利用.shape查看结构。
print(birth_header.shape)

	
	