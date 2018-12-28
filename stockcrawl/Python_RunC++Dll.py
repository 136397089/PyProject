##2017-06-25
##�ļ���Ҫ���ܣ�python����C++��̬���ʾ������
##
##
##
##

from ctypes import * 
import win32api
mStockData = Read_Csv_File('d:\\stockdata\\000005.csv')
dllpath='D:\\MyProjects\\win_project\\DataFrameTool\\x64\\Release\\DataFrameTool.dll'

#����Dll�������ݷ��أ�ͨ�����а彻��
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
		
#�ж�mStockData[indexname]�Ƿ����ӵ�
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
		


#�ж�mStockData[indexname]�Ƿ��½���
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
    files = os.listdir(FilePath)#��·���ļ����������ļ�
    Increase = 0
    Reduce = 0
    AllGroup = 0
    for Datafile in files:
        filedata = Read_Csv_File(FilePath + '\\' + Datafile)#��ȡÿ���ļ�������
        filedata = StockToolInterface(filedata)
        groupedData = filedata.groupby('BARChange')
        for name,singledata in groupedData:
            Increase += isIncrease(singledata,'close')
            Reduce += isReduce(singledata,'close')
            AllGroup = AllGroup + 1
        print Datafile
    return [AllGroup,Increase,Reduce]
	
	
	