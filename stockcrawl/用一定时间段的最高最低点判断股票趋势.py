##2017-06-25
##文件主要功能：用一定时间段的最高最低点判断股票趋势
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
    filedata.columns = filedata.ix[0]#columns更新为首行
    filedata.index.name = 'date'
    filedata.columns.name = None
    filedata = filedata.ix[filedata.index[1:-1]]#去除首行
    filedata = filedata.drop_duplicates()#去除重复
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
        













