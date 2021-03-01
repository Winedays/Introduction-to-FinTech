import sys
import numpy as np
import pandas as pd

# 判斷當天action
def myStrategy(pastData, currPrice, windowSize, alpha, beta):
    import numpy as np

    action = 0  # action : 1(buy), -1(sell), 0(hold)
    dataLen = len(pastData) # 資料天數
    ma = 0 ;
    if dataLen == 0 : 
        return 0
    elif dataLen<windowSize:    
        #當資料天數<windowSize, 以資料天數計算ma
        ma=np.mean(pastData)
    else :
        # 向前看windowSize天數的資料, 算ma
        windowedData=pastData[-windowSize:] 
        ma=np.mean(windowedData)
    if (currPrice-alpha)>ma : 
        # 價格>均線: 買
        action=1
    elif (currPrice+beta)<ma :
        # 價格<均線: 賣
        action=-1
    else:
        action=0
    return action

if __name__ == '__main__':
    bestRate = 1.00  # return rate baseline
        
    # read stock file    
    df = pd.read_csv(sys.argv[1])
    adjClose = df["Adj Close"].values  # get adj close
    dataCount=len(adjClose) # day size
    # try window_size
    for windowSize in range(0,30) :
        # iteration log
        if windowSize % 10 == 0 :
            print( "iteration : %d " %(windowSize))
        # try alpha
        for alpha in range(10) :
            # try beta
            for beta in range(20) :
                # init.
                capital=1  # 持有資金
                capitalOrig=capital  # cost
                suggestedAction= np.zeros((dataCount,1))  # 判斷action
                stockHolding=np.zeros((dataCount,1))  # 持有股票
                total = np.zeros((dataCount,1))  # 結算資金
                realAction=np.zeros((dataCount,1))  # 實際action
                
                # run each day
                for ic in range(dataCount):
                    currPrice=adjClose[ic]  # 當天價格
                    suggestedAction[ic]=myStrategy(adjClose[0:ic], currPrice,windowSize,alpha,beta) # 取得當天action
                    
                    # get real action by suggested action
                    if ic > 0: 
                        # 更新手上持有股票
                        stockHolding[ic]=stockHolding[ic-1]
                    if suggestedAction[ic] == 1:
                        # 若未持有股票: 買
                        if stockHolding[ic]==0:            
                            stockHolding[ic]=capital/currPrice # 買入股票
                            capital=0   # 持有資金
                            realAction[ic]=1
                    elif suggestedAction[ic] == -1:
                        # 若持有股票： 賣
                        if stockHolding[ic]>0:
                            capital=stockHolding[ic]*currPrice # 賣出股票
                            stockHolding[ic]=0  # 持有股票
                            realAction[ic]=-1
                    elif suggestedAction[ic] == 0:
                        # 不買不賣
                        realAction[ic]=0
                    else:
                        assert False
                    # 當天結算資金
                    total[ic]=capital+stockHolding[ic]*currPrice
                # 最終盈利率
                returnRate=(total[-1]-capitalOrig)/capitalOrig 
                # 比較最佳盈利率
                if returnRate > bestRate :
                    bestRate = returnRate
                    print( "windowSize = %d | alpha = %d | beta = %d" % (windowSize,alpha,beta) )
                    print( "bestRate = %f " % (bestRate) )
                
