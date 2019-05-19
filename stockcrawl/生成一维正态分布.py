
import numpy as np
import matplotlib.pyplot as plt
import math



if __name__=="__main__":
    Showrand()


sampleNo = 1000;
#通过正态分布公式绘图
def ShowRand():
    u = 0.6  # 均值μ
    u01 = -2
    sig = math.sqrt(10) # 标准差δ
    x = np.linspace(u - 3*sig, u + 3*sig, 50)
    y_sig = np.exp(-(x - u) ** 2 /(2* sig **2))/(math.sqrt(2*math.pi)*sig)
    print(x)
    print("="*20)
    print(y_sig)
    plt.plot(x, y_sig, "r-", linewidth=2)
    plt.grid(True)
    plt.show()


def ShowRand2(mu,sigma):
    # 一维正态分布
    # 下面三种方式是等效的
    np.random.seed(0)
    s = np.random.normal(mu, sigma, sampleNo )
    plt.subplot(141)
    plt.hist(s, 30, normed=True)
    np.random.seed(0)
    s = sigma * np.random.randn(sampleNo ) + mu
    plt.subplot(142)
    plt.hist(s, 30, normed=True)
    np.random.seed(0)
    s = sigma * np.random.standard_normal(sampleNo ) + mu
    plt.subplot(143)
    plt.hist(s, 30, normed=True)
    # 二维正态分布
    mu = np.array([[1, 5]])
    Sigma = np.array([[1, 0.5], [1.5, 3]])
    R = cholesky(Sigma)
    s = np.dot(np.random.randn(sampleNo, 2), R) + mu
    plt.subplot(144)
    # 注意绘制的是散点图，而不是直方图
    plt.plot(s[:,0],s[:,1],'+')
    plt.show()



