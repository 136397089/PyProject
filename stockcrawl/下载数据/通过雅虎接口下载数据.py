#将所有600000到601000的股票数据保存到本地的文件夹
def GetAllDataAndSave(a):
    FailList=[]
    for StockCode in a['code']:
        if (int(StockCode)>000000 and int(StockCode)<003000):
            try:
                StockCodehead = '0'*(6-len(str(StockCode)))
                strStoceCade = StockCodehead+ str(StockCode) +'.sz'#上海加ss，深圳加sz
                StockData = web.get_data_yahoo(strStoceCade,'1/1/1990','12/3/2017')
                filename = 'd://StockData//'+StockCodehead+str(StockCode)+'.csv'
                print filename
                StockData = StockData.T
                StockData.to_csv(filename)
            except:
                FailList.append(StockCode)
                print 'Can not Get Data:'+str(StockCode)
    print FailList

data = pd.read_csv(r"D:\StockCode.csv", date_parser=True, encoding='gbk')
data.index=data['date']