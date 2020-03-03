"""这是节流模块 控制访问频率"""
from rest_framework.throttling import BaseThrottle,SimpleRateThrottle
import time

# 匿名用户
class VisitThrottle(SimpleRateThrottle):
   """使用内置的SimpleRateThrottle类完成控制"""
   # 与配置文件中的visit对应
   scope = "visit"
   def get_cache_key(self, request, view):
       return self.get_ident(request)

# 登录用户
class UserThrottle(SimpleRateThrottle):
   """使用内置的SimpleRateThrottle类完成控制"""
   # 与配置文件中的Login对应
   scope = "login"
   def get_cache_key(self, request, view):
       return request.user.username