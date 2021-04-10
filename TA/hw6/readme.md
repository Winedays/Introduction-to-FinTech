###### tags: `fintech`
# HW6
https://docs.google.com/spreadsheets/d/1GPR6WQAwB9f6VyiEyCW3XHKVDJFMk-KgONAwKOgTPTE/edit?usp=sharing  
Q{1-3}_x : x坐標  
Q{1-3}_y : y坐標  
Q{1-3}_x_hex : x坐標(16進位)  
Q{1-3}_y_hex : y坐標(16進位)  
Q4_Total_step : 總運算次數  
Q4_double_step : Double次數  
Q4_add_step	: Add次數  
Q4_bin : d的二進位  
Q5_Total_step : 總運算次數  
Q5_double_step : Double次數  
Q5_add_step : Add次數  
Q5_inv_add_step : Inverse Add次數  
Q5_inv_bin : d的二進位轉換，Double & Add結果  

## 分工
傳祐：第1-4頁  
政鷹：第5-8頁  
智顥：第9-12頁  


## 其他標準
* 遲交 : 扣5分
* 檔案格式錯 : 扣5分
* 沒有寫自己的d : 扣5分
* 交錯作業 : 0分，之後補交最高70分

## 配分
* Q1 : 10分
* Q2 : 10分
* Q3 : 10分
* Q4 : 15分
* Q5 : 15分
* Q6 : 20分
* Q7 : 20分
* Total : 100分

## Q1
* 10分
* 只看答案
* x,y坐標各5分

## Q2
* 10分
* 只看答案
* x,y坐標各5分

## Q3
* 10分
* 只看答案
* x,y坐標各5分

## Q4
* 15分
* 看Total step，若有分別寫到dobule & add step則也都要對
* Double & add step錯： 扣5分
* d轉2進位轉錯：0分
* 只給答案：5分
* 說明不足：10分

## Q5
* 15分
* 看Total step，若有分別寫到dobule & add ( & inverse ) step則也都要對
* **有機會可以 loop 做優化，但作業沒要求所以做一次就好，參考答案也只有做一次，假如 total stap 比較少要看一下他的答案是不是做了多次優化。**
* 細項Step視情況誤差+-4，但Dobule應該不會比我的多
* Double & add ( & inverse ) step錯：扣5分
* 次數有減少但不是最佳解：5分
* d轉2進位轉錯：0分
* 只給答案：5分
* 說明不足：10分


## Q6
* 20分
* d = 學號後6碼 
* k^-1 是 k mod n 的反元素，不是1/k
* 沒有code：0分
* d完全不是自己學號，是別人學號：0分 -> 很明顯就是抄別人code
* d跟學號只差1個數字：最多給15分 -> 應該就手殘
* code只給一點，不完整：最多給10分
* 抄Github：只給10分
* 套件一句解：20分
* 有k & k^-1正確： 5分
* 算出x_1 & y_1： 5分
* r算式正確 ： 5分
* s算式正確 ： 5分  
![](https://i.imgur.com/qdZPwwX.png)

## Q7
* 20分
* pubile key = Q = dG = Q3答案
* w 是 s mod n 的反元素，不是1/s
* 沒有code：0分
* 若第六題d完全不是自己學號，是別人學號：0分 -> 很明顯就是抄別人code
* code只給一點，不完整：最多給10分
* pubile key(dG)錯：最多給15分 (Q3錯/Q6的d錯)
* 抄Github：只給10分
* 套件一句解：20分
* w算式正確： 5分 
* 算出 u_1 & u_2： 5分 
* 算出 x_1 & y_1： 5分
* 驗算 r == x_1： 5分  
![](https://i.imgur.com/Uez0GdU.png)

## Q6-7 Sage相關語法
* secp256k1   
    1.
    ![](https://i.imgur.com/KV0usM1.png)  
    2.
    ![](https://i.imgur.com/D3hrSpb.png)

* Mod function / inverse mod. function  
    * IntegerModRing(n)  
    * 1 / IntegerModRing(n)  
    ![](https://i.imgur.com/O0UdUuu.png)  
    * FiniteField(n)  
    * 1 / FiniteField(n)  
    ![](https://i.imgur.com/9SWZbMO.png)  
    * GF(n)  
    * 1 / GF(n)  
    ![](https://i.imgur.com/ElDA8SH.png)  
    * n / n.inverse_mod()  
    ![](https://i.imgur.com/0mFodI7.png)  
    * FiniteField(n).random_element()  
    ![](https://i.imgur.com/ovBdxue.png)  
    * Integer(n)  
    * 1 / Integer(n)  
    ![](https://i.imgur.com/gGZ6uze.png)  




# sample
1. Q6-7沒有載圖定義橢圓曲線G的code -> 算了給過  
![](https://i.imgur.com/fGzIPAF.png)  
2. Q6-7把前一句print的結果寫死在code裡 -> 算了給過  
![](https://i.imgur.com/D20xolx.png)  
3. Q6-7截圖code沒有d，但作業一開始有寫 -> 給過  
![](https://i.imgur.com/BUQf69S.png)  
4. Q6-7截圖code只給一點，不完整 -> 最多給10分  
![](https://i.imgur.com/NWN6KqA.png)  
5. Q1-3沒有分別寫x,y坐標 -> 0分，別麻煩自己  
![](https://i.imgur.com/DGwp0HJ.png)  
6. Q4-5步驟寫一半 -> 給過  
![](https://i.imgur.com/3wIrWXJ.png)  



# Github
https://github.com/TheBlueMatt/bitcoinninja/blob/master/secp256k1.ecdsa.sage?fbclid=IwAR3o79aPnnlCPG3PjVyR9BAMfiJ63dqANgjolrd2_J8kPfIj9glRPFiLDxY  
![](https://i.imgur.com/YoCBXnU.png)

# ?
![](https://i.imgur.com/VTMo0lk.png)


# 陳*華
![](https://i.imgur.com/p75VThp.png)
![](https://i.imgur.com/DzVCNv3.png)
