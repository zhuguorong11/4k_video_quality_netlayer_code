# coding:utf-8
# -*- coding: utf-8 -*-
from datetime import datetime
import pcap
import dpkt
import binascii
import struct
import time
import decimal

def getReTranRate():
    while True:
        a = pcap.pcap()
        a.setfilter('tcp and src 10.149.252.105')  # 可以是'tcp' 'udp' 'port 80'等过滤用的
        #if a == None:
            #break
        print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        try:

            listseq = [0]#put seq,initial
            reTran = 0;#重传率,通过in判断
            packageNum = 0;
            reTranRate = 0.0
            startTime = time.time()
            for i, j in a:

                # print type(i)
                # print type(j)
                tem = dpkt.ethernet.Ethernet(j)

                #print ("11111%s %x", i, tem)

                #time
                # nowTime = decimal.Decimal(i)
                #
                # print startTime
                # print nowTime
                src = '%d.%d.%d.%d' % tuple(map(ord, list(tem.data.src)))
                dst = '%d.%d.%d.%d' % tuple(map(ord, list(tem.data.dst)))
                seq = tem.data.data.seq
                ack = tem.data.data.ack
                flag = tem.data.data.flags

                #print data
                data = tuple(map(ord, list(tem.data.data.data)))
                #print data


                listlen = len(listseq)


                if flag == 18:#当flag=18的时候,seq重新赋值
                    listseq.append(seq)
                    # 重传好像上后面几个比最后一个要小,
                elif seq < listseq[listlen - 1]:  # 此时表示重传或者乱序
                    reTran += 1
                else:
                    # put seq into list
                    listseq.append(seq)

                packageNum += 1

                #每5000个包计算重传率
                # if (nowTime - startTime) >= 0.1:
                if  packageNum >= 10000:
                    reTranRate = (reTran*1.0/packageNum) * 100
                    reTranRate = float('%.5f'%reTranRate)
                    #startTime = nowTime
                    print "============ ================================================="
                    print "%.5f"%reTranRate
                    # infoTime = time.strftime('%H:%M:%S', time.localtime(time.time()))
                    infoTime = time.ctime()[-13:-5]
                    listseq = listseq[len(listseq)-1]#继续上一个
                    reTran = 0
                    packageNum = 0
                    reTran = models.ReTran()
                    reTran.reTran = str(reTranRate)
                    reTran.reTranTIme = str(infoTime)
                    reTran.save()
                    # endtime = time.time()
                    #
                    # print endtime - startTime
                    # startTime = time.time()
                #print tem.data.tos
                #tcpLen = tem.data.len - 40#sum-ip_header-tcp_header
                #print tcpLen
                # #print tem.data.ttl
                # #print tem.data.id
                # ff.write(str(flag))
                # ff.write("\t")
                #print seq;#seqNum
                #ff.write(str(seq))
                #ff.write("\t")
                #ff.write("\n")

                #print src
                #print dst

        except TypeError:
            print "a is None"


