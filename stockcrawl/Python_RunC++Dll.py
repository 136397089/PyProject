##2017-06-25
##文件主要功能：python调用C++动态库的示例代码
##
##
##
##

from ctypes import * 
import win32api
mStockData = Read_Csv_File('d:\\stockdata\\000005.csv')
dllpath='D:\\MyProjects\\win_project\\DataFrameTool\\x64\\Release\\DataFrameTool.dll'

#调用Dll计算数据返回，通过剪切板交互
#
#
#
#
def StockToolInterface(mStockData):
    try:
        dll=CDLL('D:\\MyProjects\\win_project\\DataFrameTool\\x64\\Release\\DataFrameTool.dll')
        mStockData.to_clipboard()
        b=dll.ToolInterface(1)
        result = pd.read_clipboard()
        win32api.FreeLibrary(dll._handle)
        return result
    except:
        print 'Error'
        win32api.FreeLibrary(dll._handle)
        return mStockData
		
#判断mStockData[indexname]是否增加的
#
#
#
#
def isIncrease(mStockData,indexname):
    if mStockData[indexname][mStockData.index[0]] < mStockData[indexname][mStockData.index[-1]]\
	and mStockData['BAR'][mStockData.index[0]] > 0:
        return 1
    else:
        return 0
		


#判断mStockData[indexname]是否下降的
#
#
#
#
def isReduce(mStockData,indexname):
    if mStockData[indexname][mStockData.index[0]] > mStockData[indexname][mStockData.index[-1]]\
	and mStockData['BAR'][mStockData.index[0]] < 0:
        return 1
    else:
        return 0



#
#
#
#
#
def CheckBARChange(FilePath) :
    files = os.listdir(FilePath)#打开路径文件夹下所有文件
    Increase = 0
    Reduce = 0
    AllGroup = 0
    for Datafile in files:
        filedata = Read_Csv_File(FilePath + '\\' + Datafile)#读取每个文件的数据
        filedata = StockToolInterface(filedata)
        groupedData = filedata.groupby('BARChange')
        for name,singledata in groupedData:
            Increase += isIncrease(singledata,'close')
            Reduce += isReduce(singledata,'close')
            AllGroup = AllGroup + 1
        print Datafile
    return [AllGroup,Increase,Reduce]
	
	
	