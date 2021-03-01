# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 17:15:50 2018

@author: USER
"""
import pandas as pd
import numpy as np

def readFile( file ) :
    df = pd.read_csv( 'SPY.csv' )  #讀取 CSV 檔案
    df.drop( df[ df.columns[ [1,2,3,4,6] ] ] , axis=1 , inplace=True )  # only need the data of Adj Close
    return df.values

def MAcalculator( data , day ) :
    ma_list = [] 
    # calculate the ma that data quantity are less than ma_day
    for i in range( day ):
#        adj_sum = 0
#        for j in range( 0 , i+1 ):
#            adj_sum += data[j] ;
#        ma = adj_sum / (i+1)
        ma = np.mean(data[0 : i+1])
        ma_list.append( ma )
    # calculate the ma
    for i in range( day , len(data) ):
#        adj_sum = 0
#        for j in range( i + 1 - day , i + 1 ) :
#            adj_sum += data[j] ;
#        ma = adj_sum / day
        ma = np.mean(data[i+1-day : i+1])
        ma_list.append( ma )
    return np.array(ma_list)

def RSIcalculator( data , day ) :
    rsi_list = [ 0 ] 
    # calculate the difference of each day , and set day one difference is zero 
    diff_list = [ 0 ] 
    for i in range( 1 , len(data) ) :
        diff_list.append( data[i] - data[i-1] )
    # calculate the rsi that data quantity are less than rsi_day
    for i in range( 1,day ):
        # sum all upward change
        upward_change = sum( x for x in diff_list[1 : i+1] if x>=0  )
        rsi = upward_change / np.sum( np.abs( diff_list[1 : i+1] ) )
        rsi_list.append( rsi )
    # calculate the rsi
    for i in range( day , len(data) ):
        # sum all upward change
        upward_change = sum( x for x in diff_list[i+1-day : i+1] if x>=0  )
        rsi = upward_change / np.sum( np.abs( diff_list[i+1-day : i+1] ) )
        rsi_list.append( rsi )
    #print( np.array(rsi_list) )
    return np.array(rsi_list)
    
def addData( data , list_ ) :
    data = np.hstack( ( data,list_.reshape((2724,1)) ) )
    return data
    

def myStrategy():
    x=0 
    
if __name__ == "__main__" :
    # main function start
    spy_data = readFile( 'SPY.csv' ) 
    print( len(spy_data) )
    ma5_list = MAcalculator( spy_data.T[1] , 5 ) # get 5 ma of spy
    spy_data = addData( spy_data , ma5_list )
    
    ma14_list = MAcalculator( spy_data.T[1] , 14 ) # get 14 ma of spy
    spy_data = addData( spy_data , ma14_list )
    
    rsi5_list = RSIcalculator( spy_data.T[1] , 5 )  # get 5 day rsi of spy
    spy_data = addData( spy_data , rsi5_list )
    
    rsi14_list = RSIcalculator( spy_data.T[1] , 14 )  # get 14 day rsi of spy
    spy_data = addData( spy_data , rsi14_list )
    print( spy_data )
    
    start = 365
    
    