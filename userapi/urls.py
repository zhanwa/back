from django.urls import path, re_path, include
from . import views

urlpatterns = [
    # 登录
    re_path(r'^(?P<version>[v1|v2]+)/login/$', views.Login.as_view(), name='Login'),
    # 用户信息
    re_path(r'^(?P<version>[v1|v2]+)/usermessage/$', views.Usermessage.as_view(), name='Usermessage'),

    # 扫码登录管理页面
    re_path(r'^wslogin/(?P<flag>[wx|web]+)/$', views.Weblogin, name='Weblogin'),
    re_path(r'^wss/$', views.Wss, name='wss')

]
