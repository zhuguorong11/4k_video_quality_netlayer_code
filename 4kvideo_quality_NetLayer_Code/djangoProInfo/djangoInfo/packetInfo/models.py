from __future__ import unicode_literals
from django.db import models


# Create your models here.
#Bandwidth Delay jetter
class BandwidthDelay(models.Model):
    bandWidth = models.CharField(max_length=20,default='0')
    delay = models.CharField(max_length=20,default='0')
    jetter = models.CharField(max_length=20,default='0')
    bdTIme = models.CharField(max_length=40,default='00:00:00')
    ipPlay = models.CharField(max_length=40,default='0.0.0.0')
    def __unicode__(self):
        return self.bandWidth,self.delay,self.jetter

#source time url tcpTIme
class Source(models.Model):
    srcTodst = models.CharField(max_length=100, default='0')
    urlAdd = models.CharField(max_length=50, default='0')
    reqTIme = models.CharField(max_length=40, default='00:00:00')
    TCPtime = models.CharField(max_length=10, default='0')
    ipPlay = models.CharField(max_length=40, default='0.0.0.0');

    def __unicode__(self):
        return self.srcTodst,self.urlAdd,self.reqTIme,self.TCPtime

#httpcode time
class HTTPCode(models.Model):
    httpCode = models.CharField(max_length=10, default='0')
    responseTIme = models.CharField(max_length=40, default='00:00:00')
    ipPlay = models.CharField(max_length=40, default='0.0.0.0');
    def __unicode__(self):
        return self.httpCode,self.responseTIme

#Retran
class ReTran(models.Model):
    reTran = models.CharField(max_length=10, default='0')
    reTranTIme = models.CharField(max_length=40, default='00:00:00')
    ipPlay = models.CharField(max_length=40, default='0.0.0.0');
    def __unicode__(self):
        return self.reTran,self.reTranTIme

#play_record
class PlayRecord(models.Model):
    ip = models.CharField(max_length=40,default='0.0.0.0')
    filename = models.CharField(max_length=60,default='0')
    time = models.CharField(max_length=40,default='00:00:00')
    width = models.IntegerField(max_length=10,default=0)
    height = models.IntegerField(max_length=10,default=0)
    framerate = models.IntegerField(max_length=10,default=0)
    ext = models.CharField(max_length=20,default='0')
    codecname = models.CharField(max_length=20,default='0')
    pixfmt = models.CharField(max_length=20,default='0')

#video_quality
class VideoQuality(models.Model):
    ip = models.CharField(max_length=40, default='0.0.0.0')
    filename = models.CharField(max_length=60, default='0')
    time = models.CharField(max_length=40,default='00:00:00')
    psnr = models.FloatField(max_length=15,default=0.0)