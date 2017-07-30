# coding:utf-8
# -*- coding: utf-8 -*-
"""djangoInfo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from packetInfo.views import *
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',index,name='index'),

    # url(r'^startDetect/$',startDetect,name='startDetect'),
    # url(r'^startCalReTran/$',startCalReTran,name='startCalReTran'),
    url(r'^getInfoSource/$',getInfoSource,name='getInfoSource'),
    url(r'^getInfoDelay/$',getInfoDelay,name='getInfoDelay'),
    url(r'^getReTran/$',getReTran,name='getReTran'),
    url(r'^outAndDelete/$',outAndDelete,name='outAndDelete'),
    url(r'^upToHadoop/$',upToHadoop,name='upToHadoop'),
    url(r'^deleteHadoop/$',deleteHadoop,name='deleteHadoop'),
    url(r'^getInfoUser/$',getInfoUser,name='getInfoUser'),
    url(r'^getVideoInfo/$',getVideoInfo,name='getVideoInfo'),
    url(r'^getVideoQuqlity/$',getVideoQuqlity,name='getVideoQuqlity'),
    # url(r'^startDetectHttpCode/$',startDetectHttpCode,name='startDetectHttpCode'),
    # url(r'^startDetectSource/$',startDetectSource,name='startDetectSource'),
    #test
    # url(r'^ajax_list/$', ajax_list, name='ajax-list'),
    # url(r'^ajax_dict/$',ajax_dict , name='ajax-dict'),


]
