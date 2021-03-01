def RSIcalculator( data ) :
    import numpy as np
    diff_list = [ 0 ] 
    if len(diff_list) <= 1 :
        return 0
    upward_change = 0
    for i in range( 1 , len(data) ) :
        diff_list.append( data[i] - data[i-1] )
        if data[i] - data[i-1] > 0 :
            upward_change += data[i] - data[i-1]
    # calculate the rsi that data quantity are less than rsi_day
    # sum all upward change
    # upward_change = sum( x for x in diff_list if x>=0  )
    rsi = upward_change / np.sum( np.abs( diff_list ) )
    #print( np.array(rsi_list) )
    return rsi
    
def myStrategy(pastData, currPrice, windowSize, alpha, beta ):
    import numpy as np

    action=0
    ma=0
    dataLen = len(pastData)
    if dataLen == 0 :
        return 0 ;
    elif dataLen<windowSize:
        # ma=np.mean(pastData)
        return 0
    else :
        windowedData=pastData[-windowSize:]
        ma_l=np.mean(windowedData)
        ma_s=np.mean(windowedData[:5])
        rsi_l=RSIcalculator(windowedData)
        rsi_s=RSIcalculator(windowedData[:5])
    # if ma_s>ma_l and (currPrice-alpha)>ma_l and rsi_s>rsi_l and (currPrice-alpha)>rsi_l:
        # action=1
    # elif ma_s<ma_l and (currPrice+beta)<ma_l and rsi_s<rsi_l and (currPrice-beta)>rsi_l:
        # action=-1
    if rsi_s>=rsi_l and (currPrice-alpha)>rsi_l:
        action=1
    elif rsi_s<=rsi_l and (currPrice-beta)>rsi_l:
        action=-1
    else:
        action=0
    return action
