# 7.2933
def myStrategy(pastData, currPrice, stockType):
    import numpy as np

    paramSetting = {'SPY': {'alpha':4, 'beta':7, 'windowSize':6},
                    'IAU': {'alpha':0, 'beta':0, 'windowSize':9},
                    'LQD': {'alpha':0, 'beta':1, 'windowSize':15},
                    'DSI': {'alpha':2, 'beta':8, 'windowSize':18}}
                
    windowSize = paramSetting[stockType]['windowSize']
    alpha = paramSetting[stockType]['alpha']
    beta = paramSetting[stockType]['beta']
    
    action = 0  # action : 1(buy), -1(sell), 0(hold)
    dataLen = len(pastData) # 資料天數
    ma = 0 ; ma_s = 0 ;
    if dataLen == 0 : 
        return 0
    elif dataLen<windowSize:    
        #當資料天數<windowSize, 以資料天數計算ma
        ma=np.mean(pastData)
        ma_s = np.mean(pastData[:5])
    else :
        # 向前看windowSize天數的資料, 算ma
        windowedData=pastData[-windowSize:] 
        ma=np.mean(windowedData)
        ma_s = np.mean(windowedData[:5])
    if ma_s>=ma and (currPrice-alpha)>ma : 
        # 價格>均線: 買
        action=1
    elif ma_s<=ma and (currPrice+beta)<ma :
        # 價格<均線: 賣
        action=-1
    else:
        action=0
    return action

