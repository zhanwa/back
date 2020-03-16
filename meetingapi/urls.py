from django.urls import path, re_path, include
from . import views

urlpatterns = [
    re_path(r'^(?P<version>[v1|v2]+)/setmeeting/$', views.Setmeeting.as_view(), name='Setmeeting'),
    re_path(r'^(?P<version>[v1|v2]+)/getmeeting/$', views.Getmeeting.as_view(), name='Getmeeting'),
    re_path(r'^chat/(?P<mid>[0-9]+)/(?P<userid>[0-9]+)$', views.Chat, name='chat'),
    re_path(r'^(?P<version>[v1|v2]+)/sign/$', views.Sign.as_view(), name='Sign'),

]
