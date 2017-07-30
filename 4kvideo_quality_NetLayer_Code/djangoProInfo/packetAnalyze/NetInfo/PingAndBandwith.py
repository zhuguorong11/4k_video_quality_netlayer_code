#coding=utf-8
# -*- coding: utf-8 -*-
from linuxPING import getPing
from linuxBandWidth import getBandWidth
import time
import MySQLdb
def getPingAndBandWith():
    while True:
        start = time.time();
        average,jetter = getPing()
        bandwidth,infoTime,src= getBandWidth()
        #end = time.time()
        # bwd = models.BandwidthDelay()
        # bwd.bandWidth = str(bandwidth)
        # bwd.bdTIme = str(infoTime)
        # bwd.delay = str(average)
        # bwd.jetter = str(jetter)
        # bwd.save()
    #print end-start
    #return bandwidth,infoTime,average,delayTime
        conn = MySQLdb.connect(
            host='10.141.251.146',
            port=3306,
            user='root',
            passwd='118925',
            db='zgr',
        )
        cur = conn.cursor()
        sql = "INSERT INTO packetInfo_bandwidthdelay(bandWidth, \
                                    delay,jetter,bdTIme,ipPlay) \
                                    VALUES ('%s', '%s', '%s', '%s','%s')" % \
              (str(bandwidth),  str(average),str(jetter),str(infoTime),str(src))
        try:
            cur.execute(sql)
            conn.commit()
        except:
            # 发生错误时回滚
            conn.rollback()
        cur.close()
        conn.close()
#bandwidth,infoTime,average,delayTime = getPingAndBandWith()
