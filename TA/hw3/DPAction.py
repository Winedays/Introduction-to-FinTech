import numpy as np
import numpy as np
 
def myOptimAction(prices, trans_fee_rate):
    """
        method: dp on all four stock, buy all or sell all.
    """
    """
        prices.shape = (5, 2) day, stock_type
        stock_type 0 = money
        stock_type 1 = prices[0]'s val
    """
    dp = np.zeros((prices.shape[0]+1, prices.shape[1]+1))
    action = np.zeros((prices.shape[0]+1, prices.shape[1]+1), dtype=np.int64)
 
    # initial money is 1
    dp[0, 0] = 1000
    for i in range(1, dp.shape[1]):
        action[0, i] = -1
 
    for k in range(1, dp.shape[0]):
        t = k - 1
        # change type i to type j
        for i in range(0, dp.shape[1]):
            for j in range(0, dp.shape[1]):
                if i == j:
                    # no action
                    if dp[k, j] < dp[k-1, i]:
                        dp[k, j] = dp[k-1, i]
                        action[k, j] = i
                else:
                    new_val = 0
                    if i == 0 and j != 0:
                        # buy j
                        new_val = dp[k-1, i]*(1-trans_fee_rate)/prices[t, j-1]
                    elif i != 0 and j == 0:
                        # sell i
                        new_val = dp[k-1, i]*prices[t, i-1]*(1-trans_fee_rate)
                    else:
                        # sell i and buy j
                        current_money = (dp[k-1, i]*prices[t, i-1]*(1-trans_fee_rate))
                        new_val = current_money*(1-trans_fee_rate)/prices[t, j-1]
 
                    if dp[k, j] < new_val:
                        dp[k, j] = new_val
                        action[k, j] = i
 
 
    final = []
    for idx in range(dp.shape[1]):
        if idx == 0:
            final.append( dp[-1, idx] )
        else:
            final.append( dp[-1, idx] * prices[-1, idx-1] * (1-trans_fee_rate) )
    # print(final)
    stock_idx = np.argmax(final)
    # print(final[stock_idx])
    action_sequence = []
    asset_sequence = []
 
    t = dp.shape[0] - 1
    while t != 0:
        _from = action[t, stock_idx]
        _to = stock_idx
        action_sequence.append( (_from, _to) )
        asset_sequence.append( dp[t-1, _from] )
        stock_idx = _from
        t = t-1
 
    action_sequence.reverse()
    asset_sequence.reverse()
    # print(action_sequence)
    # print(asset_sequence)
    # print(dp)
    # print(action)
    action_matrix = []
    for t in range(0, len(action_sequence)):
        _from, _to = action_sequence[t]
        if _from == _to:
            continue
        act = []
        act.append(t)
        act.append(_from-1)
        act.append(_to-1)
 
        if _from == 0:
            act.append(asset_sequence[t])
        else:    
            act.append(asset_sequence[t]*prices[t, _from-1])
        action_matrix.append(act)
 
    return action_matrix
    
    
def myOptimActionOld(priceMat, transFeeRate):
    priceVec = []
    for vec in priceMat :
        priceVec.append( vec[0] )
        
    dataLen = len(priceMat)
    cash = 1000
    hold = 0
    cash_max = np.zeros(dataLen)
    hold_max = np.zeros(dataLen)
    cash_action = np.zeros(dataLen)
    hold_action = np.zeros(dataLen)
    
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
   
    print(cash_max)
    print(hold_max)
    
    
    actionMat = []
    best_action = np.zeros(dataLen)
    pre_action = 0

    if cash_action[-1] == -1 :
        best_action[-1] = -1
        pre_action = 1
        actionMat.append( [dataLen-1 ,0 ,-1 ,cash_max[i]] )
    elif hold_action[-1] == 1 :
        best_action[-1] = 1
        pre_action = -1
        actionMat.append( [dataLen-1 ,-1 ,0 ,hold_max[i]] )
    
    for i in range(dataLen-2,-1,-1) :
        if pre_action == -1 :
            best_action[i] = cash_action[i]
            if cash_action[i] == -1 :
                pre_action = 1
                actionMat.append( [i ,0 ,-1 ,cash_max[i]] )
        elif pre_action == 1 :
            best_action[i] = hold_action[i]
            if hold_action[i] == 1 :
                pre_action = -1
                actionMat.append( [i ,-1 ,0 ,hold_max[i]] )
        
    print(best_action)
    
    returnMat = []
    for i in range(len(actionMat)-1,-1,-1) :
        returnMat.append( actionMat[i] )
    # print(np.array( returnMat ))
    
    return returnMat

    