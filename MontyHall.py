# -*- coding: cp936 -*-
__author__ = 'went'
import random

cs = 30000
js = 0
for i in xrange(0,cs):
    qc = random.randint(1,3)  #�������ĸ��ź���
    wj = random.randint(1,3)  #���ÿ��ѡ�����
    if qc==wj:      #��ҵ�һ��ѡ����ȷ
        zcr = random.choice(list(set([1,2,3])-set([wj])))   #��������ʣ�µĿ�������ѡ��һ��
        wj2 = list(set([1,2,3]) - set([wj]) - set([zcr]))[0]    #��һ���
    else:
        zcr = list(set([1,2,3]) - set([wj]) - set([qc]))[0]     #������ֻ��һ��ѡ��
        wj2 = list(set([1,2,3]) - set([wj]) - set([zcr]))[0]
    if wj2==qc:
        js = js + 1
print js
#print("ʵ��%d�Σ�������ţ���ҵڶ���ѡ�д���Ϊd%" %(cs,js))
