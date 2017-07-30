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
import ConfigParser
import pyhdfs
# Create your views here.
def index(request):
    #return render(request,"index.html")
    return render(request, "QoSInfo.html")

#START 启动抓包分析
# def startDetect(request):
#     info1 ='0'
#
#     threads = []
#     threads.append(threading.Thread(target=PingAndBandwith.getPingAndBandWith))
#     threads.append(threading.Thread(target=getHttpReq.httpReq))
#     threads.append(threading.Thread(target=getHttpResponse.httpResponse))
#     # start
#     for t in threads:
#         t.start()
#      # join
#     for t in threads:
#         t.join()
#     info1 = '1'
#     return JsonResponse(info,safe=False)
#
# #启动重传乱序计算
# def startCalReTran(request):
#     info2 = '0'
#     ReTransimission.getReTranRate()
#     info1 = '1'
#     return JsonResponse(info, safe=False)


#从数据库中获取数据
prebwdCount = 0
presourceCount = 0
prehttpcodeCount = 0
preReTran = 0
config = ConfigParser.ConfigParser()
config.readfp(open("/home/a/project/djangoProInfo/djangoInfo/static_file/config/config.ini","rb"))
clientIP = config.get("clinetIP","ip")
clients = clientIP.split(',')
ipDict = {}
for i in range(len(clients)):
    ipDict[clients[i]] = [0,0,0,0]
# ipDict = {'- please select clinet ip-':[0,0,0,0],'192.168.1.2':[0,0,0,0],'192.168.1.3':[0,0,0,0],'192.168.1.5':[0,0,0,0]}
#得到流媒体信息
def getInfoSource(request):
    if request.method == 'GET':
        selectIp = request.GET.get("selectIp")
        if (selectIp == '- please select clinet ip-'):
            sourcequery = Source.objects.all()
            httpcodequery = HTTPCode.objects.all()
        #bwdquery = BandwidthDelay.objects.all()
        else:
            sourcequery = Source.objects.all().filter(ipPlay__contains=selectIp)
            httpcodequery = HTTPCode.objects.all().filter(ipPlay__contains=selectIp)

        #global prebwdCount
        # global presourceCount
        # global prehttpcodeCount

        nowsourceCount = sourcequery.count()
        nowhttpcodeCount = httpcodequery.count()

        if nowsourceCount == ipDict[selectIp][1]:
            source = []
        else:
            source = list(sourcequery.values()[ipDict[selectIp][1]:nowsourceCount])

        if nowhttpcodeCount == ipDict[selectIp][2]:
            httpcode = []
        else:
            #responseTIme = list(httpcodequery.values('responseTIme').distinct()[ipDict[selectIp][2]:nowhttpcodeCount])#get unique time
            old_httpcode = list(httpcodequery.values('httpCode','responseTIme','ipPlay')[ipDict[selectIp][2]:nowhttpcodeCount])
            # httpcodeRaw = list(httpcodequery.values()[ipDict[selectIp][2]:nowhttpcodeCount])
            # httpcode = []
            # for i in range(len(httpcodeRaw)-1):
            #     if httpcodeRaw[i]['responseTIme'] == httpcodeRaw[i+1]['responseTIme']:
            #         continue;
            #     else:
            #         httpcode.append(httpcodeRaw[i])
            # httpcode.append(httpcodeRaw[len(httpcodeRaw)-1])
            httpcode = []
            for x in old_httpcode:
                if x not in httpcode:
                    httpcode.append(x)

        #prebwdCount = nowbwdCount
        ipDict[selectIp][1] = nowsourceCount
        ipDict[selectIp][2] = nowhttpcodeCount

        # infoMes = {'bdelay':bwd,'source':source,'httpcode':httpcode}
        infoMes = {'source': source, 'httpcode': httpcode}
        # print '=============================================================='
        return JsonResponse(infoMes)

#得到延时数据
def getInfoDelay(request):
    if request.method == 'GET':
        selectIp = request.GET.get("selectIp")
        if (selectIp == '- please select clinet ip-'):
            bwdquery = BandwidthDelay.objects.all()
        else:
            bwdquery = BandwidthDelay.objects.all().filter(ipPlay__contains=selectIp).order_by('bdTIme');
        #global prebwdCount
        nowbwdCount = bwdquery.count()
        if nowbwdCount == ipDict[selectIp][0]:
            bwd = []
        else:
            bwd = list(bwdquery.values()[ipDict[selectIp][0]:nowbwdCount])

        #prebwdCount = nowbwdCount
        ipDict[selectIp][0] = nowbwdCount
        infoMes = {'bdelay': bwd}
        return JsonResponse(infoMes)

#获得重传数据，发给前端
def getReTran(request):
    if request.method == 'GET':
        selectIp = request.GET.get("selectIp")
        if(selectIp == '- please select clinet ip-'):
            reTran = ReTran.objects.all()
        else:
            reTran = ReTran.objects.all().filter(ipPlay__contains=selectIp).order_by('reTranTIme')
        #global preReTran
        nowReTran = reTran.count()
        if nowReTran == ipDict[selectIp][3]:
            retranList = []
        else:
            retranList = list(reTran.values()[ipDict[selectIp][3]:nowReTran])

        ipDict[selectIp][3] = nowReTran
        infoMes = {'retran': retranList}
        return JsonResponse(infoMes)

