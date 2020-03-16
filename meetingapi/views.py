import json
from userapi import models
from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework.request import Request
from django.http import JsonResponse
from unit.serializer import UserSerializer, MeetingSerializer
from unit.md5 import getcurrenttime, md5


class Setmeeting(APIView):
    # 获取用户创建和参加的会议信息
    def get(self, request, *args, **kwargs):
        ret = {
            "data": None,
            "msg": "ok"
        }
        u_id = request.GET.get('u_id')
        opt = request.GET.get('opt')
        print(opt)
        print(u_id)
        # 我创建的会议
        if opt == 'create':
            obj = models.Meeting.objects.filter(mcreator_id=u_id)
            data = MeetingSerializer(obj, many=True).data

            ret["data"] = data
            return JsonResponse(ret)
        # 我参加的会议
        elif opt == 'append':
            # 因为多对多通过menbers连接的User的,故members__u_id双下划线查找,把User里u_id=u_id的会议返回出来
            obj = models.Meeting.objects.filter(members__u_id=u_id)
            print(obj)
            data = MeetingSerializer(obj, many=True).data
            ret["data"] = data
            return JsonResponse(ret)
        # 所有会议
        elif opt == "all":
            obj = models.Meeting.objects.all()
            data = MeetingSerializer(obj, many=True).data
            ret["data"] = data
            return JsonResponse(ret)

    # 创建会议
    def post(self, request, *args, **kwargs):
        ret = {
            "data": None,
            "msg": "ok"
        }
        # 获取当前时间
        current_time = getcurrenttime()

        print(request.data)
        try:
            meetingdata = request.data
            u_id = meetingdata["u_id"]
            title = meetingdata["title"]
            dec = meetingdata["dec"]
            serect = meetingdata["serect"]
            location = meetingdata["location"]
            start_date = meetingdata["date"]
            label = meetingdata["label"]
            # 会议标识符
            sign = md5(serect)
            create_date = current_time
            models.Meeting.objects.create(msign_id=sign, m_title=title, c_time=create_date, m_place=location,
                                          m_content=dec, mcreator_id=u_id, mlabel=label, b_time=start_date)
            obj = models.Meeting.objects.get(msign_id=sign)
            data = MeetingSerializer(obj).data
            print(data)
            ret["data"] = data
            return JsonResponse(ret)
        except:
            return JsonResponse({"ddd": "not"})


class Getmeeting(APIView):
    # 返回会议详细数据
    def get(self, request, *args, **kwargs):
        m_id = request.GET.get('m_id')
        print(m_id)
        obj = models.Meeting.objects.get(m_id=m_id)
        data = MeetingSerializer(obj).data
        ret = {
            "data": None,
            "msg": "ok"
        }
        ret["data"] = data
        return JsonResponse(ret)

    # 声请加入
    def post(self, request, *args, **kwargs):
        ret = {
            "data": None,
            "msg": "200"
        }
        try:
            joindata = request.data
            u_id = joindata["u_id"]
            m_id = joindata['m_id']
            print(u_id, m_id)
            obj = models.Membership.objects.filter(user_id=u_id, meeting_id=m_id)
            if not obj:
                models.Membership.objects.create(user_id=u_id, meeting_id=m_id)
                return JsonResponse(ret)
            else:
                ret["data"] = "请勿重复报名"
                ret["msg"] = "302"
                return JsonResponse(ret)
        except:
            return JsonResponse({"ddd": "not"})


from dwebsocket.decorators import accept_websocket, require_websocket
from collections import defaultdict

# 保存所有接入的用户地址
allconn = defaultdict(list)
rooms = []


@accept_websocket
def Chat(request, mid, userid):
    # allresult = {}
    # # 获取用户信息
    # userinfo = request.user
    # allresult['userinfo'] = userinfo
    # print(allresult)
    # # 声明全局变量
    global allconn
    global rooms
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return JsonResponse(message)
        except:
            return JsonResponse({"msg": "no ok"})
    else:
        try:
            # 将链接(请求？)存入全局字典中
            if mid not in rooms:
                rooms.append(mid)
            print(rooms)
            allconn[str(userid)] = request.websocket
            print(allconn)
            # 遍历请求地址中的消息
            for message in request.websocket:
                # 将信息发至自己的聊天框
                request.websocket.send(message)
                # 将信息发至其他所有用户的聊天框
                for i in allconn:
                    if i != str(userid):
                        allconn[i].send(message)
        except:
            allconn.pop(str(userid))
            print(allconn)
            print("close")


class Sign(APIView):
    """处理签到"""

    def get(self, request, *args, **kwargs):
        """获取签到人员"""
        ret = {
            "data": None,
            "msg": "200"
        }
        try:
            m_id = request.data['m_id']
            models.Membership.objects.filter(meeting_id=m_id)
        except:
            pass
        return JsonResponse(ret)

    def post(self, request, *args, **kwargs):
        # 签到
        ret = {
            "data": None,
            "msg": "200"
        }
        try:
            u_id = request.data['u_id']
            m_id = request.data['m_id']
            print(u_id, m_id)
            models.Membership.objects.filter(user_id=u_id, meeting_id=m_id).update(sign="1")
            return JsonResponse(ret)
        except:
            ret["msg"] = "404"
            return JsonResponse(ret)
