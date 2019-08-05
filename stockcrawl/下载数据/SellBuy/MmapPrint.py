import sys
sys.path.append(r'D:/MyProjects/python/stockcrawl/下载数据/SellBuy')
import os
sys.path.append(os.getcwd())
from multiprocessing import Process, Queue
import mmap
import time
import _thread




maxIndex = 100
class MmapClass():
	def __init__(self, name = ''):
		self.WriIndex = None
		self.CurrentReadIndex = 0
		self.mmaplist=[]
		self.maxIndex = 200
		self.dataqueue = Queue()
		self.SpaceName = name
		self.__get_mmap_info()
	##从内存中读取信息，
	def __get_mmap_info(self):
		for i in range(0,self.maxIndex):
			##第二个参数1024是设定的内存大小，单位：字节。如果内容较多，可以调大一点
			mmap_file = mmap.mmap(-1, 1024, access = mmap.ACCESS_WRITE, tagname = self.SpaceName+'share_mmap'+str(i))
			self.mmaplist.append(mmap_file)
		self.WriIndex = mmap.mmap(-1, 4, access = mmap.ACCESS_WRITE, tagname = self.SpaceName+'share_lock')
	def read_mmap_info(self):
		while True:
			mmap_file = self.mmaplist[self.CurrentReadIndex % self.maxIndex]
			if self.__ReadAble():
				#到达位置0
				mmap_file.seek(0)
				##把二进制转换为字符串
				info_str = mmap_file.readline().translate(None, b'\x00').decode()
				self.CurrentReadIndex = self.CurrentReadIndex + 1
				mmap_file.seek(0)
				mmap_file.write((b'\x00')*1024)
				print(info_str)
				#self.dataqueue.put(info_str)
	##如果内存中没有对应信息，则向内存中写信息以供下次调用使用
	##修改内存块中的数据
	def write_mmap_info(self,data):
		if len(data) > 0 and type(data) == type(''):
			self.WriIndex.seek(0)
			CurrentWriteIndex = int.from_bytes(self.WriIndex.read(),byteorder='big', signed=False)
			mmap_file = self.mmaplist[CurrentWriteIndex % self.maxIndex]
			mmap_file.seek(0)
			mmap_file.write((b'\x00')*1024)
			mmap_file.seek(0)
			mmap_file.write(data.encode(encoding="utf-8"))
			CurrentWriteIndex = CurrentWriteIndex + 1
			self.WriIndex.seek(0)
			self.WriIndex.write(CurrentWriteIndex.to_bytes(length=4,byteorder='big',signed=False))
	def getdata(self):
		if not self.dataqueue.empty():
			return self.dataqueue.get()
		else:
			return None
	def __ReadAble(self):
		self.WriIndex.seek(0)
		if int.from_bytes(self.WriIndex.read(),byteorder='big', signed=False) > self.CurrentReadIndex:
			return True
		else:
			return False
	def loop(self):
		_thread.start_new_thread( self.read_mmap_info, () )


		
'''
mmap 对象的方法

 m.close() 　　关闭 m 对应的文件；

 m.find(str, start=0) 　　从 start 下标开始，在 m 中从左往右寻找子串 str 最早出现的下标；

 m.flush([offset, n]) 　　把 m 中从offset开始的n个字节刷到对应的文件中，参数 offset 要么同时指定，要么同时不指定；

 m.move(dstoff, srcoff, n) 　　等于 m[dstoff:dstoff+n] = m[srcoff:srcoff+n]，把从 srcoff 开始的 n 个字节复制到从 dstoff 开始的n个字节，可能会覆盖重叠的部分。

 m.read(n) 　　返回一个字符串，从 m 对应的文件中最多读取 n 个字节，将会把 m 对应文件的位置指针向后移动；

 m.read_byte() 　　返回一个1字节长的字符串，从 m 对应的文件中读1个字节，要是已经到了EOF还调用 read_byte()，则抛出异常 ValueError；

 m.readline() 　　返回一个字符串，从 m 对应文件的当前位置到下一个'\n'，当调用 readline() 时文件位于 EOF，则返回空字符串；

 m.resize(n) 　　把 m 的长度改为 n，m 的长度和 m 对应文件的长度是独立的；

 m.seek(pos, how=0) 　　同 file 对象的 seek 操作，改变 m 对应的文件的当前位置；

 m.size()　 　返回 m 对应文件的长度（不是 m 对象的长度len(m)）；

 m.tell() 　　返回 m 对应文件的当前位置；

 m.write(str) 　　把 str 写到 m 对应文件的当前位置，如果从 m 对应文件的当前位置到 m 结尾剩余的空间不足len(str)，则抛出 ValueError；

 m.write_byte(byte) 　　把1个字节（对应一个字符）写到 m 对应文件的当前位置，实际上 m.write_byte(ch) 等于 m.write(ch)。如果 m 对应文件的当前位置在 m 的结尾，也就是 m 对应文件的当前位置到 m 结尾剩余的空间不足1个字节，write() 抛出异常ValueError，而 write_byte() 什么都不做。
'''


	