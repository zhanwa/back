import json
import uuid
from io import BytesIO
from urllib.request import urlopen

from django.core.files import File
from rest_framework.parsers import MultiPartParser,JSONParser
from unit.md5 import md5, getInetpicture,rep
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
            token = md5(openid)
            isregister = models.User.objects.filter(openid=openid)
            if isregister:
                # 已注册,直接更新一下token就行
                # isregister.update(token=token)
                pass
            else:
                name = request.data["name"]
                face = request.data["face"]
                r = urlopen(face)
                # 将图片地址缓存到bytesio中
                io = BytesIO(r.read())
                # 拼接一个文件名
                img = "{}.jpg".format(uuid.uuid1().hex)
                #File要加img文件名
                # print(File(io,img).name)
                # models.User.objects.update_or_create(
                #     openid=openid,
                #     defaults={'username': name, 'image': File(io), 'token': token})
                models.User.objects.create(openid=openid,username=name,token=token,image=File(io,img))
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
                    try:
                        mess = json.loads(message.decode())
                        allconn[mess['flag']].send(message)
                    except:
                        pass

        except:
            allconn.pop(str(client_id))
            print(allconn)
            print("close")


class Usermessage(APIView):
    '''用户信息'''

    parser_classes = [MultiPartParser,JSONParser, ]
    def get(self, request, *args, **kwargs):
        data = rep()
        uid = request.GET.get('uid')
        user_message = models.User.objects.get(u_id=uid)
        user_message = UserSerializer(instance=user_message).data
        data["data"] = user_message
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = rep()
        type = request.data['type']
        uid = request.data['uid']
        if type == 'avatar':
            # 头像修改
            avatar =  request.FILES.get('avator')
            # 下面的update方法是不能更新正确更新保存的文件路径的，除非我们自己手动拼接文件路径，然后img=路径来进行update更新
            # models.User.objects.filter(u_id=uid).update(image=avatar)
            # 已经使用一个清理就图片模块来删除掉就得头像
            obj = models.User.objects.get(u_id=uid)
            obj.image = avatar
            obj.save()
            rep_avatar = UserSerializer(instance=obj).data['image']
            data['data'] = rep_avatar
            return JsonResponse(data)

clients=defaultdict(list) # 创建客户端列表,保存在线客户端
rooms = defaultdict(list) # 保存房间号 格式为{room_number:[uid....]}
@accept_websocket
def Wss(request):
    global clients
    global rooms
    if request.is_websocket():  # 是websocket连接
        try:
            client_name = uuid.uuid1().hex
            clients[client_name] = request.websocket
            print(clients)
            for message in request.websocket:
                request.websocket.send(message)  # 发送消息到客户端
                print(message)
                # 将信息转为python字符
                mess = json.loads(message.decode())
                print(mess)
                try:
                    # 进入会议
                    if mess['type'] == 'manage' or mess['type'] == 'append':
                        rooms[int(mess['mid'])].append(client_name)
                        print(rooms)
                    # 退出会议
                    if mess['type'] == 'out_meeting':
                        rooms[int(mess['mid'])].remove(client_name)
                        print(rooms[int(mess['mid'])])
                    if mess['type'] == 'vote':
                        for i in rooms[int(mess['mid'])]:
                            print(i)
                            clients[i].send(message)
                except Exception as c:
                    pass
        except Exception as e:
            print('关闭')
            clients.pop(client_name)
            print(clients)
            try:
                rooms[int(mess['mid'])].remove(client_name)
            except:
                pass
    else:
        return JsonResponse({'msg':'nook'})




