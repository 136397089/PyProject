

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from pandas import Series, DataFrame

excelFileName = 'x.xlsx'

df = pd.read_excel(excelFileName)#读文件
df = df.replace({np.nan:0})#按照字典替换表内元素
print(df)
print (os.getcwd())
