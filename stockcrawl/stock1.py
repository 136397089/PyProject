# -*- coding:utf-8 -*-

import urllib.request
url='http://quote.stockstar.com/stock/ranklist_a_3_1_1.html'  #Ŀ����ַ
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64)"}  #αװ������������ͷ
request=urllib.request.Request(url=url,headers=headers)  #����������
response=urllib.request.urlopen(request)  #������Ӧ��
content=response.read().decode('gbk')   #��һ���ı��뷽ʽ�鿴Դ��
print(content)  #��ӡҳ��Դ�� 