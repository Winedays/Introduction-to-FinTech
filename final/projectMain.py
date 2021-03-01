import sys
import numpy as np
import pandas as pd
from myStrategy import myStrategy

#def myStrategy(dailyOhlcvFile , minutelyOhlcvFile , openPricev ):
#    from keras.layers import Input, Dense
#    from keras.models import Model , Sequential
#    #print('dailyOhlcvFile : ' , dailyOhlcvFile)
##    print('minutelyOhlcvFile : ' , minutelyOhlcvFile)
##    print('openPricev : ' , openPricev)
#    import random 
#    
#    dailyOhlcvFile = dailyOhlcvFile[['open','high','low','close','volume']].values
#    
#    look_day = 15
#    X = []
#    Y = []
#    for i in range( len(dailyOhlcvFile)-look_day ) :
#        x = []
#        daily = dailyOhlcvFile[i:i+look_day]
#        y = dailyOhlcvFile[i+look_day][-1]
#        for j in range( look_day ) :
#            for k in range( 5 ) :
#                x.append( daily[j][k] )
#        X.append( x )
#        Y.append( [y] )
#    
#    z = list( zip(X , Y) )
#    random.Random(4).shuffle( z )
#    X , Y = zip(*z)
#    
#    test_size = len(X) - int(len(X)*0.2)
#    X_train, Y_train = X[:test_size], Y[:test_size]     # train 前 160 data points
#    X_test, Y_test = X[test_size:], Y[test_size:]       # test 后 40 data points
#    
#    X_train = np.array( X_train )
#    X_test = np.array( X_test )
#    Y_train = np.array( Y_train )
#    Y_test = np.array( Y_test )
#    print('X : ' , X_train )
#    print('Y : ' , Y_train )
#    
#    #train(X_train,Y_train)
#    #print('dailyOhlcvFile : ' , dailyOhlcvFile[-15:])
#    
##    inputs = Input(shape=(1,))
##    preds = Dense(1,activation='linear')(inputs)
#    
#    
#    
#    model = Sequential()
#    model.add(Dense(input_dim=1, activation="linear", units=1))
#    model.compile(loss='mse', optimizer='sgd')
#    model.fit(X,Y, batch_size=1, epochs=30, shuffle=False)
#            
#    return 1 

dailyOhlcv = pd.read_csv('./ohlcv_daily.csv')
minutelyOhlcv = pd.read_csv('./ohlcv_minutely.csv')
evalDays = 1
action = np.zeros((evalDays,1))
openPricev = dailyOhlcv["open"].tail(evalDays).values
for ic in range(evalDays,0,-1):
    dailyOhlcvFile = dailyOhlcv.head(len(dailyOhlcv)-ic)
    dateStr = dailyOhlcvFile.iloc[-1,0]
    minutelyOhlcvFile = minutelyOhlcv.head((np.where(minutelyOhlcv.iloc[:,0].str.split(expand=True)[0].values==dateStr))[0].max()+1)
    action[evalDays-ic] = myStrategy(dailyOhlcvFile,minutelyOhlcvFile,openPricev[evalDays-ic])
    print('action : ' , action)
