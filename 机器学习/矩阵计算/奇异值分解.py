from numpy import *

def loadData():
    return mat([[1,1,1,0,0],
             [2,2,2,0,0],
             [3,3,3,0,0],
             [5,5,3,2,2],
             [0,0,0,3,3],
             [0,0,0,6,6]])

data=loadData()
u,sigma,vt=linalg.svd(data)
print sigma

sig2 = mat([[sigma[0], 0],
            [0, sigma[1]]])

print(u[:,:2]*sig2*vt[:2,:])
print(u)
print(vt)
