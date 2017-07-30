# coding:utf-8
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from packetInfo.models import *
from NetInfo import PingAndBandwith,getHttpResponse,getHttpReq,ReTransimission
import threading
import MySQLdb
import time
import os

# Create your views here.
def index(request):
    #return render(request,"index.html")
    return render(request, "QoSInfo.html")

#START 启动抓包分析
def startDetect(request):
    info1 ='0'

    threads = []
    threads.append(threading.Thread(target=PingAndBandwith.getPingAndBandWith))
    threads.append(threading.Thread(target=getHttpReq.httpReq))
    threads.append(threading.Thread(target=getHttpResponse.httpResponse))
    # start
    for t in threads:
        t.start()
     # join
    for t in threads:
        t.join()
    info1 = '1'
    return JsonResponse(info,safe=False)

#启动重传乱序计算
def startCalReTran(request):
    info2 = '0'
    ReTransimission.getReTranRate()
    info1 = '1'
    return JsonResponse(info, safe=False)


#从数据库中获取数据
prebwdCount = 0
presourceCount = 0
prehttpcodeCount = 0
preReTran = 0

#得到流媒体信息
def getInfoSource(request):
    #bwdquery = BandwidthDelay.objects.all()
    sourcequery = Source.objects.all()
    httpcodequery = HTTPCode.objects.all()

    #global prebwdCount
    global presourceCount
    global prehttpcodeCount

    # nowbwdCount = bwdquery.count()
    nowsourceCount = sourcequery.count()
    nowhttpcodeCount = httpcodequery.count()

    # if nowbwdCount == prebwdCount:
    #     bwd = []
    # else:
    #     bwd = list(bwdquery.values()[prebwdCount:nowbwdCount])

    if nowsourceCount == presourceCount:
        source = []
    else:
        source = list(sourcequery.values()[presourceCount:nowsourceCount])

    if nowhttpcodeCount == prehttpcodeCount:
        httpcode = []
    else:
        httpcode = list(httpcodequery.values()[prehttpcodeCount:nowhttpcodeCount])

    #prebwdCount = nowbwdCount
    presourceCount = nowsourceCount
    prehttpcodeCount = nowhttpcodeCount

    # infoMes = {'bdelay':bwd,'source':source,'httpcode':httpcode}
    infoMes = {'source': source, 'httpcode': httpcode}
    # print '=============================================================='
    return JsonResponse(infoMes)

#得到延时数据
def getInfoDelay(request):
    bwdquery = BandwidthDelay.objects.all()
    global prebwdCount
    nowbwdCount = bwdquery.count()
    if nowbwdCount == prebwdCount:
        bwd = []
    else:
        bwd = list(bwdquery.values()[prebwdCount:nowbwdCount])

    prebwdCount = nowbwdCount
    infoMes = {'bdelay': bwd}
    return JsonResponse(infoMes)

#获得重传数据，发给前端
def getReTran(request):
    reTran = ReTran.objects.all()
    global preReTran
    nowReTran = reTran.count()
    if nowReTran == preReTran:
        retranList = []
    else:
        retranList = list(reTran.values()[preReTran:nowReTran])

    preReTran = nowReTran
    infoMes = {'retran': retranList}
    return JsonResponse(infoMes)


#导出数据库中的数据
def outAndDelete(request):
    info = 0;
    conn = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='118925',
        db='zgr',
    )
    infoTime = time.strftime('%y_%m_%d_%H_%M_%S', time.localtime(time.time()))
    cur = conn.cursor()
    sql1 = "SELECT * FROM packetInfo_source INTO OUTFILE '/var/lib/mysql-files/"+infoTime+"packetInfo_source.txt' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';"
    sql2 = "SELECT * FROM packetInfo_bandwidthdelay  INTO OUTFILE '/var/lib/mysql-files/"+infoTime+"packetInfo_bandwidth.txt' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';"
    sql3 = "SELECT * FROM packetInfo_httpcode INTO OUTFILE '/var/lib/mysql-files/"+infoTime+"packetInfo_httpcode.txt' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';"
    sql4 = "SELECT * FROM packetInfo_retran INTO OUTFILE '/var/lib/mysql-files/"+infoTime+"packetInfo_retran.txt' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';"
    cur.execute(sql1)
    cur.execute(sql2)
    cur.execute(sql3)
    cur.execute(sql4)

    os.system("cp /var/lib/mysql-files/"+infoTime+"packetInfo_bandwidth.txt"+" /home/a/project/djangoProInfo/djangoInfo/static_file/data/")

    sql1 = "truncate table packetInfo_source"
    sql2 = "truncate table packetInfo_bandwidthdelay"
    sql3 = "truncate table packetInfo_httpcode"
    sql4 = "truncate table packetInfo_retran"

    cur.execute(sql1)
    cur.execute(sql2)
    cur.execute(sql3)
    cur.execute(sql4)

    cur.close()
    conn.commit()
    conn.close()
    info = 1;
    infoMes = {'out' : info}
    return JsonResponse(infoMes)


#将数据上传至大数据平台
def upToHadoop(request):
    hadoopInfo = 0;
    try:
        os.system('/opt/hadoop-2.7.3/bin/hadoop dfs -put /var/lib/mysql-files/*  hdfs://10.149.252.106:9000/input/netWorkInfo')
        hadoopInfo = 1;
    except e:
        print e
    infoMes = {'out': hadoopInfo}
    return JsonResponse(infoMes)

def deleteHadoop(request):
    hadoopInfo = 0;
    try:
        os.system('/opt/hadoop-2.7.3/bin/hadoop dfs -rm hdfs://10.149.252.106:9000/input/netWorkInfo/*')
        hadoopInfo = 1;
    except e:
        print e
    infoMes = {'out': hadoopInfo}
    return JsonResponse(infoMes)