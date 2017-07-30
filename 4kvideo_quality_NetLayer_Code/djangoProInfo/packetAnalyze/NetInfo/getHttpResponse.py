# coding:utf-8
# -*- coding: utf-8 -*-
import pcap
import dpkt
import sys
import re
import time
import MySQLdb
import ConfigParser
class PacketInfo:
    def __init__(self):
        self.listseq = [0]
        self.reTran = 0
        self.packageNum = 0
        self.reTranRate = 0
        self.seq = 0
        self.ack = 0
        self.flag = 0


def httpResponse():
    host = 'a'
    source = 'b'
    infoTime = None
    httpCode= None
    config = ConfigParser.ConfigParser()
    config.readfp(open("config.ini", "rb"))
    videoIp = config.get("global", "ip")
    filterIp = 'src ' + videoIp + ' and port 80'
    # dic save different IP
    ipSet = {}
    while True:
        pc = pcap.pcap()  # 注，参数可为网卡名，如eth0
        #pc.setfilter('src 10.149.252.105 and port 80')  # 设置监听过滤器
        pc.setfilter(filterIp)  # 设置监听过滤器
        try:
            # listseq = [0]  # put seq,initial
            # reTran = 0;  # 重传num
            # packageNum = 0;
            # reTranRate = 0.0
            for ptime, pdata in pc:  # ptime为收到时间，pdata为收到数据
                p = dpkt.ethernet.Ethernet(pdata)
                # print ("11111%s %x", ptime, p)
                if p.data.__class__.__name__ == 'IP':
                    ip = '%d.%d.%d.%d' % tuple(map(ord, list(p.data.dst)))
                    if p.data.data.__class__.__name__ == 'TCP':
                        if ipSet.has_key(ip):  # has this ip
                            print 'has this ip:'+ip
                            ipClinet = ipSet[ip]#get instance
                            ipClinet.seq = p.data.data.seq
                            ipClinet.ack = p.data.data.ack
                            ipClinet.flag = p.data.data.flags

                            listlen = len(ipClinet.listseq)

                            if ipClinet.flag == 18:  # 当flag=18的时候,seq重新赋值
                                ipClinet.listseq.append(ipClinet.seq)
                                # 重传好像上后面几个比最后一个要小,
                            elif ipClinet.seq < ipClinet.listseq[listlen - 1]:  # 此时表示重传或者乱序
                                ipClinet.reTran += 1
                            else:
                                # put seq into list
                                ipClinet.listseq.append(ipClinet.seq)

                            ipClinet.packageNum += 1

                            # 每5000个包计算重传率
                            # if (nowTime - startTime) >= 0.1:
                            if ipClinet.packageNum >= 5000:
                                rate = (ipClinet.reTran * 1.0 / ipClinet.packageNum) * 100
                                ipClinet.reTranRate = float('%.5f' % rate)
                                # startTime = nowTime
                                print "============ ================================================="
                                print "%.5f" % ipClinet.reTranRate
                                # infoTime = time.strftime('%H:%M:%S', time.localtime(time.time()))
                                # if ipClinet.reTranRate < 10.0 :
                                infoTime = time.ctime()[-13:-5]
                                # ipClinet.listseq = ipClinet.listseq[len(ipClinet.listseq) - 1]  # 继续上一个
                                ipClinet.listseq = ipClinet.listseq[-1:]  # 继续上一个
                                ipClinet.reTran = 0
                                ipClinet.packageNum = 0
                                # reTran = models.ReTran()
                                # reTran.reTran = str(reTranRate)
                                # reTran.reTranTIme = str(infoTime)
                                # reTran.save()
                                conn = MySQLdb.connect(
                                    host='10.141.251.146',
                                    port=3306,
                                    user='root',
                                    passwd='118925',
                                    db='zgr',
                                )
                                cur = conn.cursor()
                                sql = "INSERT INTO packetInfo_retran(reTran, \
                                                               reTranTIme,ipPlay) \
                                                               VALUES ('%s', '%s','%s')" % \
                                        (str(ipClinet.reTranRate), str(infoTime), str(ip))
                                try:
                                    cur.execute(sql)
                                    conn.commit()
                                except:
                                    # 发生错误时回滚
                                    conn.rollback()
                                cur.close()
                                conn.close()
                            ipSet[ip] = ipClinet

                            if p.data.data.sport == 80:
                                sStr1 = p.data.data.data
                                # sStr4 = 'GET /'
                                sStr5 = 'HTTP/1.1'
                                res = sStr1.find(sStr5);
                                if(res != -1):
                                    #infoTime = time.strftime('%H:%M:%S', time.localtime(time.time()))
                                    infoTime = time.ctime()[-13:-5]
                                    httpCode = sStr1[9:13]
                                    # httpcodeDB =models.HTTPCode()
                                    # httpcodeDB.httpCode = str(httpCode)
                                    # httpcodeDB.responseTIme = str(infoTime)
                                    # httpcodeDB.save()
                                    #print sStr1[9:13],"time:",infoTime#http cpde
                                    conn = MySQLdb.connect(
                                        host='10.141.251.146',
                                        port=3306,
                                        user='root',
                                        passwd='118925',
                                        db='zgr',
                                    )
                                    cur = conn.cursor()
                                    sql = "INSERT INTO packetInfo_httpcode(httpCode, \
                                                                   responseTIme,ipPlay) \
                                                                   VALUES ('%s', '%s','%s')" % \
                                          (str(httpCode), str(infoTime),str(ip))
                                    try:
                                        cur.execute(sql)
                                        conn.commit()
                                    except:
                                        # 发生错误时回滚
                                        conn.rollback()
                                    cur.close()
                                    conn.close()
                        else:#not has this ip
                            print "new client ip:"+ip
                            ipPacket = PacketInfo()#new instance
                            # ipSet[ip] = ipPacket
                            # ipSet[ip] = ipPacket#save
                            ipPacket.seq = p.data.data.seq
                            ipPacket.ack = p.data.data.ack
                            ipPacket.flag = p.data.data.flags

                            # print data
                            data = tuple(map(ord, list(p.data.data.data)))
                            # print data


                            listlen = len(ipPacket.listseq)

                            if ipPacket.flag == 18:  # 当flag=18的时候,seq重新赋值
                                ipPacket.listseq.append(ipPacket.seq)
                                # 重传好像上后面几个比最后一个要小,
                            elif ipPacket.seq < ipPacket.listseq[listlen - 1]:  # 此时表示重传或者乱序
                                ipPacket.reTran += 1
                            else:
                                # put seq into list
                                ipPacket.listseq.append(ipPacket.seq)

                            ipPacket.packageNum += 1

                            # 每5000个包计算重传率
                            # if (nowTime - startTime) >= 0.1:
                            if ipPacket.packageNum >= 10000:
                                ipPacket.reTranRate = (ipPacket.reTran * 1.0 / ipPacket.packageNum) * 100
                                ipPacket.reTranRate = float('%.5f' % ipPacket.reTranRate)
                                # startTime = nowTime
                                print "============ ================================================="
                                print "%.5f" % ipPacket.reTranRate
                                # infoTime = time.strftime('%H:%M:%S', time.localtime(time.time()))
                                infoTime = time.ctime()[-13:-5]
                                ipPacket.listseq = ipPacket.listseq[-1:]  # 继续上一个
                                ipPacket.reTran = 0
                                ipPacket.packageNum = 0
                                # reTran = models.ReTran()
                                # reTran.reTran = str(reTranRate)
                                # reTran.reTranTIme = str(infoTime)
                                # reTran.save()
                                conn = MySQLdb.connect(
                                    host='10.141.251.146',
                                    port=3306,
                                    user='root',
                                    passwd='118925',
                                    db='zgr',
                                )
                                cur = conn.cursor()
                                sql = "INSERT INTO packetInfo_retran(reTran, \
                                                               reTranTIme,ipPlay) \
                                                               VALUES ('%s', '%s','%s')" % \
                                        (str(ipPacket.reTranRate), str(infoTime), str(ip))
                                try:
                                    cur.execute(sql)
                                    conn.commit()
                                except:
                                    # 发生错误时回滚
                                    conn.rollback()
                                cur.close()
                                conn.close()
                            ipSet[ip] = ipPacket

                            if p.data.data.sport == 80:
                                sStr1 = p.data.data.data
                                # sStr4 = 'GET /'
                                sStr5 = 'HTTP/1.1'
                                res = sStr1.find(sStr5);
                                if(res != -1):
                                    #infoTime = time.strftime('%H:%M:%S', time.localtime(time.time()))
                                    infoTime = time.ctime()[-13:-5]
                                    httpCode = sStr1[9:13]
                                    # httpcodeDB =models.HTTPCode()
                                    # httpcodeDB.httpCode = str(httpCode)
                                    # httpcodeDB.responseTIme = str(infoTime)
                                    # httpcodeDB.save()
                                    #print sStr1[9:13],"time:",infoTime#http cpde
                                    conn = MySQLdb.connect(
                                        host='10.141.251.146',
                                        port=3306,
                                        user='root',
                                        passwd='118925',
                                        db='zgr',
                                    )
                                    cur = conn.cursor()
                                    sql = "INSERT INTO packetInfo_httpcode(httpCode, \
                                                                   responseTIme,ipPlay) \
                                                                   VALUES ('%s', '%s','%s')" % \
                                          (str(httpCode), str(infoTime),str(ip))
                                    try:
                                        cur.execute(sql)
                                        conn.commit()
                                    except:
                                        # 发生错误时回滚
                                        conn.rollback()
                                    cur.close()
                                    conn.close()

        except Exception,e:
            print "a is None",Exception,":",e
    #return httpCode,infoTime



