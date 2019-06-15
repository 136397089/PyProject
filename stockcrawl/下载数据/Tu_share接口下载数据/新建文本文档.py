# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 00:03:46 2018
@author: South
"""
 
import requests
import time
import sys
import json
import os 
def get_file(url, filename):    
    r = requests.get(url)    
    try:
        with open(filename, 'wb') as file:        
            file.write(r.content)
    except:
        print(filename)
        pass
 
def check_fileToSleep(filename):    
    '''检查有没有被反爬'''    
    if os.path.exists(filename):        
        with open(filename, 'r') as f:            
            line = f.readline()            
            if 'Doc' in line:                
                return False            
            else:                
                return True    
    else:        
        return False 
 
def check_item(num):    
    '''检查文件是否下载完整'''    
    zcfzb = './data/zcfzb/' + num + '.csv'    
    lrb = './data/lrb/' + num + '.csv'    
    xjllb = './data/xjllb/' + num + '.csv'    
    if check_fileToSleep(zcfzb) == False | check_fileToSleep(lrb) == False | check_fileToSleep(xjllb) == False:        
        return False    
    else:        
        return True 

def GetDataS(num):
    #存放文件的路径    
    zcfzb = 'd:/stockfile/data/zcfzb/' + num + '_zcfzb.csv'    
    lrb = 'd:/stockfile/data/lrb/' + num + '_lrb.csv'    
    xjllb = 'd:/stockfile/data/xjllb/' + num + '_xjllb.csv' 
    #文件下载网址
    zcfzb_url = "http://quotes.money.163.com/service/zcfzb_"+ num + ".html?type=year"    
    lrb_url = "http://quotes.money.163.com/service/lrb_"+ num + ".html?type=year"    
    xjllb_url = "http://quotes.money.163.com/service/xjllb_"+ num + ".html?type=year"     
    get_file(zcfzb_url, zcfzb)    
    get_file(lrb_url, lrb)    
    get_file(xjllb_url, xjllb)
    #time.sleep(1)        
    if check_item(num):        
        pass    
    else:        
        print("被反爬了，休息10s")        
        time.sleep(5)

