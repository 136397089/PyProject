import pandas as pd
import os

class StateMachine(object):
    def __init__(self,DEAFrontDay,MACD_Ch,DEAFrontDay,DEA_Ch):
        self.MACDFrontDay = MACDFrontDay#MACD考查的时间段
        self.MACD_Ch = MACD_Ch
        self.DEAFrontDay = DEAFrontDay#DEA考查的时间段
        self.DEA_Ch = DEA_Ch
    def cacl_all(self, days=1):
        return (self.room * self.cf + self.br) * days
		
		
def TestAllStockData(FilePath):
    files = os.listdir(FilePath)
    for Datafile in files:
        filedata = pd.read_csv(FilePath+'\\'+Datafile)
        filedata.index = filedata['Date']
        TestStockData(filedata)

def TestStockData(filedata):
    if type(filedata) != type(pd.DataFrame()):
        return
    for q in TageData:
        