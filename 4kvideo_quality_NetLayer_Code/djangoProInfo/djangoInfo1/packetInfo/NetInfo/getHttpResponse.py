# coding:utf-8
# -*- coding: utf-8 -*-
import pcap
import dpkt
import sys
import re
import time
from packetInfo import models
def httpResponse():
    host = 'a'
    source = 'b'
    infoTime = None
    httpCode= None




    while True:
        pc = pcap.pcap()  # 注，参数可为网卡名，如eth0
        pc.setfilter('src 10.149.252.105 and port 80')  # 设置监听过滤器
        try:
            listseq = [0]  # put seq,initial
            reTran = 0;  # 重传率,通过in判断
            packageNum = 0;
            reTranRate = 0.0
            for ptime, pdata in pc:  # ptime为收到时间，pdata为收到数据
                p = dpkt.ethernet.Ethernet(pdata)
                # print ("11111%s %x", ptime, p)
                if p.data.__class__.__name__ == 'IP':
                    ip = '%d.%d.%d.%d' % tuple(map(ord, list(p.data.dst)))
                    if p.data.data.__class__.__name__ == 'TCP':

                        seq = p.data.data.seq
                        ack = p.data.data.ack
                        flag = p.data.data.flags

                        # print data
                        data = tuple(map(ord, list(p.data.data.data)))
                        # print data


                        listlen = len(listseq)

                        if flag == 18:  # 当flag=18的时候,seq重新赋值
                            listseq.append(seq)
                            # 重传好像上后面几个比最后一个要小,
                        elif seq < listseq[listlen - 1]:  # 此时表示重传或者乱序
                            reTran += 1
                        else:
                            # put seq into list
                            listseq.append(seq)

                        packageNum += 1

                        # 每5000个包计算重传率
                        # if (nowTime - startTime) >= 0.1:
                        if packageNum >= 10000:
                            reTranRate = (reTran * 1.0 / packageNum) * 100
                            reTranRate = float('%.5f' % reTranRate)
                            # startTime = nowTime
                            print "============ ================================================="
                            print "%.5f" % reTranRate
                            # infoTime = time.strftime('%H:%M:%S', time.localtime(time.time()))
                            infoTime = time.ctime()[-13:-5]
                            listseq = listseq[len(listseq) - 1]  # 继续上一个
                            reTran = 0
                            packageNum = 0
                            reTran = models.ReTran()
                            reTran.reTran = str(reTranRate)
                            reTran.reTranTIme = str(infoTime)
                            reTran.save()

                        if p.data.data.sport == 80:
                            sStr1 = p.data.data.data
                            # sStr4 = 'GET /'
                            sStr5 = 'HTTP/1.1'
                            res = sStr1.find(sStr5);
                            if(res != -1):
                                #infoTime = time.strftime('%H:%M:%S', time.localtime(time.time()))
                                infoTime = time.ctime()[-13:-5]
                                httpCode = sStr1[9:13]
                                httpcodeDB =models.HTTPCode()
                                httpcodeDB.httpCode = str(httpCode)
                                httpcodeDB.responseTIme = str(infoTime)
                                httpcodeDB.save()
                                #print sStr1[9:13],"time:",infoTime#http cpde
        except TypeError:
            print "a is None"
    return httpCode,infoTime

