import numpy as np

def myOptimAction(priceVec, transFeeRate):
    return GreedyAlgo(priceVec, transFeeRate)

def GreedyAlgo(priceVec, transFeeRate) :
    dataLen = len(priceVec)
    cash = 1
    hold = 0
    cash_max = np.zeros(dataLen)
    hold_max = np.zeros(dataLen)
    cash_action = np.zeros(dataLen)
    hold_action = np.zeros(dataLen)
    
    curprofit = 1 # 由上次賣出到目前為止的利潤
    
    for i in range(dataLen) :
        #手上有現金的最大化 = Max(昨天有股票今天有現金, 昨天有現金今天有現金）
        cash_max[i] = max(hold*priceVec[i]*(1-transFeeRate),cash)
        if cash_max[i] > cash :
            cash_action[i] = -1
        
        #手上有股票的最大化 = Max( 昨天有股票今天有股票,昨天有現金今天有股票）
        hold_max[i] = max(hold,cash*(1-transFeeRate)/priceVec[i])
        if hold_max[i] > hold :
            hold_action[i] = 1
            
            
        cash = cash_max[i]
        hold = hold_max[i]
        hold_max[i] = hold_max[i]*priceVec[i]*(1-transFeeRate)
    
    
    print(cash,hold*priceVec[-1]*(1-transFeeRate))
   
    print(cash_action)
    print(hold_action)
    
    best_action = np.zeros(dataLen)
    pre_action = 0

    # if cash_action[-1] == -1 :
        # best_action[-1] = -1
        # pre_action = 1
    # elif hold_action[-1] == 1 :
        # best_action[-1] = 1
        # pre_action = -1
    
    for i in range(dataLen-1,-1,-1) :
        if pre_action == 0 :
            if cash_action[i] == -1 :
                best_action[i] = -1
                pre_action = 1
            elif hold_action[i] == 1 :
                best_action[i] = 1
                pre_action = -1
        elif pre_action == -1 :
            best_action[i] = cash_action[i]
            if cash_action[i] == -1 :
                pre_action = 1
        elif pre_action == 1 :
            best_action[i] = hold_action[i]
            if hold_action[i] == 1 :
                pre_action = -1
        
    print(best_action)
    return best_action
        
    