def myOptimAction(priceVec, transFeeRate,conCount_up,conCount_down, x_up, x_down):
	import numpy as np
	import operator
	dataLen = len(priceVec)
	actionVec = np.zeros(dataLen)
#	conCount_up = 3
#	conCount_down = 3
	conCount_max = 0
	if conCount_down >conCount_up :
		conCount_max = conCount_down 
	else :
		conCount_max = conCount_up
	for ic in range(dataLen):
		if ic + conCount_max + 5 > dataLen:
			continue
		up_1 = map(operator.sub,priceVec[ic+1:ic+1+conCount_up], priceVec[ic:ic+conCount_up])
		down_1 = map(operator.sub,priceVec[ic+1:ic+1+conCount_down], priceVec[ic:ic+conCount_down])
		if all(x > x_up for x in list(up_1)):
			actionVec[ic] = 1
		if all(x < x_down for x in list(down_1)):
			actionVec[ic] = -1
	prevAction = -1
	for ic in range(dataLen):
		if actionVec[ic] == prevAction:
			actionVec[ic] = 0
		elif actionVec[ic] == -prevAction:
			prevAction = actionVec[ic]
	return actionVec