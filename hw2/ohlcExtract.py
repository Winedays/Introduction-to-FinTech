# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 02:36:56 2018
FinTech hw 2 : compute the OHLC of 台指期 within a given date based on minute-based trading record.
@author: Adler
"""
import sys
import pandas as pd
 
file = sys.argv[1] ;
 
df = pd.read_csv( file , encoding="big5")  #讀取 CSV 檔案
# only need the data of product code = "TX"
df.drop( df[ df[ df.columns[1]].str.strip() != "TX" ].index , axis=0 , inplace=True )
 
# the maximum date = the trading date we need , the minimum month = expiration month is next month
trading_date = max(df[ df.columns[0] ])  # 交易日期
expiration_month_list = df[ df.columns[2] ].astype(str).values
#expiration_month_list = [ x[0:6] for x in expiration_month_list ]
df.drop( df[ df[ df.columns[2] ].str.len() > 11.0 ].index , axis=0 , inplace=True )
expiration_month =  min( df[ df.columns[2] ].astype(str).values )  # 到期月份
print( expiration_month )
# only need the data on trading date and its expiration month is next month
df.drop( df[ df[ df.columns[0] ] != trading_date ].index , axis=0 , inplace=True )
df.drop( df[ df[ df.columns[2] ].astype(str).values != str(expiration_month) ].index , axis=0 , inplace=True )
 
# only need the data between 08:45 ~ 13:45
df.drop( df[ df[ df.columns[3] ] < 84500 ].index , axis=0 , inplace=True )
df.drop( df[ df[ df.columns[3] ] > 134500 ].index , axis=0 , inplace=True )
 
# remove the data which trading prcie < 0
df.drop( df[ df[ df.columns[4] ] <= 0 ].index , axis=0 , inplace=True )
 
df.drop( df[ df.columns[ [0,1] ] ] , axis=1 , inplace=True )  # use for console debug
 
# sort data by trading time
df.sort_values(by=[df.columns[1]] , inplace=True )
 
# get all trading price by a list
trading_price_list = df[ df.columns[2] ].astype(int).values
 
# get OHLC
open_price = trading_price_list[0]
close_price = trading_price_list[ len(trading_price_list) - 1 ]
high_price = max( trading_price_list )
low_price = min( trading_price_list )
 
print( open_price , high_price , low_price , close_price )