# -*- coding:utf-8 -*-
 
import numpy as np
from math import pi
import matplotlib.pyplot as plt
import matplotlib
import math
 
 
 
#码元数
 
size = 10
sampling_t = 0.01
t = np.arange(0, size, sampling_t)
 

# 随机生成信号序列
a = np.random.randint(0, 2, size)
m = np.zeros(len(t), dtype=np.float32)
for i in range(len(t)):
    m[i] = a[math.floor(t[i])]

fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1)
 
ax1.set_title('generate Random Binary signal', fontsize = 20)
plt.axis([0, size, -0.5, 1.5])
plt.plot(t, m, 'b')

fc = 4000
fs = 20 * fc # 采样频率
ts = np.arange(0, (100 * size) / fs, 1 / fs)
coherent_carrier = np.cos(np.dot(2 * pi * fc, ts))
 
bpsk = np.cos(np.dot(2 * pi * fc, ts) + pi * (m - 1) + pi / 4)

# BPSK调制信号波形
ax2 = fig.add_subplot(2, 1, 2)
ax2.set_title('BPSK Modulation', fontsize=20)#, fontproperties=zhfont1
plt.axis([0,size,-1.5, 1.5])
plt.plot(t, bpsk, 'r')
plt.show()
print()



