import json
import uuid

from unit.md5 import md5
from . import models
from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework.request import Request
from django.http import JsonResponse
import requests
from unit.serializer import UserSerializer


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




from dwebsocket.decorators import accept_websocket, require_websocket
from collections import defaultdict
# 保存所有接入的用户地址
allconn = defaultdict(list)


@accept_websocket
def Weblogin(request,flag):
    global allconn
    print(flag)
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return JsonResponse(message)
        except:
            return JsonResponse({"msg": "no ok"})
    else:
        try:
            if flag == 'web':
            # 生成每个uuid,用来区分登录
                client_id = uuid.uuid4()
                allconn[str(client_id)] = request.websocket
                print(allconn)
                for message in request.websocket:
                    # 将client_id转为字符串再转为字节发送到前端
                    request.websocket.send(str(client_id).encode('utf-8'))
                if request.websocket.is_close():
                    allconn.pop(str(client_id))
                    print(allconn)
                    print("close")
            if flag == 'wx':
                for message in request.websocket:
                    mess = json.loads(message.decode())
                    allconn[mess['flag']].send(message)

        except:
            allconn.pop(str(client_id))
            print(allconn)
            print("close")
