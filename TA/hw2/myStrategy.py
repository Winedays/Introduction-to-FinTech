def RSIcalculator( data ) :
    import numpy as np
    diff_list = [ 0 ] 
    for i in range( 1 , len(data) ) :
        diff_list.append( data[i] - data[i-1] )
    # calculate the rsi that data quantity are less than rsi_day
    # sum all upward change
    upward_change = sum( x for x in diff_list if x>=0  )
    rsi = upward_change / np.sum( np.abs( diff_list ) )
    #print( np.array(rsi_list) )
    return rsi
    
def myStrategy(pastData, currPrice, stocksType ):
    import numpy as np
    
    paramSetting = {'SPY': {'alpha':0, 'beta':8, 'windowSize':88},
                    'IAU': {'alpha':0, 'beta':1, 'windowSize':145},
                    'LQD': {'alpha':0, 'beta':1, 'windowSize':14},
                    'DSI': {'alpha':2, 'beta':7, 'windowSize':36}}
    
    windowSize = paramSetting[stocksType]['windowSize']
    alpha = paramSetting[stocksType]['alpha']
    beta = paramSetting[stocksType]['beta']
    
    action=0
    ma=0
    dataLen = len(pastData)
    if dataLen<windowSize:
        #ma=np.mean(pastData)
        return 0
    else :
        windowedData=pastData[-windowSize:]
        ma_l=np.mean(windowedData)
        ma_s=np.mean(windowedData[:5])
        rsi_l=RSIcalculator(windowedData)
        rsi_s=RSIcalculator(windowedData[:5])
    if ma_s>ma_l and (currPrice-alpha)>ma_l and rsi_s>rsi_l and (currPrice-alpha)>rsi_l:
        action=1
    elif ma_s<ma_l and (currPrice+beta)<ma_l and rsi_s<rsi_l and (currPrice-beta)>rsi_l:
        action=-1
    else:
        action=0
    return action
