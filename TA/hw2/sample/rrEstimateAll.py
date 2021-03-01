# How to invoke this program:
#	python rrEstimateAll.py
import sys
import numpy as np
import pandas as pd
from test import myStrategy

# Compute return rate over a given price vector, with 3 modifiable parameters
def computeReturnRate(priceVec, stockType):
	capital=1000	# Initial capital at hand (持有資金)
	capitalOrig=capital	 # original capital
	dataCount=len(priceVec)				# day size
	suggestedAction=np.zeros((dataCount,1))	# 判斷action
	stockHolding=np.zeros((dataCount,1))  # 持有股票
	total=np.zeros((dataCount,1))	 # 結算資金
	realAction=np.zeros((dataCount,1))	# Real action, which might be different from suggested action. For instance, when the suggested action is 1 (buy) but you don't have any capital, then the real action is 0 (hold, or do nothing). 
	# Run through each day
	for ic in range(dataCount):
		currentPrice=priceVec[ic]	# 當天價格
		suggestedAction[ic]=myStrategy(priceVec[0:ic], currentPrice, stockType)		# 取得當天 suggested action
		# get real action by suggested action
		if ic>0:
			stockHolding[ic]=stockHolding[ic-1]	# 更新手上持有股票
		if suggestedAction[ic]==1:	# 建議「買」
			if stockHolding[ic]==0:		# 若未持有股票==>買
				stockHolding[ic]=capital/currentPrice # 買入股票
				capital=0	# 持有資金
				realAction[ic]=1
		elif suggestedAction[ic]==-1:	# 建議「賣」
			if stockHolding[ic]>0:		# 若持有股票==>賣
				capital=stockHolding[ic]*currentPrice # 賣出股票
				stockHolding[ic]=0	# 持有股票
				realAction[ic]=-1
		elif suggestedAction[ic]==0:	# 不買不賣
			realAction[ic]=0
		else:
			assert False
		total[ic]=capital+stockHolding[ic]*currentPrice	# 當天結算資金
	returnRate=(total[-1]-capitalOrig)/capitalOrig		# Return rate of this run
	return returnRate
	
if __name__=='__main__':
	# fileList=['../SPY.csv', '../DSI.csv', '../IAU.csv', '../LQD.csv']
	fileList=['SPY_test.csv', 'DSI_test.csv', 'IAU_test.csv', 'LQD_test.csv']
	fileCount=len(fileList);
	rr=np.zeros((fileCount,1))
	for ic in range(fileCount):
		file=fileList[ic];
		df=pd.read_csv(file)	
		adjClose=df["Adj Close"].values	# Get adj close as the price vector
		stockType=file[-7:-4]		# Get stock type
		rr[ic]=computeReturnRate(adjClose, stockType)	# Compute return rate
		print("file=%s ==> rr=%f" %(file, rr[ic]));
	print("Average return rate = %f" %(np.mean(rr)))