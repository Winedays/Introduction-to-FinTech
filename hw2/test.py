import pandas as pd
import sys
import numpy as np
fname = sys.argv[1]
df = pd.read_csv(fname, encoding = 'big5')
df = df[(df['商品代號'] == 'TX     ')]
df = df[(df['到期月份(週別)'] == '201909')]
df = df[(df['成交時間'] >= 84500)]
df = df[(df['成交時間'] <= 134500)]
array = df['成交價格']
print(array.tolist())
print(array.iat[1])
first = int(array.iat[0])
print(first)
