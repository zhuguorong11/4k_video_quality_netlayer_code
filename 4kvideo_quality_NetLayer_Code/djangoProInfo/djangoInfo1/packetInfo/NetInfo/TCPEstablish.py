# coding:utf-8
# -*- coding: utf-8 -*-
import datetime
import time
import pcap
import dpkt

#tcp建立时间
def TcpTime():
    host = 'a'
    source = 'b'

    synExist = False
    ackExist = False

    startTime = None
    endTime = None
    timeToEstablis = None
    pc = pcap.pcap()  # 注，参数可为网卡名，如eth0
    pc.setfilter('dst 10.149.252.105 and port 80')  # 设置监听过滤器
    for ptime, pdata in pc:  # ptime为收到时间，pdata为收到数据
        p = dpkt.ethernet.Ethernet(pdata)
        if p.data.__class__.__name__ == 'IP':
            ip = '%d.%d.%d.%d' % tuple(map(ord, list(p.data.dst)))
            #        print ip
            if p.data.data.__class__.__name__ == 'TCP':
                if p.data.data.dport == 80:
                    flag = p.data.data.flags
                    if flag == 2 and not ackExist:#收到syn,开始建立
                        startTime = datetime.datetime.now().time().strftime("%f")
                        ackExist = True
                        synExist = True

                    if flag == 16 and synExist:#收到ack，建立结束
                        endTime = datetime.datetime.now().time().strftime("%f")
                        timeToEstablis = (int(endTime) - int(startTime))*1.0/1000#ms
                        synExist = False
                        ackExist = False
                        #print timeToEstablis
    return timeToEstablis



