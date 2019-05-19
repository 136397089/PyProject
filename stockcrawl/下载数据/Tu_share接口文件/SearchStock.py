import pandas as pd
import tushare as ts
import numpy as np
import datetime
import MySQLdb
from sqlalchemy import create_engine


Path='D:\\StockFile\\reporting\\'

get_stock_basics_map={'code':'代码','name':'名称','industry':'所属行业','area':'地区','pe':'市盈率','outstanding':'流通股本(亿)','totals':'总股本(亿)','totalAssets':'总资产(万)','liquidAssets':'流动资产','fixedAssets':'固定资产','reserved':'公积金','reservedPerShare':'每股公积金','esp':'每股收益','bvps':'每股净资','pb':'市净率','timeToMarket':'上市日期','undp':'未分利润','perundp':' 每股未分配','rev':'收入同比(%)','profit':'利润同比(%)','gpr':'毛利率(%)','npr':'净利润率(%)','holders':'股东人数'}
get_report_data_map={'code':'代码','name':'名称','esp':'每股收益','eps_yoy':'每股收益同比(%)','bvps':'每股净资产','roe':'净资产收益率(%)','epcf':'每股现金流量(元)','net_profits':'净利润(万元)','profits_yoy':'净利润同比(%)','distrib':'分配方案','report_date':'发布日期'}
get_profit_data_map={'code':'代码','name':'名称','roe':'净资产收益率(%)','net_profit_ratio':'净利率(%)','gross_profit_rate':'毛利率(%)','net_profits':'净利润(万元)','esp':'每股收益','business_income':'营业收入(百万元)','bips':'每股主营业务收入(元)'}
get_operation_datamap_map={'code':'代码','name':'名称','arturnover':'应收账款周转率(次)','arturndays':'应收账款周转天数(天)','inventory_turnover':'存货周转率(次)','inventory_days':'存货周转天数(天)','currentasset_turnover':'流动资产周转率(次)','currentasset_days':'流动资产周转天数(天)'}
get_growth_data_map={'code':'代码','name':'名称','mbrg':'主营业务收入增长率(%)','nprg':'净利润增长率(%)','nav': '净资产增长率','targ': '总资产增长率','epsg': '每股收益增长率','seg': '股东权益增长率','nprg':'净利润增长率(%)','nav':'净资产增长率','targ':'总资产增长率','epsg':'每股收益增长率','seg':'股东权益增长率'}
get_debtpaying_data_map={'code':'代码','name':'名称','currentratio':'流动比率','quickratio':'速动比率','cashratio':'现金比率','icratio':'利息支付倍数','sheqratio':'股东权益比率','adratio':'股东权益增长率'}
get_cashflow_datamap_map={'code':'代码','name':'名称','cf_sales':'经营现金净流量对销售收入比率','rateofreturn':'资产的经营现金流量回报率','cf_nm':'经营现金净流量与净利润的比率','cf_liabilities':'经营现金净流量对负债比率','cashflowratio':'现金流量比率'}



def GetAllReport(year,quarter):
    engine = create_engine('mysql://root:@localhost/Financedata?charset=utf8')#连接数据库
    today = str(year) + '_' + str(quarter)
    report = ts.get_report_data(year,quarter)
    profit = ts.get_profit_data(year,quarter)
    operation = ts.get_operation_data(year,quarter)
    growth = ts.get_growth_data(year,quarter)
    debtpaying = ts.get_debtpaying_data(year,quarter)
    cashflow = ts.get_cashflow_data(year,quarter)

    report.to_sql('report_'+today, engine)
    profit.to_sql('profit_' + today, engine)
    operation.to_sql('operation_' + today, engine)
    growth.to_sql('growth_' + today, engine)
    debtpaying.to_sql('debtpaying_' + today, engine)
    cashflow.to_sql('cashflow_' + today, engine)

###
    report.rename(columns=get_report_data_map, inplace=True)
    profit.rename(columns=get_profit_data_map, inplace=True)
    operation.rename(columns=get_operation_datamap_map, inplace=True)
    growth.rename(columns=get_growth_data_map, inplace=True)
    debtpaying.rename(columns=get_debtpaying_data_map, inplace=True)
    cashflow.rename(columns=get_cashflow_datamap_map, inplace=True)
####
    report.to_csv(Path+'report'+today+'.csv',encoding='utf_8_sig')
    profit.to_csv(Path+'profit'+today+'.csv',encoding='utf_8_sig')
    operation.to_csv(Path+'operation'+today+'.csv',encoding='utf_8_sig')
    growth.to_csv(Path+'growth'+today+'.csv',encoding='utf_8_sig')
    debtpaying.to_csv(Path+'debtpaying'+today+'.csv',encoding='utf_8_sig')
    cashflow.to_csv(Path+'cashflow'+today+'.csv',encoding='utf_8_sig')
    report.to_sql('report_'+today, engine)

    print('完成'+today+'数据下载')


if __name__=='__main__':
    for num in range(2010,2018):
        GetAllReport(num,4)



def GetBasicsAndSave():
    cur = datetime.datetime.now()
    today = str(cur.year) + '_' + str(cur.month) + '_' + str(cur.day)
    engine = create_engine('mysql://root:@localhost/Financedata?charset=utf8')  # 连接数据库
    basics = ts.get_stock_basics()
    tempbasics = basics
    tempbasics.insert(0, 'code', tempbasics.index)
    tempbasics.set_index(['index'])
    tempbasics.index = pd.core.indexes.range.RangeIndex(start=0, stop=len(tempbasics), step=1)
    tempbasics.to_sql('basics'+today, engine)
