import sys
import numpy as np
import pandas as pd
from myOptimAction_loop import myOptimAction
from profitEstimateOpen import profitEstimateOpen
df = pd.read_csv(sys.argv[1])
transFeeRate= float(sys.argv[2])
priceVec = df["Adj Close"].values
max_rate = 0.
best_weight = []
for i in range( 6 ) :
    print( 'interation : ' + str(i) )
    for j in range( 6 ) :
        for m in range( 1,101 ) :
            for n in range( 1,101 ) :
                    actionVec = myOptimAction(priceVec, transFeeRate , i , j , -1/m , -1/n  )
                    returnRate = profitEstimateOpen(priceVec, transFeeRate, actionVec)
                    if returnRate > max_rate :
                        max_rate = returnRate
                        best_weight = [ i , j , m , n ]
                        print( 'returnRate : ' + str(returnRate) )
                        print( 'best_weight : ' + str(best_weight) )
print( 'max_rate : ' + str(max_rate) )
print( 'best_weight[ conCount  , alpha , beta , rsi_alpha , rsi_beta ] : ' + str(best_weight) )