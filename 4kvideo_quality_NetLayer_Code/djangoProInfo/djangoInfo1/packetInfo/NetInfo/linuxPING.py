#coding=utf-8
# -*- coding: utf-8 -*-
import os
import sys
import re
import subprocess
import threading
import time
#获取rtt的函数，即得到average值
def getPing():
    #调用系统自带的ping.exe
    p = subprocess.Popen('ping -c 4 10.149.252.105', stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    out = p.stdout.read().decode('gbk')


    regIP = r'\d+\.\d+\.\d+\.\d+'
    regRtt = r'min/avg/max/mdev = \d+.\d+/\d+.\d+/\d+.\d+/\d+.\d+'
    regTime = u'time=\d+.\d+ ms|时间=\d+.\d+ ms'



    ip = re.search(regIP,out)
    rttString = re.search(regRtt,out)
    eachTime = re.findall(regTime,out)#找到每一次的时延

    if ip:
        ip = ip.group()
    if rttString:
        rttTime = rttString.group().split(r"=")[1]
        if rttTime:
            rttGet = rttTime.split(r"/")
            if rttGet:
                minimum = rttGet[0]
                maximum = rttGet[2]
                average = rttGet[1]
    if eachTime:
        eachTime = [ time.split('=')[1][:-2] for time in eachTime ]#对时间进行处理，得到只含数字的列表


    #计算时延范围
    timeDiff = []
    for i in eachTime:
         #要对i，average进行int转换，因为之前得到的是unicode，不支持-
        diff = abs(float(i)-float(average))
        timeDiff.append(diff)

    #包抖动是包延时与平均传输延时的差值的平均值。
    #得到最小抖动和最大抖动
    minDelay = min(timeDiff)
    maxDelay = max(timeDiff)
    delayTime = sum(timeDiff)*1.0/len(timeDiff)

    #address data
    average = float(average)
    delayTime = float(delayTime)
    # minimum = float(minimum) * 100
    # maximum = float(maximum) * 100
    # minDelay = float(minDelay) * 100
    # maxDelay = float(maxDelay) * 100

    #return (ip,lost,minimum,maximum,average,minDelay,maxDelay)
    #
    # ip,lost,minimum,maximum,average,minDelay,maxDelay,delayTime = ip,lost,minimum,maximum,average,minDelay,maxDelay,delayTime
    # with open('/home/a/test.txt','a+') as f:
    #      f.write(str("%.2f"%average))
    #      f.write('ms')
    #      f.write('   ')
    #      f.write(str("%.3f"%delayTime))
    #      f.write('ms')
    #      f.write('\n')
    #print 'ip:'+ip
    #print 'lostPackage:'+lost
    #print '延迟average:',float(average),'ms'
    # print 'maximum:',maximum,'ms'
    # print 'minimum:',minimum,'ms'
    # print '抖动范围是',minDelay,'ms--',maxDelay,'ms'
    #print '包抖动平均值为',delayTime,'ms'
    return average,delayTime
# def Rtttest():
#     print 'RTT Test thread %s is running...' % threading.current_thread().name
#     for i in range(10):
#         startTime = time.time()
#         t = threading.Thread(target=getPing)
#         t.start()#线程启动
#         print '线程已经启动了'
#         #检验线程池中的线程是否结束，没有结束就阻塞直到线程结束
#         t.join()#等待线程结束
#         endTime = time.time()
#         print '执行一次的事件为',endTime-startTime,'s'
#     print 'ing-----------------'
#     print 'thread %s ended.' % threading.current_thread().name
