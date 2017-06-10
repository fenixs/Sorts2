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

def getRank(gc1,gc2,gc3,gc4,myScore):
    '''从四个数据中返回名次'''
    all = [gc1,gc2,gc3,gc4]
    all.sort()
    all.reverse()
    return str(all.index(myScore) + 1)

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
    mySumScores = [] #我的累计成绩
    myScoresVsOther = {}   #面对其他人时候的我的成绩
    myRanks = {'1':0,'2':0,'3':0,'4':0}
    isUseDate = False
    st = datetime.datetime.now()
    et = datetime.datetime.now()
    if starttime!='2017-01-01 00:00:00' or endtime!='2099-01-01 00:00:00':
        isUseDate = True
        st = datetime.datetime.strptime(starttime,'%y-%m-%d h:m:s')
        et = datetime.datetime.strptime(endtime,'%y-%m-%d h:m:s')

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
        myScore = 0
        if(user1==_userid2):    #记录自己成绩
            myScore = gc1
        elif(user2==_userid2):
            myScore = gc2
        elif(user3==_userid2):
            myScore = gc3
        elif(user4==_userid2):
            myScore = gc4
        myScores.append(myScore)
        myRanks[getRank(gc1,gc2,gc3,gc4,myScore)] += 1
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
            myScoresVsOther[user1] += myScore
        else:
            scores[user1] = gc1
            times[user1]  =1
            myScoresVsOther[user1] = myScore
        if(scores.has_key(user2)):
            scores[user2] += gc2
            times[user2] +=1
            myScoresVsOther[user2] += myScore
        else:
            scores[user2] = gc2
            times[user2]  =1
            myScoresVsOther[user2] = myScore
        if(scores.has_key(user3)):
            scores[user3] += gc3
            times[user3] +=1
            myScoresVsOther[user3] += myScore
        else:
            scores[user3] = gc3
            times[user3]  =1
            myScoresVsOther[user3] = myScore
        if(scores.has_key(user4)):
            scores[user4] += gc4
            times[user4] +=1
            myScoresVsOther[user4] += myScore
        else:
            scores[user4] = gc4
            times[user4]  =1
            myScoresVsOther[user4] = myScore
        idname.setdefault(user1,username1)
        idname.setdefault(user2,username2)
        idname.setdefault(user3,username3)
        idname.setdefault(user4,username4)
        cnt+=1
        circle += int(d['pantype'])

    myScores.reverse()
    #计算累计成绩
    lastAllScore = 0
    for score in myScores:
        lastAllScore += score
        mySumScores.append(lastAllScore)


    dataFile.write('%30s%7s:%s%s%s\n'%(' ',' ',myAlign('数据',10),myAlign('次数',10),myAlign('我的数据',10)))
    for key in scores:
        dataFile.write('%s(%s):%10s%10s%10s\n'%(myAlign(idname[key],30),key,str(scores[key]),str(times[key]),str(myScoresVsOther[key])))

    dataFile.write("\nmy scores:" + ','.join(str(s) for s in myScores) + "\n")
    dataFile.write("\nmy sum scores:" + ','.join(str(s) for s in mySumScores) + "\n")
    # for s in mySumScores:
    #     dataFile.write(str(s) + "\n")
    dataFile.write("\nmy rank: 1st: %s,2nd: %s,3rd: %s,4th: %s \n"%(str(myRanks['1']),str(myRanks['2']),str(myRanks['3']),str(myRanks['4'])))
    dataFile.write('\ntotal count:' + str(cnt) + "  total quan:" + str(circle) + "\n")
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


#fe:12939|Philip：12881|12569：zzf|atubo:12906|天外:12883|yyk:12792|西湖:12900|lsj:12824|老庄:12621
getData(12621)
# getMultiDatas()










