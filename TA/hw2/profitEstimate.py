import sys
import numpy as np
import pandas as pd
from myStrategy_ma_ls import myStrategy

def calculateReturnRate( file, stocksType ) :
    capital=1
    capitalOrig=capital  # cost
    
    # read file
    df = pd.read_csv(file)
    adjClose = df["Adj Close"].values
    dataCount=len(adjClose)
    
    # setting
    suggestedAction= np.zeros((dataCount,1))
    stockHolding=np.zeros((dataCount,1))
    total = np.zeros((dataCount,1))
    realAction=np.zeros((dataCount,1))
    
    total[0] = capital
    for ic in range(dataCount):
        currPrice=adjClose[ic]
        suggestedAction[ic]=myStrategy(adjClose[0:ic], currPrice, stocksType)
        
        # get real action by suggested action
        if ic > 0:
            stockHolding[ic]=stockHolding[ic-1]
        if suggestedAction[ic] == 1:
            if stockHolding[ic]==0: # buy    
                stockHolding[ic]=capital/currPrice
                capital=0
                realAction[ic]=1
        elif suggestedAction[ic] == -1:
            if stockHolding[ic]>0:  # sell
                capital=stockHolding[ic]*currPrice
                stockHolding[ic]=0
                realAction[ic]=-1
        elif suggestedAction[ic] == 0: # hold
            realAction[ic]=0
        else:
            assert False
        total[ic]=capital+stockHolding[ic]*currPrice
    returnRate=(total[-1]-capitalOrig)/capitalOrig 
    return returnRate
    
returnRate_SPY = calculateReturnRate( sys.argv[1], "SPY" ) # SPY.csv
returnRate_IAU = calculateReturnRate( sys.argv[2], "IAU" ) # IAU.csv
returnRate_LQD = calculateReturnRate( sys.argv[3], "LQD" ) # LQD.csv
returnRate_DSI = calculateReturnRate( sys.argv[4], "DSI" ) # DSI.csv
totalReturnRate = returnRate_SPY + returnRate_IAU + returnRate_LQD + returnRate_DSI
print( returnRate_SPY )
print( returnRate_IAU )
print( returnRate_LQD )
print( returnRate_DSI )
print( totalReturnRate )