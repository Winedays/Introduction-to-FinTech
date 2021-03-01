# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 15:41:27 2018

@author: USER
"""
import numpy as np
import pandas as pd
import random

def RSIcalculator( data ) :
    diff_list = [ 0 ] 
    for i in range( 1 , len(data) ) :
        diff_list.append( data[i] - data[i-1] )
    # calculate the rsi that data quantity are less than rsi_day
    # sum all upward change
    upward_change = sum( x for x in diff_list if x>=0  )
    rsi = upward_change / np.sum( np.abs( diff_list ) )
    #print( np.array(rsi_list) )
    return rsi
    
def myStrategy(dailyOhlcvFile , minutelyOhlcvFile , openPricev ):
    
    dailyOhlcvFile = dailyOhlcvFile[['close']].values
    pastData = dailyOhlcvFile
    currPrice = dailyOhlcvFile[-1]
    
    #param=[4,5]
    windowSize= random.randint(5,20)
    alpha= random.randint(3,10) + 200
    beta= random.randint(3,10) + 200
    action=0
    ma=0
    dataLen = len(pastData)
    if dataLen<windowSize:
        #ma=np.mean(pastData)
        return 0
    else :
        windowedData=pastData[-windowSize:]
        ma_l=np.mean(windowedData)
        ma_s=np.mean(windowedData[:int(windowSize/2)])
        rsi_l=RSIcalculator(windowedData)
        rsi_s=RSIcalculator(windowedData[:5])
    if (ma_s>ma_l and (currPrice-alpha)>ma_l) or (rsi_s>rsi_l and (currPrice-alpha)>rsi_l) :
        action=1
    elif (ma_s<ma_l and (currPrice+beta)<ma_l) or (rsi_s<rsi_l and (currPrice+beta)<rsi_l) :
        action=-1
    else:
        action=0
    return action
