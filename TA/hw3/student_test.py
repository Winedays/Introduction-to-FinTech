import numpy as np
import operator
 
def myOptimAction(priceMat, transFeeRate):
    # Explanation of my approach:
    # 1. Technical indicator used: Watch next day price
    # 2. if increase for 2 consecutive days ==> buy
    #       * buy the best stock
    #    if decrease for 2 consecutive days ==> sell
    #       * sell if you are holding stock
    # 3. You should sell before buy to get cash each day
    # default
    cash = 1000
    consec_decrease=2 
    consec_increase=2
    date=max(consec_decrease,consec_increase)
    # user definition
 
 
    dataLen, stockCount = priceMat.shape  # day size & stock count 
    stockHolding = np.zeros((dataLen,stockCount))  # Mat of stock holdings
    actionMat = []  # An k-by-4 action matrix which holds k transaction records.
 
    for day in range( 0, dataLen-date ) :
        if day > 0:
            stockHolding[day] = stockHolding[day-1]  # The stock holding from the previous action day
 
        buyStock = -1  # which stock should buy. No action when is -1
        buyPrice = 0  # use how much cash to buy
        sellStock = []  # which stock should sell. No action when is null
        sellPrice = []  # get how much cash from sell
        bestPriceDiff = 0  # difference in today price & next day price of "buy" stock
        stockCurrentPrice = 0  # The current price of "buy" stock
 
        # sell
        for stock in range(0,stockCount) :
              # stock price 
            stock_prices=[]
            for date in range(0,consec_decrease+1):
                stock_prices.append(priceMat[day+date][stock])
            holding = stockHolding[day][stock]
            if holding > 0 :  # "sell"
                #to tell whether its strict decrease, so that its good time to sell
                strict_decrease=True
                for x in range(1,consec_decrease+1):
                    '''current value is more than previous days, 
                    if it is then its certainly is not gonna be strict increase'''
                    if(stock_prices[x] > stock_prices[x-1]*(1+transFeeRate)):
                        strict_decrease=False
                        break
                if strict_decrease:
                    sellStock.append(stock)
                    sellPrice.append(holding * priceMat[day][stock])
                    cash = holding * priceMat[day][stock] * (1-transFeeRate) # Sell stock to have cash
                    stockHolding[day][sellStock] = 0
        #buy
 
        if cash > 0 :  # "buy" only when you have cash
            for stock in range(0,stockCount) :
                strict_increase=True
                '''
                insert the prices into the list'''
                stock_prices=[]
                for date in range(0,consec_increase+1):
                    stock_prices.append(priceMat[day+date][stock])
                    #to tell whether its strict increase so that its high time to buy
                    '''if previous day is more than current day then it is not possible to be strict increase'''
                for x in range(1,consec_increase+1):
                    if(stock_prices[x] < stock_prices[x-1]*(1+transFeeRate)):
                        strict_increase=False
                        break
                    '''if strict increase and the last day of the window is more valuable 
                    than that of the current time then go buy and replace the best buy option'''
                    if strict_increase:
                        diff = priceMat[day+consec_increase][stock] - priceMat[day][stock]*(1+transFeeRate)
                        if diff > bestPriceDiff :  # this stock is better
                            bestPriceDiff = diff
                            buyStock = stock
                            stockCurrentPrice = priceMat[day][stock]
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
    print(2)
    return actionMat