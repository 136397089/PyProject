import pandas as pd
import os

#将股票日数据按照MACD正负变化分组   
def UpdataStockData(FilePath):
    files = os.listdir(FilePath)
    StockBayList = {}
    for Datafile in files:
        filedata = pd.read_csv(FilePath+'\\'+Datafile)
        filedata.index = filedata['Date']
        TageData=filedata[['BAR','Close','Diff','DEA','Ma12','Ma26']]
        Fromtindex = TageData.index[-1]
        groupindex = Fromtindex
        FromtGroup = pd.DataFrame([0],columns=['BAR'],index=['0'])
        GroupList = []
        for q in TageData.index[::-1]:
            if TageData['BAR'][q]*TageData['BAR'][Fromtindex] < 0:
                GroupList.append(TageData[groupindex:Fromtindex:-1])
                groupindex = q
            Fromtindex = q
        AllGroup = 0
        TageGroup = 0
        DownGroup = 0
        sumlist = []
        updaylist = []
        DownDaylist = []
        for q in GroupList:
            if FromtGroup['BAR'].sum()<-3.0:
                sumlist.append(q['BAR'].sum())
                AllGroup = AllGroup+1
                if q['Close'][0] > q['Close'][-1]:
                    updaylist.append(q)
                    TageGroup = TageGroup + 1
                elif q['Close'][0] < q['Close'][-1]:
                    DownDaylist.append(q)
                    DownGroup = DownGroup+1
            FromtGroup = q
        if float(TageGroup)/float(AllGroup)>0.7:
            StockBayList = StockBayList.join(pd.DataFrame([float(TageGroup)/float(AllGroup)],index=[Datafile],columns=['per']))
            #StockBayList[Datafile] = float(TageGroup)/float(AllGroup)
    with open('d:\\123.csv','w') as handle:
        handle.writelines(["%s,%d\n" % item for item in StockBayList.items()])
#            print Datafile,
#            print float(TageGroup)/float(AllGroup)
#            for bayday in updaylist:
#                print bayday
			

def GetNextMACD(M12,M26,DEA,NextValue):
    m12 = M12+(NextValue-M12)*float(2)/float(13)
    m26 = M26+(NextValue-M26)*float(2)/float(27)
    diff=m12-m26
    dea = DEA*0.8+diff*0.2
    bar = 2.0*(-dea+diff)
    return float(bar)


#以IndexStr正负变化作为标准，对股票数据分组
def CutDataBy(TageData,IndexStr):
    GroupList = []
    Fromtindex = TageData.index[-1]
    groupindex = Fromtindex
    for q in TageData.index[::-1]:
        if TageData[IndexStr][q]*TageData[IndexStr][Fromtindex] < 0:
            GroupList.append(TageData[groupindex:Fromtindex:-1])
            groupindex = q
        Fromtindex = q
    return GroupList


#画MACD柱状图
def TestStockDataByBARGroup(FilePath):
    files = os.listdir(FilePath)
    StockBayList = {}
    for Datafile in files:
        filedata = pd.read_csv(FilePath+'\\'+Datafile)
        filedata.index = filedata['Date']
        TageData=filedata[['BAR','Close','Diff','DEA','Ma12','Ma26']]
        GroupList = CutDataBy(TageData,'BAR')
        AllGroup = 0
        TageGroup = 0
        DownGroup = 0
        sumlist = []
        updaylist = []
        DownDaylist = []
        FromtGroup = pd.DataFrame([0],columns=['BAR'],index=['0'])
        for q in GroupList:
            if FromtGroup['BAR'].sum()<-0.5 and FromtGroup['Diff'][-1] > 0:
                sumlist.append(q['BAR'].sum())
                AllGroup = AllGroup+1
                if q['Close'][0] > q['Close'][-1]:
                    updaylist.append(q)
                    TageGroup = TageGroup + 1
                elif q['Close'][0] < q['Close'][-1]:
                    DownDaylist.append(q)
                    DownGroup = DownGroup+1
            FromtGroup = q
        if float(TageGroup)/float(AllGroup)>0.7:
            #StockBayList = StockBayList.join(pd.DataFrame([float(TageGroup)/float(AllGroup)],index=[Datafile],columns=['per']))
            print ('%s:%f--%d' %(Datafile,float(TageGroup)/float(AllGroup),AllGroup))
            StockBayList[Datafile] = float(TageGroup)/float(AllGroup)
    with open('d:\\123.csv','w') as handle:
        handle.writelines(["%s,%f\n" % item for item in StockBayList.items()])




data = ts.get_today_all()







