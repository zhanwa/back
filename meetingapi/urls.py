from django.urls import path, re_path, include
from . import views

urlpatterns = [
    re_path(r'^(?P<version>[v1|v2]+)/setmeeting/$', views.Setmeeting.as_view(), name='Setmeeting'),
    re_path(r'^(?P<version>[v1|v2]+)/getmeeting/$', views.Getmeeting.as_view(), name='Getmeeting'),
]
