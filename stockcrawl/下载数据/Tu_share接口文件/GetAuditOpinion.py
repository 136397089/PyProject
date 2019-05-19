import pandas as pd
import tushare as ts
import time
import MySQLdb
from sqlalchemy import create_engine

CodeFile='D:\\StockFile\\whole\\AllCompanyCode.csv'
AuditFile='D:\\StockFile\\whole\\AuditFile.csv'


def Fun1():
    engine = create_engine('mysql://root:@localhost/Financedata?charset=utf8')#连接数据库
    api=ts.pro_api()#获得Ts接口
    Code = pd.read_csv(CodeFile)#读取股票代码文件
    AllAudit = api.fina_audit(ts_code='000001.SZ', start_date='19910101', end_date='20190808')
    for index in Code['ts_code']:
        df = api.fina_audit(ts_code=index, start_date='19910101', end_date='20190808')
        AllAudit = pd.concat([df,AllAudit],axis=0,ignore_index=True)
        time.sleep(1)
        print(index)
    AllAudit.drop_duplicates()
    AllAudit.to_csv(AuditFile,encoding='utf_8_sig')
    AllAudit.to_sql('Auditdata', engine)
    print('Get audit data down.')




def Fun_SaveToMysql_AtOnce():
    engine = create_engine('mysql://root:@localhost/Financedata?charset=utf8')#连接数据库
    api=ts.pro_api()#获得Ts接口
    Code = pd.read_csv(CodeFile)#读取股票代码文件
    for index in Code['ts_code']:
        df = api.fina_audit(ts_code=index, start_date='19910101', end_date='20190808')
        df.to_sql('Auditdata', engine,if_exists='append')
        time.sleep(0.9)
        print(index)

if __name__=="__main__":
    Fu_AtOnce()
