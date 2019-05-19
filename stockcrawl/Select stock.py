# -*- coding:utf-8 -*-


def Select_stock():
    codelist = []
    allstock = ts.get_today_all()
    if allstock.size == 0:
        print 'Can not get stock list.'
        return
    for Code in allstock['code']:
        quotes = ts.get_hist_data(Code,start='2016-1-1')
        #print 'quotes size= ',
        #print quotes.size
        if quotes.size > 100:
            getMACD(quotes)
            Judgeresult = JudgeByMACD(quotes)
            if Judgeresult != False and Judgeresult < -10:
                print 'Get Code: '+Code
                codelist.append(Code)
            elif Judgeresult != False:
                print 'Judgeresult = ',
                print Judgeresult
    return codelist

def JudgeByMACD(Date):
    # print Date['BAR'][1],
    # print '  ',
    # print Date['BAR'][2]
    if float(Date['BAR'][0]) > 0.0:
        print Date['BAR'][0]
        return False
    MACD_Sum = 0;
    for MACD in Date['BAR']:
        if MACD <= 0.0:
            MACD_Sum = MACD_Sum + MACD
        else:
            print Date['BAR'][0]
            return MACD_Sum


