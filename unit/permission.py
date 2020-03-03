"""
权限模块
"""
from rest_framework.permissions import BasePermission


class VIPPermission(BasePermission):
    """vip权限"""
    message = "vip用户"

    def has_permission(self, request, view):
        if request.user.user_type != 3:
            return False
        return True


class MyPermission(BasePermission):
    """普通用户权限"""
    message = "普通用户"

    def has_permission(self, request, view):
        if request.user.user_type == 3:
            return False
        return True
