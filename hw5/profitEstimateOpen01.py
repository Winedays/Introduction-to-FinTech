import sys
import numpy as np
import pandas as pd
from myOptimAction import myOptimAction
from profitEstimateOpen import profitEstimateOpen
df = pd.read_csv(sys.argv[1])
transFeeRate= float(sys.argv[2])
priceVec = df["Adj Close"].values
actionVec = myOptimAction(priceVec, transFeeRate)
returnRate = profitEstimateOpen(priceVec, transFeeRate, actionVec)
f = open( "action.txt" , 'w' )
f.write( ','.join(actionVec.astype(str).tolist()) )
f.close()
print( 'returnRate : ' + str(returnRate) )