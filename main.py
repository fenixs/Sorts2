# -*- coding:utf-8 -*-
__author__ = 'went'
import urllib
import json
import os
import datetime

def isChinese(uchar):
    '''判断是不是中文'''
    if uchar>=u'\u4e00' and uchar<= u'\u9fa5':
        return True
    else:
        return False

def myAlign(text,width):
    '''中文的左对齐'''
    stext = str(text)
    utext = stext.decode('utf-8')
    cnCount = 0
    for u in utext:
        if(isChinese(u)):
            cnCount += 1
    return ' ' * (width-cnCount-len(utext)) + stext

#fe:12939|Philip：12881|12569：zzf
def getData(userid,cnt=1000,starttime='2017-01-01 00:00:00',endtime='2099-01-01 00:00:00'):
    '''用户名,数据条数'''
    _userid = userid
    _username=''
    _pancnt=cnt
    _userid2 = str(_userid).encode("utf-8")
    url = 'http://mj.smzy.cc:9368/queryPlayRecord.aspx?user=' + str(_userid) + '&startindex=0&number=' + str(_pancnt)
    response = urllib.urlopen(url)      #获取到response
    html = response.read()              #获取到response的内容文本
    target = json.loads(html)           #获取到内容文本的json对象
    message=target['message']          #获取到message
    datas = json.loads(message)         #将内容转换为list
    if len(datas)>0:            #获取到当前用户名
        if(datas[0]['user_1'] == _userid2):
            _username = datas[0]['showname_1']
        elif(datas[0]['user_2'] == _userid2):
            _username = datas[0]['showname_2']
        elif(datas[0]['user_3'] == _userid2):
            _username = datas[0]['showname_3']
        elif(datas[0]['user_4'] == _userid2):
            _username = datas[0]['showname_4']
    cnt=0   #总局数
    circle=0    #总盘数
    filePath = os.path.dirname(os.path.realpath(__file__))  #当前目录
    filePath = os.path.join(filePath,os.path.pardir)        #上级目录
    filePath = filePath + '\dataresults\data-' + _username + '.txt'  #具体文件
    dataFile = open(filePath,'w')
    scores = {}  #所有人的成绩
    idname = {}  #id和name
    times = {} #对战次数
    myScores = [] #我的成绩
    dataFile.write('id,tableid,roomid,starttime,endtime,pantype,userid1,username1,score1,userid2,username2,score2,userid3,username3,score3,userid4,username4,score4 \n')
    for d in datas:
        user1=(d['user_1']).encode("utf-8")     #获取到用户id
        user2=(d['user_2']).encode("utf-8")
        user3=(d['user_3']).encode("utf-8")
        user4=(d['user_4']).encode("utf-8")
        gc1= int(d['gamecoin_1'])   #用户成绩
        gc2= int(d['gamecoin_2'])
        gc3= int(d['gamecoin_3'])
        gc4= int(d['gamecoin_4'])
        if(user1==_userid2):    #记录自己成绩
            myScores.append(gc1)
        elif(user2==_userid2):
            myScores.append(gc2)
        elif(user3==_userid2):
            myScores.append(gc3)
        elif(user4==_userid2):
            myScores.append(gc4)
        username1 = (d['showname_1']).encode("utf-8")   #各个用户名
        username2 = (d['showname_2']).encode("utf-8")
        username3 = (d['showname_3']).encode("utf-8")
        username4 = (d['showname_4']).encode("utf-8")
        dataFile.write((d['id']).encode("utf-8") + "," + (d['tableid']).encode("utf-8") + "," + (d['roomid']).encode("utf-8") + "," + (d['starttime']).encode("utf-8") + "," + (d['endtime']).encode("utf-8") + "," + (d['pantype']).encode("utf-8") + ","  \
                        + user1 + "," + username1 + "," + str(gc1) + "," + user2 + "," + username2 + "," + str(gc2) + "," \
                        + user3 + "," + username3 + "," + str(gc3) + "," + user4 + "," + username4 + "," + str(gc4) + "\n")
        if(scores.has_key(user1)):  #保存各用户的成绩和次数
            scores[user1] += gc1
            times[user1] +=1
        else:
            scores[user1] = gc1
            times[user1]  =1
        if(scores.has_key(user2)):
            scores[user2] += gc2
            times[user2] +=1
        else:
            scores[user2] = gc2
            times[user2]  =1
        if(scores.has_key(user3)):
            scores[user3] += gc3
            times[user3] +=1
        else:
            scores[user3] = gc3
            times[user3]  =1
        if(scores.has_key(user4)):
            scores[user4] += gc4
            times[user4] +=1
        else:
            scores[user4] = gc4
            times[user4]  =1
        idname.setdefault(user1,username1)
        idname.setdefault(user2,username2)
        idname.setdefault(user3,username3)
        idname.setdefault(user4,username4)
        cnt+=1
        circle += int(d['pantype'])

    dataFile.write('%30s%7s:%s%s\n'%(' ',' ',myAlign('数据',10),myAlign('次数',10)))
    for key in scores:
        dataFile.write('%s(%s):%10s%10s\n'%(myAlign(idname[key],30),key,str(scores[key]),str(times[key])))

    dataFile.write("my scores:" + ','.join(str(s) for s in myScores) + "\n")
    dataFile.write('total count:' + str(cnt) + "  total quan:" + str(circle) + "\n")
    dataFile.close()


def getMultiDatas():
    filePath = os.path.dirname(os.path.realpath(__file__))  #当前目录
    filePath = os.path.join(filePath,os.path.pardir)        #上级目录
    filePath = filePath + '\dataresults\userids.txt'  #具体文件,换行保存
    ids = []
    userFile = open(filePath,'r')
    for line in userFile:
        ids.append(line)
    userFile.close()
    idCnt = len(ids)
    i=0
    if(idCnt>0):
        for uid in ids:
            curId = int(uid)
            getData(curId)
            i+=1
            print('user %s data complete.(%s/%s)'%(curId,i,idCnt))


#fe:12939|Philip：12881|12569：zzf
getData(12794)
# getMultiDatas()









