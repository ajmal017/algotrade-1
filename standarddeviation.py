# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 14:21:53 2020

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


time_period = 20 # look back period
history = [] # history of prices 
sma_values = [] # to track moving average values for visualization purposes 
stddev_values = [] # history of computed stdev values 
for close_price in close: 
    history.append(close_price) 
    if len(history) > time_period: # we track at most 'time_period' number of prices   
        del (history[0])
    sma = stats.mean(history) 
    sma_values.append(sma)
    variance = 0 # variance is square of standard deviation 
    for hist_price in history:   
        variance = variance + ((hist_price - sma) ** 2)
    stdev = math.sqrt(variance / len(history)) 
    stddev_values.append(stdev)
goog_data = goog_data.assign(ClosePrice=pd.Series(close, index=goog_data.index)) 
goog_data = goog_data.assign(StandardDeviationOver20Days=pd.Series(stddev_values, index=goog_data.index)) 
close_price = goog_data['ClosePrice'] 
stddev = goog_data['StandardDeviationOver20Days']
import matplotlib.pyplot as plt
fig = plt.figure() 
ax1 = fig.add_subplot(211, ylabel='Google price in $') 
close_price.plot(ax=ax1, color='g', lw=2., legend=True) 
ax2 = fig.add_subplot(212, ylabel='Stddev in $') 
stddev.plot(ax=ax2, color='b', lw=2., legend=True) 
plt.show()