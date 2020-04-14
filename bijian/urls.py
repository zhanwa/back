"""programserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include

# import api

# 导入restframework的路由
# from rest_framework import routers
#
# # 引用的是 ModelViewSet视图,自动生成url
# router = routers.DefaultRouter()
# router.register(r'autourl', views.Viewprower)
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/v1/User/', views.UserLogin.as_view(), name='User'),
    # path('api/v1/User2/', views.User2.as_view(), name='User2'),
    # re_path(r'^api/(?P<version>[v1|v2]+)/user3/$', views.User3.as_view(), name='User3'),
    # re_path(r'^api/(?P<version>[v1|v2]+)/seri/$', views.Seri.as_view(), name='Seri'),
    # re_path(r'^api/(?P<version>[v1|v2]+)/viewprower/(?P<pk>\d+)/$', views.Viewprower.as_view({
    #     'get': 'retrieve', 'post': 'create', 'delete': 'destroy', 'put': 'update', 'patch': 'partial_update'
    # }), name='viewprower'),
    #
    # re_path(r'^(?P<version>[v1|v2]+)/', include(router.urls)),
    # path('webscoket/', views.webscoket, name='webscoket'),

    # api路由
    path('userapi/', include('userapi.urls')),
    path('meetingapi/', include('meetingapi.urls')),

    # 获取图片接口
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
