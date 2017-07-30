# coding:utf-8
# -*- coding: utf-8 -*-
import PingAndBandwith,getHttpResponse,getHttpReq
import MySQLdb
import threading
def startDetect():
    info1 ='0'

    threads = []
    threads.append(threading.Thread(target=getHttpReq.httpReq))
    threads.append(threading.Thread(target=PingAndBandwith.getPingAndBandWith))
    threads.append(threading.Thread(target=getHttpResponse.httpResponse))
    # start
    for t in threads:
        t.start()
     # join
    for t in threads:
        t.join()
    info1 = '1'


print "detecting and analyzing........."
startDetect()