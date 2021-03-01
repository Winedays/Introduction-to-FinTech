import sys
import numpy as np
import pandas as pd

def myOptimAction(priceMat, transFeeRate,day1,day2):
    # Explanation of my approach:
	# 1. Technical indicator used: Watch next day price
	# 2. if next day price > today price + transFee ==> buy
    #       * buy the best stock
	#    if next day price < today price + transFee ==> sell
    #       * sell if you are holding stock
    # 3. You should sell before buy to get cash each day
    # default
    cash = 1000
    hold = 0
    # user definition
    buyDay = day1
    sellDay = day2
    dataLen, stockCount = priceMat.shape  # day size & stock count   
    stockHolding = np.zeros((dataLen,stockCount))  # Mat of stock holdings
    actionMat = []  # An k×4 action matrix which holds k transaction records.
    
    bigDay = sellDay if sellDay > buyDay else buyDay
    
    for day in range( 0, dataLen-bigDay ) :
        dayPrices = priceMat[day]  # Today price of each stock
        nextBuyDayPrices = priceMat[ day + buyDay ]  # Next day price of each stock
        nextSellDayPrices = priceMat[ day + sellDay ]  # Next day price of each stock
        
        if day > 0:
            stockHolding[day] = stockHolding[day-1]  # The stock holding from the previous action day
        
        buyStock = -1  # which stock should buy. No action when is -1
        buyPrice = 0  # use how much cash to buy
        sellStock = []  # which stock should sell. No action when is null
        sellPrice = []  # get how much cash from sell
        bestPriceDiff = 0  # difference in today price & next day price of "buy" stock
        stockCurrentPrice = 0  # The current price of "buy" stock
        
        # Check next day price to "sell"
        for stock in range(stockCount) :
            todayPrice = dayPrices[stock]  # Today price
            nextDayPrice = nextSellDayPrices[stock]  # Next day price
            holding = stockHolding[day][stock]  # how much stock you are holding
            
            if holding > 0 :  # "sell" only when you have stock holding
                if nextDayPrice < todayPrice*(1+transFeeRate) :  # next day price < today price, should "sell"
                    sellStock.append(stock)
                    # "Sell"
                    sellPrice.append(holding * todayPrice)
                    cash = holding * todayPrice*(1-transFeeRate) # Sell stock to have cash
                    stockHolding[day][sellStock] = 0
        
        # Check next day price to "buy"
        if cash > 0 :  # "buy" only when you have cash
            for stock in range(stockCount) :
                todayPrice = dayPrices[stock]  # Today price
                nextDayPrice = nextBuyDayPrices[stock]  # Next day price
                
                if nextDayPrice > todayPrice*(1+transFeeRate) :  # next day price > today price, should "buy"
                    diff = (nextDayPrice - todayPrice*(1+transFeeRate)) / todayPrice
                    if diff > bestPriceDiff :  # this stock is better
                        bestPriceDiff = diff
                        buyStock = stock
                        stockCurrentPrice = todayPrice
            # "Buy" the best stock
            if buyStock >= 0 :
                buyPrice = cash
                stockHolding[day][buyStock] = cash*(1-transFeeRate) / stockCurrentPrice # Buy stock using cash
                cash = 0
                
        # Save your action this day
        if buyStock >= 0 or len(sellStock) > 0 :
            action = []
            if len(sellStock) > 0 :
                for i in range( len(sellStock) ) :
                    action = [day, sellStock[i], -1, sellPrice[i]]
                    actionMat.append( action )
            if buyStock >= 0 :
                action = [day, -1, buyStock, buyPrice]
                actionMat.append( action )
    return actionMat

    

