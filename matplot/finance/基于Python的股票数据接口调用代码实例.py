#!/usr/bin/python
# -*- coding: utf-8 -*-
import json, urllib
from urllib import urlencode
  
#----------------------------------
# ��Ʊ���ݵ���ʾ������ �� �ۺ�����
# ���߽ӿ��ĵ���http://www.juhe.cn/docs/21
#----------------------------------
  
def main():
  
    #�����������APPKey
    appkey = "*********************"
  
    #1.�������
    request1(appkey,"GET")
  
    #2.��۹���
    request2(appkey,"GET")
  
    #3.��������
    request3(appkey,"GET")
  
    #4.��۹����б�
    request4(appkey,"GET")
  
    #5.���������б�
    request5(appkey,"GET")
  
    #6.���ڹ����б�
    request6(appkey,"GET")
  
    #7.�����б�
    request7(appkey,"GET")
  
  
  
#�������
def request1(appkey, m="GET"):
    url = "http://web.juhe.cn:8080/finance/stock/hs"
    params = {
        "gid" : "", #��Ʊ��ţ��Ϻ�������sh��ͷ�����ڹ�����sz��ͷ�磺sh601009
        "key" : appkey, #APP Key
  
    }
    params = urlencode(params)
    if m =="GET":
        f = urllib.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.urlopen(url, params)
  
    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            #�ɹ�����
            print res["result"]
        else:
            print "%s:%s" % (res["error_code"],res["reason"])
    else:
        print "request api error"
  
#��۹���
def request2(appkey, m="GET"):
    url = "http://web.juhe.cn:8080/finance/stock/hk"
    params = {
        "num" : "", #��Ʊ���룬�磺00001 Ϊ������ʵҵ����Ʊ����
        "key" : appkey, #APP Key
  
    }
    params = urlencode(params)
    if m =="GET":
        f = urllib.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.urlopen(url, params)
  
    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            #�ɹ�����
            print res["result"]
        else:
            print "%s:%s" % (res["error_code"],res["reason"])
    else:
        print "request api error"
  
#��������
def request3(appkey, m="GET"):
    url = "http://web.juhe.cn:8080/finance/stock/usa"
    params = {
        "gid" : "", #��Ʊ���룬�磺aapl Ϊ��ƻ����˾���Ĺ�Ʊ����
        "key" : appkey, #APP Key
  
    }
    params = urlencode(params)
    if m =="GET":
        f = urllib.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.urlopen(url, params)
  
    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            #�ɹ�����
            print res["result"]
        else:
            print "%s:%s" % (res["error_code"],res["reason"])
    else:
        print "request api error"
  
#��۹����б�
def request4(appkey, m="GET"):
    url = "http://web.juhe.cn:8080/finance/stock/hkall"
    params = {
        "key" : appkey, #�������APPKEY
        "page" : "", #�ڼ�ҳ,ÿҳ20������,Ĭ�ϵ�1ҳ
  
    }
    params = urlencode(params)
    if m =="GET":
        f = urllib.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.urlopen(url, params)
  
    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            #�ɹ�����
            print res["result"]
        else:
            print "%s:%s" % (res["error_code"],res["reason"])
    else:
        print "request api error"
  
#���������б�
def request5(appkey, m="GET"):
    url = "http://web.juhe.cn:8080/finance/stock/usaall"
    params = {
        "key" : appkey, #�������APPKEY
        "page" : "", #�ڼ�ҳ,ÿҳ20������,Ĭ�ϵ�1ҳ
  
    }
    params = urlencode(params)
    if m =="GET":
        f = urllib.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.urlopen(url, params)
  
    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            #�ɹ�����
            print res["result"]
        else:
            print "%s:%s" % (res["error_code"],res["reason"])
    else:
        print "request api error"
  
#���ڹ����б�
def request6(appkey, m="GET"):
    url = "http://web.juhe.cn:8080/finance/stock/szall"
    params = {
        "key" : appkey, #�������APPKEY
        "page" : "", #�ڼ�ҳ(ÿҳ20������),Ĭ�ϵ�1ҳ
  
    }
    params = urlencode(params)
    if m =="GET":
        f = urllib.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.urlopen(url, params)
  
    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            #�ɹ�����
            print res["result"]
        else:
            print "%s:%s" % (res["error_code"],res["reason"])
    else:
        print "request api error"
  
#�����б�
def request7(appkey, m="GET"):
    url = "http://web.juhe.cn:8080/finance/stock/shall"
    params = {
        "key" : appkey, #�������APPKEY
        "page" : "", #�ڼ�ҳ,ÿҳ20������,Ĭ�ϵ�1ҳ
  
    }
    params = urlencode(params)
    if m =="GET":
        f = urllib.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.urlopen(url, params)
  
    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            #�ɹ�����
            print res["result"]
        else:
            print "%s:%s" % (res["error_code"],res["reason"])
    else:
        print "request api error"
  
  
  
if __name__ == '__main__':
    main()