import pandas as pd
#���ļ���ȡ���ݣ���ת��
DataList=pd.read_csv('d:\\stockdata\\000005.csv').T
#columns�õ�һ��
DataList.columns = DataList.ix['Unnamed: 0']
#ȥ����������
DataList = DataList.ix[DataList.index[1:-1]]

DataList.index.name='data