import pandas as pd
#打开文件读取数据，并转置
DataList=pd.read_csv('d:\\stockdata\\000005.csv').T
#columns用第一行
DataList.columns = DataList.ix['Unnamed: 0']
#去除首行数据
DataList = DataList.ix[DataList.index[1:-1]]

DataList.index.name='data