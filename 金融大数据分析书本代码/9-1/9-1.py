1.逼近法
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

#生成平均分布的数列
x=np.linspace(-2*np.pi,2*np.pi,50)
#定义函数
def f(x):
    return np.sin(x)+0.5*x
	
#画二维坐标曲线
plt.plot(x,f(x),'b')
#画图中添加网格
plt.grid(True)
#一次最小二乘法
reg=np.polyfit(x,f(x),deg=1)
#一维多次函数通过系数矩阵求数列的函数值
ry=np.polyval(reg,x)
#画二维坐标曲线
plt.plot(x,ry,'r.',label='regression')
#生成4*len(x)的零矩阵
matrix=np.zeros((4,len(x)))
#矩阵第3行赋值
matrix[3,:]=x**3

reg=np.linalg.lstsq(matrix.T,f(x))[0]
x=np.linspace(-2*np.pi,2*np.pi,50)
matrix=np.zeros((4,len(x)))
2.单独的基函数
matrix[3,:]=x**3
matrix[2,:]=x**2
matrix[1,:]=x
matrix[0,:]=1
reg=np.linalg.lstsq(matrix.T,f(x))[0]
ry=np.dot(reg,matrix)
plt.plot(x,f(x),'b',label='f(x)')
plt.plot(x,ry,'r.',label='regression')
plt.legend(loc=0)
plt.grid(True)
plt.xlabel('x')
plt.ylabel('f(x)')

np.allclose(f(x),ry)


3.有噪声的数据
xn = np.linspace(-2*np.pi,2*np.pi,50)
xn=xn+0.15*np.random.standard_normal(len(xn))
yn=f(xn)+0.25*np.random.standard_normal(len(xn))





4.未排序的数据
xu=np.random.rand(50)*4*np.pi-2*np.pi

5.多维
def fm(x,y):
    return np.sin(x)+0.25*x+np.sqrt(y)+0.05*y**2
x=np.linspace(0,10,10)
y=np.linspace(0,10,10)
X,Y=np.meshgrid(x,y)
Z=fm(X,Y)
x=X.flatten()
y=Y.flatten()
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
fig=plt.figure(figsize=(9,6))
ax=fig.gca(projection='3d')
surf=ax.plot_surface(X,Y,Z,rstride=2,cstride=2,cmap=mpl.cm.coolwarm,linewidth=0.5,antialiased=True)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
fig.colorbar(surf,shrink=0.5,aspect=5)











