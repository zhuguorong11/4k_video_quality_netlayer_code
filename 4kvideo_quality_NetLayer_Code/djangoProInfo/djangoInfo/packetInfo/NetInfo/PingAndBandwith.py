from linuxPING import getPing
from linuxBandWidth import getBandWidth
import time
from packetInfo import models
def getPingAndBandWith():
    while True:
        start = time.time();
        average,jetter = getPing()
        bandwidth,infoTime= getBandWidth()
        #end = time.time()
        bwd = models.BandwidthDelay()
        bwd.bandWidth = str(bandwidth)
        bwd.bdTIme = str(infoTime)
        bwd.delay = str(average)
        bwd.jetter = str(jetter)
        bwd.save()
    #print end-start
    #return bandwidth,infoTime,average,delayTime

#bandwidth,infoTime,average,delayTime = getPingAndBandWith()
