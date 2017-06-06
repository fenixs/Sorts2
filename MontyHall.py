# -*- coding: cp936 -*-
__author__ = 'went'
import random

cs = 30000
js = 0
for i in xrange(0,cs):
    qc = random.randint(1,3)  #汽车在哪个门后面
    wj = random.randint(1,3)  #玩家每次选择的门
    if qc==wj:      #玩家第一次选择正确
        zcr = random.choice(list(set([1,2,3])-set([wj])))   #主持人在剩下的空门里面选择一个
        wj2 = list(set([1,2,3]) - set([wj]) - set([zcr]))[0]    #玩家换门
    else:
        zcr = list(set([1,2,3]) - set([wj]) - set([qc]))[0]     #主持人只有一个选项
        wj2 = list(set([1,2,3]) - set([wj]) - set([zcr]))[0]
    if wj2==qc:
        js = js + 1
print js
#print("实验%d次，如果换门，玩家第二次选中次数为d%" %(cs,js))
