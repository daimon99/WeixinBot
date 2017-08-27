# coding: utf8

from django.conf.urls import url
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^wxloginhistory/wxlogin', views.wx_login_view, name='wxloginhistory_wxlogin'),
    url(r'^wxloginhistory/qrimg', views.get_wx_login_qr_image, name='wxloginhistory_qrimg'),
    url(r'^wxloginhistory/check_login_result', views.check_login_result, name='wxloginhistory_checkloginresult')

]