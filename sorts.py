__author__ = 'went'

import datetime
import random
import copy

def bubblesort(data):
    l = len(data)
    l1 = l - 1
    for i in range(l1,1,-1):
        for j in range(i):
            if(data[j]>data[j+1]):
                data[j],data[j+1] = data[j+1],data[j]


def selectionsort(data):
    l = len(data)
    l1 = l - 1
    for i in range(l1):
        min,key = data[i],i
        for j in range(i,l):
            if(data[j]<min):
                min,key = data[j],j
        if key<>i:
            data[i],data[key] = data[key],data[i]

def insertsort(data):
    l = len(data)
    l1 = l - 1
    for i in range(l1):
        key = data[i+1]
        j = i
        while j>=0 and key<data[j]:
            data[j],data[j+1] = data[j+1],data[j]
            j -= 1
        data[j+1] = key

def shellsort(data,n=None):
    l = len(data)
    if n==None:
        n = l / 2
    if(n%2==0):
        n = n + 1
    for i in range(n):
        newdata=data[i:l:n]
        insertsort(newdata)
        data[i:l:n] = newdata
    d = n / 2
    if(d>0):
        if(d%2==0):
            d = d + 1
        shellsort(data,d)

def quicksort(data,low=0,high=None):
    l = len(data)
    if(high==None):
        high = l - 1
    if(low<high):
        key, i, j = data[low], low, high
        while(i < j):
            while(i<j and data[j]>key):
                j = j - 1
            if(i<j):
                data[i] = data[j]
                i = i + 1
            while(i<j and data[i]<key):
                i = i + 1
            if(i<j):
                data[j] = data[i]
                j = j - 1
        data[i] = key
        quicksort(data,low,i-1)
        quicksort(data,i+1,high)


data = [random.randint(0,65536) for i in range(50)]
def sortperform(sortFunc):
    newdata = copy.deepcopy(data)
    t1 = datetime.datetime.now()
    sortFunc(newdata)
    t2 = datetime.datetime.now()
    if len(newdata) <= 50:
        print newdata
    print sortFunc.__name__ + ":" + str(t2-t1)

sortperform(bubblesort)
sortperform(selectionsort)
sortperform(insertsort)
sortperform(shellsort)
sortperform(quicksort)