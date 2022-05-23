
from scipy import signal, special
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker 
from matplotlib.font_manager import FontProperties
font = FontProperties(fname="/root/anaconda3/lib/python3.6/site-packages/matplotlib/mpl-data/fonts/ttf/simhei.ttf")
plt.rcParams['font.sans-serif']=['simhei']#设置作图中文显示

def wgn(x, snr):
    Ps = np.sum(abs(x)**2)/len(x)
    Pn = Ps/(10**((snr/10)))
    noise = np.random.randn(len(x)) * np.sqrt(Pn)
    signal_add_noise = x + noise
    return signal_add_noise





T = 1               #基带信号宽度，也就是频率
nb = 50              #定义传输的比特数
delta_T = T/199      #采样间隔
fs = 1/delta_T       #采样频率
fc = 100/T           #载波频率
SNR = 10             #信噪比

t = np.arange(0, nb*T, delta_T)
N = len(t)

# 产生基带信号
data = [1 if x > 0.5 else 0 for x in np.random.randn(1, nb)[0]]  #调用随机函数产生任意在0到1的1*nb的矩阵，大于0.5显示为1，小于0.5显示为0
data0 = []                             #创建一个1*nb/delta_T的零矩阵
for q in range(nb):
    data0 += [data[q]]*int(1/delta_T)  #将基带信号变换成对应波形信号

# 调制信号的产生
data1 = []      #创建一个1*nb/delta_T的零矩阵
datanrz = np.array(data)*2-1              #将基带信号转换成极性码,映射
for q in range(nb):
    data1 += [datanrz[q]]*int(1/delta_T)  #将极性码变成对应的波形信号

idata = datanrz[0:(nb-1):2]       #串并转换，将奇偶位分开，间隔为2，i是奇位 q是偶位
qdata = datanrz[1:nb:2]         
ich = []                          #创建一个1*nb/delta_T/2的零矩阵，以便后面存放奇偶位数据
qch = []         
for i in range(int(nb/2)):
    ich += [idata[i]]*int(1/delta_T)    #奇位码元转换为对应的波形信号
    qch += [qdata[i]]*int(1/delta_T)    #偶位码元转换为对应的波形信号

a = []     #余弦函数载波
b = []     #正弦函数载波
for j in range(int(N/2)):
    a.append(np.math.sqrt(2/T)*np.math.cos(2*np.math.pi*fc*t[j]))    #余弦函数载波
    b.append(np.math.sqrt(2/T)*np.math.sin(2*np.math.pi*fc*t[j]))    #正弦函数载波

idata1 = np.array(ich)*np.array(a)          #奇数位数据与余弦函数相乘，得到一路的调制信号
qdata1 = np.array(qch)*np.array(b)          #偶数位数据与余弦函数相乘，得到另一路的调制信号
s = idata1 + qdata1      #将奇偶位数据合并，s即为QPSK调制信号

s11 = wgn(s, SNR)     #高斯噪声曲线
s1 = s + s11          #加上高斯信道之后的信号 



plt.figure(figsize=(14,12))
plt.subplot(3,1,1)
plt.plot(idata1)
%plt.title('同相支路I',fontproperties=font, fontsize=20)
plt.axis([0,500,-6,6])
plt.subplot(3,1,2)
plt.plot(qdata1)
%plt.title('正交支路Q',fontproperties=font, fontsize=20)
plt.axis([0,500,-6,6])
plt.subplot(3,1,3)
plt.plot(s1)
%plt.title('调制信号',fontproperties=font, fontsize=20)
plt.axis([0,500,-6,6])
plt.show()













import commpy as cpy
bits = np.random.binomial(n=1,p=0.5,size=(128))
def Function():
    Modulation_type ="BPSK"
    if Modulation_type=="BPSK":
        bpsk = cpy.PSKModem(2)
        symbol = bpsk.modulate(bits)
        return symbol
    elif Modulation_type=="QPSK":
        qpsk = cpy.PSKModem(4)
        symbol = qpsk.modulate(bits)
        return symbol
    elif Modulation_type=="8PSK":
        psk8 = cpy.PSKModem(8)
        symbol = psk8.modulate(bits)
        return symbol
    elif Modulation_type=="8QAM":
        qam8 = cpy.QAMModem(8)
        symbol = qam8.modulate(bits)
        return symbol
    elif Modulation_type=="16QAM":
        qam16 = cpy.QAMModem(16)
        symbol = qam16.modulate(bits)
        return symbol
    elif Modulation_type=="64QAM":
        qam64 = cpy.QAMModem(64)
        symbol = qam64.modulate(bits)
        return symbol

x=[]
for i in symbol:
    x.append(i*i)
symbol[0]*symbol[0]
symbol[1]*symbol[1]


