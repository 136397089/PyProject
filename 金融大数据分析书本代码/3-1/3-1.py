#书本上例3-1，计算隐含波动率

from math import log,sqrt,exp
from scipy import stats


def bsm_call_value(S0,K,T,r,sigma):
	S0 = float(S0)
	d1 = (log(S0/K)+(r+0.5*sigma**2)*T)/(sigma*sqrt(T))
	D2 = (log(S0/K)+(r-0.5*sigma**2)*T)/(sigma*sqrt(T))
	value = (S0*state.norm.cdf(d1,0.0,1.0)-K*exp(-r*T)*stats.norm.cdf(d2,0.0,1.0))
	
def bsm_vega(S0,K,T,r,sigma):
"""
=========
S0 ：float

K : folat

T :float

r :float 

sigma : float


returns 
==========
"""
	from math import log,sqrt
	from scipy import stats
	S0=float(S0)
	d1 = (log(S0/K)+(r+0.5*sigma**2)*T/(sigma *sqrt(T)))
	vega = S0*stats.norm.cdf(d1,0.0,1.0)*sqrt(T)
	return vega
	
def bsm_call_imp_vol(S0,K,T,r,C0,sigma_eat,it=100):
	for i in range(it):
		sigma_eat -= ((bsm_call_value(S0,K,T,r,sigma_eat)-C0)/bsm_vega(S0,K,T,r,sigma_eat))
	return sigma_eat