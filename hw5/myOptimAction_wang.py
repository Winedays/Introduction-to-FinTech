import pandas as pd
import numpy as np


def myOptimAction(L, rate):
    rate = 1.0 - rate
    action = np.zeros(len(L))
    table = [np.zeros(len(L)), np.zeros(len(L))]
    trace = [np.zeros(len(L)), np.zeros(len(L))] #紀錄從哪裡來
    back = np.zeros(len(L))  # 紀錄trace回來的結果，方便算action

    
    table[0][0] = rate/L[0]
    table[1][0]= 1.0
    for i in range(1, len(L)):
        # 變成有股票
        a = table[0][i - 1]  
        b = table[1][i - 1] * rate / L[i]

        if a > b:  # 有 ->有
            table[0][i] = a
            trace[0][i] = 0
        else:      #沒有 -> 有
            table[0][i] = b
            trace[0][i] = 1

        #變成沒股票
        a = table[0][i - 1] * rate * L[i]
        b = table[1][i - 1]

        if a > b:  # 有 ->無
            table[1][i] = a
            trace[1][i] = 0
        else:      #沒有 -> 無
            table[1][i] = b
            trace[1][i] = 1
    
    #最後誰比較大
    index=0
    if table[0][len(L)-1] * rate * L[len(L)-1] < table[1][len(L)-1]:
        index = 1
    
    back[len(L)-1] = index
    back[len(L)-2] = trace[index][len(L)-1]
    action[len(L)-1]=back[len(L)-2] - back[len(L)-1]
    for k in range(len(L) - 2, 0, -1):
        back[k-1] = trace[int(back[k])][k]
        action[k] = back[k-1] - back[k]
    
    action[0] = 1-trace[int(back[1])][1]
    # print(trace)
    # print(back)
    return action

# data = pd.read_csv('./SPY.csv')
# l = myOptimAction(data['Adj Close'], 0.01)
# data = [10,1,2,3,4,5,6]
# l = myOptimAction(data, 0.01)
# print(l)
