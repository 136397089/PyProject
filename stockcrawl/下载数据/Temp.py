

def GetAllDataAndSave(SavePath,strStoceCade):
    pro = ts.pro_api()
    today = datetime.datetime.now().strftime('%Y%m%d')               #当前时间
    try:
        StockData = pro.daily(ts_code=strStoceCade, start_date='19910101', end_date=today)
    except:
        print('Error')
    else:
        filename = SavePath + '//' + strStoceCade + '.csv'
        print(filename)
        StockData.index = Series(StockData['trade_date'].tolist())
        StockData = StockData.sort_index()#
        StockData = StockData.T.iloc[2:11].to_csv(filename)
    print('Done!')
	
GetAllDataAndSave(StockDatapath,'000001.SZ')

today = datetime.datetime.now().strftime('%Y%m%d')
StockData = pro.daily(ts_code='000001.SZ', start_date='19910101', end_date=today)
StockData.index = Series(StockData['trade_date'].tolist())



colist = StockData[1:2].values.tolist()
StockData.reindex(columns = colist)



datelist=[]
for onedate in data1.index:
    datelist.append(datetime.strptime(onedate,'%Y/%m/%d').strftime('%Y//%m//%d')) 

data1.index = Series(datelist)
date1.T.to_csv('D:\\StockFile\\test\\sh1.csv')