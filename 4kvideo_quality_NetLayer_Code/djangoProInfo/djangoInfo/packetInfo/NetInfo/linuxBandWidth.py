#coding=utf-8
# -*- coding: utf-8 -*-
import os
import sys
import re
import subprocess
import threading
import time
import datetime


def getBandWidth():
    #调用系统自带的ping.exe
    p = subprocess.Popen('iperf -c 10.149.252.105 -t 1', stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    out = p.stdout.read().decode('gbk')
    #print out
    regBand = r'(\d+.\d+) Mbits/sec'

    #infoTime = time.strftime('%H:%M:%S', time.localtime(time.time()))
    infoTime = time.ctime()[-13:-5]
    bandWidth = re.search(regBand,out)

    if bandWidth:
        bandWidth = bandWidth.group(1)
        bandWidth = str(bandWidth)
        bandWidth = float(bandWidth)/8


    # with open('/home/a/bandwidth.txt','a+') as f:
    #      f.write(str(bandWidth))
    #      f.write('\n')
    #print 'current BandWidth to 10.149.252.105 is %s Mbps'% bandWidth
    return bandWidth,infoTime
#
# def Bandtest():
#     print 'bandWidth Test thread %s is running...' % threading.current_thread().name
#     for i in range(10):
#         startTime = time.time()
#         t = threading.Thread(target=getBandWidth)
#         t.start()#线程启动
#         print '线程已经启动了'
#         #检验线程池中的线程是否结束，没有结束就阻塞直到线程结束
#         t.join()#等待线程结束
#         endTime = time.time()
#         print '执行一次的事件为',endTime-startTime,'s'
#     print 'ing-----------------'
#     print 'thread %s ended.' % threading.current_thread().name
