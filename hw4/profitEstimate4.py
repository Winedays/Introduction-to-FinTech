import sys
import numpy as np
import pandas as pd
from myStrategy4 import myStrategy

bestRate = 1.05888507
for i in range(100,600) :
    
    if i % 10 == 0 :
        print( "iteration : %d " %(i))
    for j in range(15) :
        for k in range(20) :
            windowSize = i
            alpha = j 
            beta = k
            
            df = pd.read_csv(sys.argv[1])
            adjClose = df["Adj Close"].values
            capital=1
            capitalOrig=capital
            dataCount=len(adjClose)
            suggestedAction= np.zeros((dataCount,1))
            stockHolding=np.zeros((dataCount,1))
            total = np.zeros((dataCount,1))
            realAction=np.zeros((dataCount,1))
            total[0] = capital
            for ic in range(dataCount):
                currPrice=adjClose[ic]
                suggestedAction[ic]=myStrategy(adjClose[0:ic], currPrice,windowSize,alpha,beta)
                if ic > 0:
                    stockHolding[ic]=stockHolding[ic-1]
                if suggestedAction[ic] == 1:
                    if stockHolding[ic]==0:            
                        stockHolding[ic]=capital/currPrice
                        capital=0
                        realAction[ic]=1
                elif suggestedAction[ic] == -1:
                    if stockHolding[ic]>0:
                        capital=stockHolding[ic]*currPrice
                        stockHolding[ic]=0
                        realAction[ic]=-1
                elif suggestedAction[ic] == 0:
                    realAction[ic]=0
                else:
                    assert False
                total[ic]=capital+stockHolding[ic]*currPrice
            returnRate=(total[-1]-capitalOrig)/capitalOrig     
            #print(returnRate)
            
            if returnRate > bestRate :
                bestRate = returnRate
                print( "windowSize = %d | alpha = %d | beta = %d" % (windowSize,alpha,beta) )
                print( "bestRate = %f " % (bestRate) )
                
