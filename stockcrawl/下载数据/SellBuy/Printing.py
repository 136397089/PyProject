import sys
sys.path.append(r'D:/MyProjects/python/stockcrawl/下载数据/SellBuy')
import os
sys.path.append(os.getcwd())
import MmapPrint


if __name__=="__main__":
	r = MmapPrint.MmapClass()
	r.read_mmap_info()
