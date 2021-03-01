def profitEstimateOpen(priceVec, transFeeRate, actionVec):
    import numpy as np
    import pandas as pd
    
    capital=1
    capitalOrig=capital
    dataCount=len(priceVec)
    suggestedAction=actionVec
    stockHolding=np.zeros((dataCount,1))
    total = np.zeros((dataCount,1))
    realAction=np.zeros((dataCount,1))
    total[0] = capital
    for ic in range(dataCount):
        currPrice = priceVec[ic]
        if ic > 0:
            stockHolding[ic]=stockHolding[ic-1]
        if suggestedAction[ic] == 1:
            if stockHolding[ic]==0:            
                stockHolding[ic]=capital*(1-transFeeRate)/currPrice
                capital=0
                realAction[ic]=1
        elif suggestedAction[ic] == -1:
            if stockHolding[ic]>0:
                capital=stockHolding[ic]*currPrice*(1-transFeeRate)
                stockHolding[ic]=0
                realAction[ic]=-1
        elif suggestedAction[ic] == 0:
            realAction[ic]=0
        else:
            assert False
        total[ic]=capital+stockHolding[ic]*currPrice
    returnRate=(total[-1]-capitalOrig)/capitalOrig
    return returnRate
