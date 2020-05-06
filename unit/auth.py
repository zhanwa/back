"""用户认证模块"""
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from userapi import models


class Confirm(BaseAuthentication):
    """
    用户认证模块
    """

    def authenticate(self, request):
        try:
            token = request._request.META['HTTP_TOKEN']

            token_obj = models.User.objects.filter(token=token).first()
            if not token_obj:
                raise exceptions.AuthenticationFailed('认证失败')
            # 在restframework内部会把这两个字段赋值给request,以备后用,前面是request.user 后面是request.auth
            return (token_obj.u_id, token_obj)
        except:
            raise exceptions.AuthenticationFailed('认证失败')

    def authenticate_header(self, val):
        pass