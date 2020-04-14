from django.conf import settings
from django.urls import path, re_path, include
from . import views
from django.views.static import serve
urlpatterns = [
    re_path(r'^(?P<version>[v1|v2]+)/setmeeting/$', views.Setmeeting.as_view(), name='Setmeeting'),
    re_path(r'^(?P<version>[v1|v2]+)/getmeeting/$', views.Getmeeting.as_view(), name='Getmeeting'),
    re_path(r'^chat/(?P<flag>[wx|web|]+)/(?P<mid>[0-9]+)/(?P<userid>[0-9]+)$', views.Chat, name='chat'),
    re_path(r'^(?P<version>[v1|v2]+)/sign/$', views.Sign.as_view(), name='Sign'),
    re_path(r'^(?P<version>[v1|v2]+)/sign_code/$', views.Signcode.as_view(), name='Signcode'),
    # 处理投票
    re_path(r'^(?P<version>[v1|v2]+)/vote/$', views.Vote.as_view(), name='Vote'),
    # 处理文件
    re_path(r'^(?P<version>[v1|v2]+)/file/$', views.File.as_view(), name='File'),


]
