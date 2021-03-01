def myStrategy(pastData, currPrice, stockType):
    import numpy as np
    
    # 設定參數
    paramSetting = {'SPY': {'alpha':6, 'beta':16, 'windowSize':4},
                    'IAU': {'alpha':0, 'beta':2, 'windowSize':26},
                    'LQD': {'alpha':0, 'beta':1, 'windowSize':5},
                    'DSI': {'alpha':2, 'beta':10, 'windowSize':17}}
    windowSize = paramSetting[stockType]['windowSize']
    alpha = paramSetting[stockType]['alpha']
    beta = paramSetting[stockType]['beta']
    
    action = 0  # action : 1(buy), -1(sell), 0(hold)
    dataLen = len(pastData) # 資料天數
    ma = 0
    if dataLen == 0 : 
        return 0
    elif dataLen<windowSize:    
        #當資料天數<windowSize, 以資料天數計算ma
        ma=np.mean(pastData)
    else :
        # 向前看windowSize天數的資料, 算ma
        windowedData=pastData[-windowSize:] 
        ma=np.mean(windowedData)
    if (currPrice-alpha)>ma: 
        # 價格>均線: 買
        action=1
    elif (currPrice+beta)<ma:
        # 價格<均線: 賣
        action=-1
    else:
        action=0
    return action
