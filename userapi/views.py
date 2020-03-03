from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework.request import Request
from django.http import JsonResponse
import requests


class Login(APIView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        return JsonResponse({"msg": "连上了"}, status=200, json_dumps_params={'ensure_ascii': False})

    # 通过前端传来的code取到用户openid
    def post(self, request, *args, **kwargs):
        appid = 'wxc086ccd0244d6104'  # 小程序拥有者appid
        secret = 'd1dbe7a99ac0758f6fe4d9ba721633ad'  # 小程序拥有者秘钥
        code = request.data["code"]
        print(code)
        url = "https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code" % (
            appid, secret, code)
        result = requests.get(url).content.decode("utf-8")
        # result = loads(result)['openid']
        print(result)
        data = {}
        data['openid'] = result
        # print(data)
        return JsonResponse({"msg": "ok"})