#one IP
# def httpResponse():
#     host = 'a'
#     source = 'b'
#     infoTime = None
#     httpCode= None
#
#     while True:
#         pc = pcap.pcap()  # 注，参数可为网卡名，如eth0
#         pc.setfilter('src 10.149.252.105 and port 80')  # 设置监听过滤器
#         try:
#             listseq = [0]  # put seq,initial
#             reTran = 0;  # 重传num
#             packageNum = 0;
#             reTranRate = 0.0
#             for ptime, pdata in pc:  # ptime为收到时间，pdata为收到数据
#                 p = dpkt.ethernet.Ethernet(pdata)
#                 # print ("11111%s %x", ptime, p)
#                 if p.data.__class__.__name__ == 'IP':
#                     ip = '%d.%d.%d.%d' % tuple(map(ord, list(p.data.dst)))
#                     if p.data.data.__class__.__name__ == 'TCP':
#
#                         seq = p.data.data.seq
#                         ack = p.data.data.ack
#                         flag = p.data.data.flags
#
#                         # print data
#                         data = tuple(map(ord, list(p.data.data.data)))
#                         # print data
#
#
#                         listlen = len(listseq)
#
#                         if flag == 18:  # 当flag=18的时候,seq重新赋值
#                             listseq.append(seq)
#                             # 重传好像上后面几个比最后一个要小,
#                         elif seq < listseq[listlen - 1]:  # 此时表示重传或者乱序
#                             reTran += 1
#                         else:
#                             # put seq into list
#                             listseq.append(seq)
#
#                         packageNum += 1
#
#                         # 每5000个包计算重传率
#                         # if (nowTime - startTime) >= 0.1:
#                         if packageNum >= 10000:
#                             reTranRate = (reTran * 1.0 / packageNum) * 100
#                             reTranRate = float('%.5f' % reTranRate)
#                             # startTime = nowTime
#                             print "============ ================================================="
#                             print "%.5f" % reTranRate
#                             # infoTime = time.strftime('%H:%M:%S', time.localtime(time.time()))
#                             infoTime = time.ctime()[-13:-5]
#                             listseq = listseq[len(listseq) - 1]  # 继续上一个
#                             reTran = 0
#                             packageNum = 0
#                             # reTran = models.ReTran()
#                             # reTran.reTran = str(reTranRate)
#                             # reTran.reTranTIme = str(infoTime)
#                             # reTran.save()
#                             conn = MySQLdb.connect(
#                                 host='10.141.251.146',
#                                 port=3306,
#                                 user='root',
#                                 passwd='118925',
#                                 db='zgr',
#                             )
#                             cur = conn.cursor()
#                             sql = "INSERT INTO packetInfo_retran(reTran, \
#                                                            reTranTIme,ipPlay) \
#                                                            VALUES ('%s', '%s','%s')" % \
#                                     (str(reTranRate), str(infoTime), str(ip))
#                             try:
#                                 cur.execute(sql)
#                                 conn.commit()
#                             except:
#                                 # 发生错误时回滚
#                                 conn.rollback()
#                             cur.close()
#                             conn.close()
#
#                         if p.data.data.sport == 80:
#                             sStr1 = p.data.data.data
#                             # sStr4 = 'GET /'
#                             sStr5 = 'HTTP/1.1'
#                             res = sStr1.find(sStr5);
#                             if(res != -1):
#                                 #infoTime = time.strftime('%H:%M:%S', time.localtime(time.time()))
#                                 infoTime = time.ctime()[-13:-5]
#                                 httpCode = sStr1[9:13]
#                                 # httpcodeDB =models.HTTPCode()
#                                 # httpcodeDB.httpCode = str(httpCode)
#                                 # httpcodeDB.responseTIme = str(infoTime)
#                                 # httpcodeDB.save()
#                                 #print sStr1[9:13],"time:",infoTime#http cpde
#                                 conn = MySQLdb.connect(
#                                     host='10.141.251.146',
#                                     port=3306,
#                                     user='root',
#                                     passwd='118925',
#                                     db='zgr',
#                                 )
#                                 cur = conn.cursor()
#                                 sql = "INSERT INTO packetInfo_httpcode(httpCode, \
#                                                                responseTIme,ipPlay) \
#                                                                VALUES ('%s', '%s','%s')" % \
#                                       (str(httpCode), str(infoTime),str(ip))
#                                 try:
#                                     cur.execute(sql)
#                                     conn.commit()
#                                 except:
#                                     # 发生错误时回滚
#                                     conn.rollback()
#                                 cur.close()
#                                 conn.close()
#         except TypeError:
#             print "a is None"
#     return httpCode,infoTime

# httpResponse()