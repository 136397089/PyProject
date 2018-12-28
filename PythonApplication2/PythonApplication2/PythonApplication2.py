import numpy as np
import pandas as pd
import pandas.io.data as web

goog = web.get_data_yahoo('GOOG','3/14/2009','2/14/2014')
goog['Log_Ret'] = np.log(goog['Close']/goog['Close'].shift(1))
goog['Volatility'] = pd.rolling_std(goog['Log_Ret'],window=252)*np.sqrt(252)

#%matplotlib inline
#goog[['Close','Volatility']].plot(subplots=True,color='blue',figsize=(20,12))
print goog
raw_input('hello')


print('Hello World')
