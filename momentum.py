# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 14:33:07 2020

@author: joebe
"""

import statistics as stats 
import math as math
import pandas as pd
from pandas_datareader import data

start_date='2014-10-01'
end_date= '2018-01-01'

SRC_DATA_FILENAME='goog_data.pkl'

try:
    goog_data = pd.read_pickle(SRC_DATA_FILENAME)
    print('File data not found.. reading goog data')
except FileNotFoundError:
    goog_data = data.DataReader('GOOG', 'yahoo', start_date, end_date)
    goog_data.to_pickle(SRC_DATA_FILENAME)

goog_data_signal=pd.DataFrame(index=goog_data.index)
goog_data_signal['price'] = goog_data['Adj Close']

close=goog_data_signal['price']

time_period = 20 # how far to look back to find reference price to compute momentum
history = [] # history of observed prices to use in momentum calculation 
mom_values = [] # track momentum values for visualization purposes
for close_price in close: 
    history.append(close_price) 
    if len(history) > time_period: # history is at most 'time_period' number of observations   
        del (history[0])
    mom = close_price - history[0] 
    mom_values.append(mom) 

goog_data = goog_data.assign(ClosePrice=pd.Series(close, index=goog_data.index)) 
goog_data = goog_data.assign(MomentumFromPrice20DaysAgo=pd.Series(mom_values, index=goog_data.index)) 
close_price = goog_data['ClosePrice'] 
mom = goog_data['MomentumFromPrice20DaysAgo']
import matplotlib.pyplot as plt

fig = plt.figure() 
ax1 = fig.add_subplot(211, ylabel='Google price in $') 
close_price.plot(ax=ax1, color='g', lw=2., legend=True) 
ax2 = fig.add_subplot(212, ylabel='Momentum in $') 
mom.plot(ax=ax2, color='b', lw=2., legend=True) 
plt.show()