# Compute return rate over a given price Matrix & action Matrix
def computeReturnRate(priceMat, transFeeRate, actionMat):
    capital = 1000    # Initial available capital
    capitalOrig = capital     # original capital
    stockCount = len(priceMat[0])   # stack size
    suggestedAction = actionMat    # Mat of suggested actions
    actionCount = len(suggestedAction)
    
    stockHolding = np.zeros((actionCount,stockCount))   # Mat of stock holdings
    realAction = np.zeros((actionCount,1))    # Real action, which might be different from suggested action. For instance, when the suggested action is 1 (buy) but you don't have any capital, then the real action is 0 (hold, or do nothing). 
    preDay = 0  # previous action day
    
    # Run through each action, should order by day
    for i in range(actionCount):
        actionVec = actionMat[ i ]
        day = actionVec[0] # The index of day
        a = actionVec[1] # The index of "from" stock
        b = actionVec[2] # The index of "to" stock
        z = actionVec[3] # The equivalent cash for such transaction.
        currentPriceVec = priceMat[day]  # current priceVec
        
        # check action day and equivalent cash
        if day >= preDay and day >= 0 and z > 0 :
            # get real action by suggested action
            if i > 0:
                stockHolding[i] = stockHolding[i-1]  # The stock holding from the previous action day
                preDay = day  # previous action day
            
            if a == -1 and b >= 0 and capital > 0 :  # Suggested action is "buy"
                currentPrice = currentPriceVec[b]  # The current price of stock
                if capital < z :  # "buy" allonly if you don't have enough capital
                    z = capital
                stockHolding[i][b] += z*(1-transFeeRate) / currentPrice # Buy stock using cash
                capital = capital - z  # Cash
                realAction[i] = 1
            elif b == -1 and a >= 0 and stockHolding[i][a] > 0 :  # Suggested action is "sell"
                currentPrice = currentPriceVec[a]  # The current price of stock
                sellStock = z / currentPrice
                if stockHolding[i][a] < sellStock :  # "sell" all only if you don't have enough stock holding
                    sellStock = stockHolding[i][a]
                getCash = sellStock * currentPrice*(1-transFeeRate)  # Sell stock to have cash
                capital = capital + getCash  # get cash from sell stock
                stockHolding[i][a] -= sellStock  # Stocking holding
                realAction[i] = -1
            elif a >= 0 and b >= 0 and stockHolding[i][a] > 0 :  # Suggested action is "buy" and "sell"
                currentPriceSell = currentPriceVec[a]  # The current price of sell stock
                currentPriceBuy = currentPriceVec[b]  # The current price of buy stock
                sellStock = z / currentPriceSell
                if stockHolding[i][a] < sellStock :  # "sell" all only if you don't have enough stock holding
                    sellStock = stockHolding[i][a]
                getCash = sellStock * currentPriceSell*(1-transFeeRate)  # Sell stock to have cash
                stockHolding[i][a] -= sellStock  # Stocking holding
                stockHolding[i][b] += getCash*(1-transFeeRate) / currentPriceBuy # Buy stock using cash
                realAction[i] = 2
            else:
                print( actionVec , stockHolding[i] )
                assert False
        else:
            print( actionVec )
            assert False
            
    # calculate total cash you get at last day
    total = capital
    for stock in range(stockCount) :
        currentPriceVec = priceMat[ actionMat[-1][0] ]
        total += stockHolding[-1][stock] * currentPriceVec[stock]*(1-transFeeRate)  # Total asset, including stock holding and cash 
    # print( total )
    returnRate=(total-capitalOrig)/capitalOrig  # Return rate of this run
    return returnRate
    
if __name__ == "__main__":
    file = sys.argv[1]    # input file
    df = pd.read_csv(file, delimiter=' ')
    transFeeRate= float(sys.argv[2])    # Rate for transaction fee
    # nextDay= int(sys.argv[3])    # Rate for transaction fee
    priceMat = df.values    # Get price as the m×n matrix which holds n stocks' price over m days
    
    bestRR = 0
    day = 0 ; day2 = 0
    for i in range( 1, 50 ) :
        for j in range( 1, 50 ) :
            actionMat = myOptimAction(priceMat, transFeeRate, i, j)  # Obtain the suggested action
            if not actionMat :
                continue ;
            returnRate = computeReturnRate(priceMat, transFeeRate, actionMat)  # Compute return rate
            # f = open( "action.txt" , 'w' )
            # f.write( ','.join(actionVec.astype(str).tolist()) )
            # f.close()
            # print( 'returnRate : ' + str(returnRate) )
            if returnRate > bestRR :
                print( 'returnRate : ' + str(returnRate) )
                bestRR = returnRate
                day = i
                day2 = j
    print( "Best Day :" , day, day2, "RR :" , bestRR )