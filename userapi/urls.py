from django.urls import path, re_path, include
from . import views

urlpatterns = [
    re_path(r'^(?P<version>[v1|v2]+)/login/$', views.Login.as_view(), name='Login'),
    re_path(r'^wslogin/(?P<flag>[wx|web]+)/$', views.Weblogin, name='Weblogin')

]
