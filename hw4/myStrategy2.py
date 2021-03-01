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

def myStrategy(pastData, currPrice):
    import numpy as np
    param=[8, 21]
    windowSize=100
    alpha=param[0]
    beta=param[1]
    action=0
    ma=0
    rsi=0
    dataLen = len(pastData)
    if dataLen<windowSize:
        #ma=np.mean(pastData)
        ma=np.mean(pastData)
        return 0
    else :
        windowedData=pastData[-windowSize:]
        ma=np.mean(windowedData)
        rsi=RSIcalculator(windowedData)
    if (currPrice-alpha)>ma and (currPrice-alpha)>rsi:
        action=1
    elif (currPrice+beta)<ma and (currPrice-beta)>rsi:
        action=-1
    else:
        action=0
    return action
