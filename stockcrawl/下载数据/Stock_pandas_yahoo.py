import pandas.io.data as web

print web.get_data_yahoo('AAPL','1/1/2014','20/8/2015')
#深圳股票
d = web.get_data_yahoo('002622.sz','1/1/2010','12/3/2017')
#上海股票
d = web.get_data_yahoo('601677.sz','1/1/2010','12/3/2017')
raw_input('hello')