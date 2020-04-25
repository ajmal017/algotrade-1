# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 11:42:57 2020

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

time_period = 20 # history length for Simple Moving Average for middle band 
stdev_factor = 2 # Standard Deviation Scaling factor for the upper and lower bands
history = [] # price history for computing simple moving average 
sma_values = [] # moving average of prices for visualization purposes 
upper_band = [] # upper band values 
lower_band = [] # lower band values
for close_price in close: 
    history.append(close_price) 
    if len(history) > time_period: # we only want to maintain at most 'time_period' number of price observations  
        del (history[0])
    sma = stats.mean(history) 
    sma_values.append(sma) # simple moving average or middle band
    variance = 0 # variance is the square of standard deviation
    for hist_price in history:   
        variance = variance + ((hist_price - sma) ** 2)
    stdev = math.sqrt(variance / len(history)) # use square root to get
    upper_band.append(sma + stdev_factor * stdev) 
    lower_band.append(sma - stdev_factor * stdev)

goog_data = goog_data.assign(ClosePrice=pd.Series(close, index=goog_data.index))
goog_data = goog_data.assign(MiddleBollingerBand20DaySMA=pd.Series(sma_values, index=goog_data.index))
goog_data = goog_data.assign(UpperBollingerBand20DaySMA2StdevFactor=pd.Series(upper_band, index=goog_data.index)) 
goog_data = goog_data.assign(LowerBollingerBand20DaySMA2StdevFactor=pd.Series(lower_band, index=goog_data.index)) 
close_price = goog_data['ClosePrice']
mband = goog_data['MiddleBollingerBand20DaySMA'] 
uband = goog_data['UpperBollingerBand20DaySMA2StdevFactor'] 
lband = goog_data['LowerBollingerBand20DaySMA2StdevFactor']

import matplotlib.pyplot as plt
fig = plt.figure() 
ax1 = fig.add_subplot(111, ylabel='Google price in $') 
close_price.plot(ax=ax1, color='g', lw=2., legend=True) 
mband.plot(ax=ax1, color='b', lw=2., legend=True) 
uband.plot(ax=ax1, color='g', lw=2., legend=True) 
lband.plot(ax=ax1, color='r', lw=2., legend=True) 
plt.show()