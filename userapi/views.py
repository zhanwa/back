import json
from . import models
from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework.request import Request
from django.http import JsonResponse
import requests
from unit.serializer import UserSerializer


# 使用md5生成随机字符串
def md5(user):
    import hashlib
    import time

    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


class Login(APIView):
    authentication_classes = []

    # 换取openid
    def get(self, request, *args, **kwargs):
        appid = 'wxc086ccd0244d6104'  # 小程序拥有者appid
        secret = 'd1dbe7a99ac0758f6fe4d9ba721633ad'  # 小程序拥有者秘钥
        code = request.query_params["code"]  # type:Request
        print(code)
        url = "https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code" % (
            appid, secret, code)
        result = requests.get(url).content.decode("utf-8")
        result = json.loads(result)
        print(type(result))
        return JsonResponse(result)

    # 登录返回token
    def post(self, request, *args, **kwargs):

        ret = {
            "status": "ok",
            "code": 200,
            "msg": "登录成功",
            "data": None
        }
        try:
            openid = request.data["openid"]
            name = request.data["name"]
            face = request.data["face"]
            token = md5(openid)
            models.User.objects.update_or_create(
                openid=openid,
                defaults={'username': name, 'image': face, 'token': token})
            obj = models.User.objects.get(openid=openid)
            # 序列化数据存储在data中
            data = UserSerializer(obj).data
            ret["data"] = data
            return JsonResponse(ret)
        except Exception as e:
            ret = {
                "status": "not ok",
                "code": 400,
                "msg": "登录失败"
            }
            return JsonResponse(ret)
