from numpy import *

def loadData():
    return mat([[1,1,1,0,0],
             [2,2,2,0,0],
             [3,3,3,0,0],
             [5,5,3,2,2],
             [0,0,0,3,3],
             [0,0,0,6,6]])
mat1 = loadData()
mat2 = mat1.H
print(mat2)