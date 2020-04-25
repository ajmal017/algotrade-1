# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 13:57:38 2020

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

time_period = 20 # look back period to compute gains & losses
gain_history = [] # history of gains over look back period (0 if no gain, magnitude of gain if gain) 
loss_history = [] # history of losses over look back period (0 if no loss, magnitude of loss if loss)

avg_gain_values = [] # track avg gains for visualization purposes 
avg_loss_values = [] # track avg losses for visualization purposes
rsi_values = [] # track computed RSI values
last_price = 0 # current_price - last_price > 0 => gain. current_price last_price < 0 => loss.
for close_price in close: 
    if last_price == 0:  
        last_price = close_price
    gain_history.append(max(0, close_price - last_price)) 
    loss_history.append(max(0, last_price - close_price)) 
    last_price = close_price
    if len(gain_history) > time_period: # maximum observations is equal to lookback period   
        del (gain_history[0])   
        del (loss_history[0])
    avg_gain = stats.mean(gain_history) # average gain over lookback period 
    avg_loss = stats.mean(loss_history) # average loss over lookback period 
    avg_gain_values.append(avg_gain) 
    avg_loss_values.append(avg_loss)
    rs = 0 
    if avg_loss > 0: # to avoid division by 0, which is undefined   
        rs = avg_gain / avg_loss 
    rsi = 100 - (100 / (1 + rs)) 
    rsi_values.append(rsi)
    
goog_data = goog_data.assign(ClosePrice=pd.Series(close, index=goog_data.index)) 
goog_data = goog_data.assign(RelativeStrengthAvgGainOver20Days=pd.Series(avg_gain_values, index=goog_data.index))
goog_data = goog_data.assign(RelativeStrengthAvgLossOver20Days=pd.Series(avg_loss_values, index=goog_data.index)) 
goog_data = goog_data.assign(RelativeStrengthIndicatorOver20Days=pd.Series(rsi_values, index=goog_data.index)) 
close_price = goog_data['ClosePrice'] 
rs_gain = goog_data['RelativeStrengthAvgGainOver20Days'] 
rs_loss = goog_data['RelativeStrengthAvgLossOver20Days'] 
rsi = goog_data['RelativeStrengthIndicatorOver20Days']
import matplotlib.pyplot as plt
fig = plt.figure() 
ax1 = fig.add_subplot(311, ylabel='Google price in $') 
close_price.plot(ax=ax1, color='black', lw=2., legend=True) 
ax2 = fig.add_subplot(312, ylabel='RS') 
rs_gain.plot(ax=ax2, color='g', lw=2., legend=True) 
rs_loss.plot(ax=ax2, color='r', lw=2., legend=True) 
ax3 = fig.add_subplot(313, ylabel='RSI') 
rsi.plot(ax=ax3, color='b', lw=2., legend=True) 
plt.show()
