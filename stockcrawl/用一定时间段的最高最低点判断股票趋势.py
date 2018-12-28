##2017-06-25
##�ļ���Ҫ���ܣ���һ��ʱ��ε������͵��жϹ�Ʊ����
##
##
##
##

import pandas as pd




#
#
#
#
#
def Read_Csv_File(mFilename):
    filedata = pd.read_csv(mFilename).T
    filedata.columns = filedata.ix[0]#columns����Ϊ����
    filedata.index.name = 'date'
    filedata.columns.name = None
    filedata = filedata.ix[filedata.index[1:-1]]#ȥ������
    filedata = filedata.drop_duplicates()#ȥ���ظ�
    return filedata
#
#
#
#
#
def GetHighAndLow(data,time):
    backindex = 0
    frontindex = 1
    lowlist = []
    highlist = []
    while frontindex*time < data.index.size:
        cutdata = data[data.index[backindex*time]:data.index[frontindex*time]]
        lowlist.append(cutdata.sort(columns='low').iloc[0].name)
        highlist.append(cutdata.sort(columns='high').iloc[time].name)
        frontindex += 1
        backindex += 1
    return [cutdata.loc[lowlist],cutdata.loc[highlist]]
        













