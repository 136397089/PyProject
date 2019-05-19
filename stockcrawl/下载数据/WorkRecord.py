
import numpy as np
from scipy.fftpack import fft,ifft
import matplotlib.pyplot as plt
import seaborn
shFile='D:\\StockFile\\test\\sh1.csv'


sh1=Read_Csv_File('D:\\StockFile\\test\\sh1.csv')

shclose=sh1['close']
x=np.linspace(1,len(shclose),len(shclose))
y=list(shclose)

yy=fft(y)                     #快速傅里叶变换
yreal = yy.real               # 获取实数部分
yimag = yy.imag               # 获取虚数部分

yf=abs(fft(y))                # 取绝对值
yf1=abs(fft(y))/len(x)           #归一化处理
yf2 = yf1[range(int(len(x)/2))]  #由于对称性，只取一半区间

xf = np.arange(len(y))        # 频率
xf1 = xf
xf2 = xf[range(int(len(x)/2))]  #取一半区间

plt.subplot(221)
plt.plot(x,yreal)
plt.title('Original wave')

plt.subplot(222)
plt.plot(xf,yf,'r')
plt.title('FFT of Mixed wave(two sides frequency range)',fontsize=7,color='#7A378B')  #注意这里的颜色可以查询颜色代码表

plt.subplot(223)
plt.plot(xf1,yf1,'g')
plt.title('FFT of Mixed wave(normalization)',fontsize=9,color='r')

plt.subplot(224)
plt.plot(xf2,yf2,'b')
plt.title('FFT of Mixed wave)',fontsize=10,color='#F08080')


plt.show()



import numpy as np
from scipy.fftpack import fft,ifft
import matplotlib.pyplot as plt
import seaborn

import numpy as np
from matplotlib.pyplot import plot, show


x = np.linspace(0, 2 * np.pi, 30)#创建一个包含30个点的余弦波信号
wave = np.cos(x)
transformed = np.fft.fft(wave)#使用fft函数对余弦波信号进行傅里叶变换。
print np.all(np.abs(np.fft.ifft(transformed) - wave) < 10 ** -9)#对变换后的结果应用ifft函数，应该可以近似地还原初始信号。
plot(transformed)#使用Matplotlib绘制变换后的信号。
show()



#2019/3/8
sh1=Read_Csv_File('D:\\StockFile\\test\\sh1.csv')
sh1['close'].value_counts(bins=10,sort=False)
sh1['pChange'].value_counts(bins=10,sort=False)
var(sh1['pChange'])

import numpy as np 
arr = sh1['pChange']
print("平均值为：%f" % np.mean(arr))
print("方差为：%f" % np.var(arr))
print("标准差为:%f" % np.std(arr,ddof=1))



import numpy as np
import pandas as pd

df = pd.DataFrame({'A':np.random.randint(1, 100, 20),
 'B':np.random.randint(1, 100, 20),
 'C':np.random.randint(1, 100, 20)})

df.corr() # pearson相关系数

df.corr('kendall') # Kendall Tau相关系数


df.corr('spearman') # spearman秩相关




####################################
sh1=Read_Csv_File('D:\\StockFile\\test\\sh1.csv')
shclose=sh1['ABVP_AR']
x=np.linspace(1,len(shclose),len(shclose))
y=list(shclose)
yy=fft(y)
yreal = yy.real
plt.plot(x[1:len(y)],yreal[1:len(y)])
plt.show()
df=pd.DataFrame(yreal)

##获得股票的负债情况，并保存
ts.get_debtpaying_data(2018,4).to_csv("D:\\stockfile\\debtpaying.csv",encoding='utf_8_sig')