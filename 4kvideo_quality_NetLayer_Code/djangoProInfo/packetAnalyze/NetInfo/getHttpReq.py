# coding:utf-8
# -*- coding: utf-8 -*-
import pcap
import dpkt
import sys
import time
import re
import datetime
import MySQLdb
import ConfigParser
src = ''
def httpReq():
    host = 'a'
    source = 'b'
    preInfo = ''  # save preGetInfo
    src = None
    dst = None
    sport = None
    dport = None
    infoTime = None

    synExist = False
    ackExist = False

    startTime = None
    endTime = None
    timeToEstablis = None
    config = ConfigParser.ConfigParser()
    config.readfp(open("config.ini", "rb"))
    videoIp = config.get("global", "ip")
    filterIp = 'dst '+videoIp+' and port 80'
    while True:
        pc = pcap.pcap()  # 注，参数可为网卡名，如eth0
        #pc.setfilter('dst 10.149.252.105 and port 80')  # 设置监听过滤器
        pc.setfilter(filterIp)  # 设置监听过滤器
        try :
            for ptime, pdata in pc:  # ptime为收到时间，pdata为收到数据
                p = dpkt.ethernet.Ethernet(pdata)
                global src
                if p.data.__class__.__name__ == 'IP':
                    src = '%d.%d.%d.%d' % tuple(map(ord, list(p.data.src)))
                    dst = '%d.%d.%d.%d' % tuple(map(ord, list(p.data.dst)))
                    #        print ip
                    if p.data.data.__class__.__name__ == 'TCP':
                        if p.data.data.dport == 80:
                            flag = p.data.data.flags
                            # print "now ip :"+dst
                            if flag == 2 and not ackExist:  # 收到syn,开始建立
                                startTime = datetime.datetime.now().time().strftime("%f")
                                ackExist = True
                                synExist = True

                            if flag == 16 and synExist:  # 收到ack，建立结束
                                endTime = datetime.datetime.now().time().strftime("%f")
                                timeToEstablis = (int(endTime) - int(startTime)) * 1.0 / 1000  # ms
                                synExist = False
                                ackExist = False

                            dport = p.data.data.dport
                            sport = p.data.data.sport
                            sStr1 = p.data.data.data
                            sStr4 = 'GET /'
                            sStr5 = ' HTTP/1.1'
                            regHost = 'Host: \d+.\d+.\d+.\d+'
                            nPosa = sStr1.find(sStr5)
                            hostRearch = re.search(regHost, sStr1)
                            if hostRearch:
                                host = hostRearch.group()
                            for n in range(sStr1.find(sStr4) + 4, nPosa + 1):
                                source = sStr1[sStr1.find(sStr4) + 4:n]
                            getInfo = host + source
                            if getInfo != preInfo:
                                #infoTime = time.strftime('%H:%M:%S', time.localtime(time.time()))
                                infoTime = time.ctime()[-13:-5]
                                #print getInfo, "   time:", infoTime
                                preInfo = getInfo  # save
                                #print timeToEstablis,src,sport,dst,dport
                                srcDst = str(src) + ':' + str(sport) + '->' + str(dst) + ':' + str(dport)
                                # sssource = models.Source()
                                # sssource.srcTodst = str(srcDst)
                                # sssource.urlAdd = str(source)
                                # sssource.reqTIme = str(infoTime)
                                # sssource.TCPtime = str(timeToEstablis)
                                # sssource.save()
                                conn = MySQLdb.connect(
                                    host='10.141.251.146',
                                    port=3306,
                                    user='root',
                                    passwd='118925',
                                    db='zgr',
                                )
                                cur = conn.cursor()
                                sql = "INSERT INTO packetInfo_source(srcTodst, \
                                       urlAdd, reqTIme, TCPtime, ipPlay) \
                                       VALUES ('%s', '%s', '%s', '%s', '%s' )" % \
                                        (str(srcDst), str(source), str(infoTime) , str(timeToEstablis), str(src))
                                try:
                                    cur.execute(sql)
                                    conn.commit()
                                except:
                                    # 发生错误时回滚
                                    conn.rollback()
                                cur.close()
                                conn.close()
        except TypeError:
            print "a is None"

    #return src,sport,dst,dport,source,infoTime