# 视频信息 分辨率 帧率
def getVideoInfo(request):
    # if request.method == 'GET':
    #     selectIp = request.GET.get("selectIp")ip__contains=selectIp
        videoInfo = PlayRecord.objects.all()
        if len(videoInfo) == 0:
            videoInfo = []
        else:
            videoInfo = list(videoInfo.values('filename','width','height','framerate','ip'))[-1:]
        infoMes = {'videoinfo': videoInfo}
        return JsonResponse(infoMes)

#视频质量信息
def getVideoQuqlity(request):
    # if request.method == 'GET':
    #     selectIp = request.GET.get("selectIp")
        psnrInfo = VideoQuality.objects.all().filter()
        psnrValue = []
        if len(psnrInfo) == 0:
            psnrInfo = []
        # else :
        #     psnrInfo = list(psnrInfo.values('psnr', 'filename'))
        elif len(psnrInfo) >= 2:
            psnrInfo = list(psnrInfo.values('psnr','filename'))[-2:]
            # psnrInfoint = int(psnrInfo[0].psnr)
            # if psnrInfoint > 27:
            #     psnrValue.append('bad')
            # elif psnrInfoint < 15:
            #     psnrValue.append('good')
            # else:
            #     psnrValue.append('general')
        else:
            psnrInfo = list(psnrInfo.values('psnr','filename'))[-1:]
            #psnrInfo['psnr'] = 11
        infoMes = {'psnrinfo': psnrInfo,'pppp':10}
        return JsonResponse(infoMes)



#导出数据库中的数据
def outAndDelete(request):
    if request.method == 'GET':
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
        sql5 = "SELECT * FROM packetInfo_playrecord INTO OUTFILE '/var/lib/mysql-files/"+infoTime+"packetInfo_playrecord.txt' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';"
        sql6 = "SELECT * FROM packetInfo_videoquality INTO OUTFILE '/var/lib/mysql-files/"+infoTime+"packetInfo_videoquality.txt' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';"

        cur.execute(sql1)
        cur.execute(sql2)
        cur.execute(sql3)
        cur.execute(sql4)
        cur.execute(sql5)
        cur.execute(sql6)

        os.system("cp /var/lib/mysql-files/"+infoTime+"packetInfo_bandwidth.txt"+" /home/a/project/djangoProInfo/djangoInfo/static_file/data/")
        os.system("cp /var/lib/mysql-files/" + infoTime + "packetInfo_retran.txt" + " /home/a/project/djangoProInfo/djangoInfo/static_file/data/")
        os.system("cp /var/lib/mysql-files/" + infoTime + "packetInfo_videoquality.txt" + " /home/a/project/djangoProInfo/djangoInfo/static_file/data/")


        sql1 = "truncate table packetInfo_source"
        sql2 = "truncate table packetInfo_bandwidthdelay"
        sql3 = "truncate table packetInfo_httpcode"
        sql4 = "truncate table packetInfo_retran"
        sql5 = "truncate table packetInfo_playrecord"
        sql6 = "truncate table packetInfo_videoquality"

        cur.execute(sql1)
        cur.execute(sql2)
        cur.execute(sql3)
        cur.execute(sql4)
        cur.execute(sql5)
        cur.execute(sql6)

        cur.close()
        conn.commit()
        conn.close()
        info = 1;
        infoMes = {'out' : info}
        return JsonResponse(infoMes)


#将数据上传至大数据平台
def upToHadoop(request):
    if request.method == 'GET':
        hadoopInfo = 0;
        try:
            os.system('/opt/hadoop-2.7.3/bin/hadoop dfs -put /var/lib/mysql-files/*  hdfs://10.149.252.106:9000/input/netWorkInfo')
            # hdfsClient = pyhdfs.HdfsClient(hosts='10.149.252.106')
            # hdfsClient.copy_from_local('/var/lib/mysql-files/17_04_15_12_34_14packetInfo_bandwidth.txt','hdfs://10.149.252.106:9000/input/netWorkInfo')
            hadoopInfo = 1;
        except Exception,e:
            print Exception,':',e
        infoMes = {'out': hadoopInfo}
        return JsonResponse(infoMes)

#delete hadoop data
def deleteHadoop(request):
    if request.method == 'GET':
        hadoopInfo = 0;
        try:
            os.system('/opt/hadoop-2.7.3/bin/hadoop dfs -rm hdfs://10.149.252.106:9000/input/netWorkInfo/*')
            hadoopInfo = 1;
        except Exception, e:
            print Exception, ':', e
        infoMes = {'out': hadoopInfo}
        return JsonResponse(infoMes)


#get information of bandwidth,delay and jetter OnLine
def getInfoUser(request):
    if request.method == 'GET':
        bwdquery = BandwidthDelay.objects.all()
        bwd = list(bwdquery.values("bandWidth","delay","jetter","bdTIme","ipPlay"))
        infoMes = {"info":bwd}
        return JsonResponse(infoMes)
