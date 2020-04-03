import json
import random
import threading

from userapi import models
from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework.request import Request
from django.http import JsonResponse
from unit.serializer import UserSerializer, MeetingSerializer, MembershipSerializer, VotethemeSerializer, VoteoptionSerializer
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
def Chat(request, flag, mid, userid):
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
            # 将用户和响应的socket组成字典
            user_socket = {flag + userid: request.websocket}
            # 将链接(请求？)存入全局字典中
            if mid not in rooms:
                rooms.append(mid)
            print(rooms)
            for room in rooms:
                if mid == room:
                    # 将所有房间放在rooms字典,将所有用户和对应socket嵌套到rooms入面
                    if room in allconn:
                        allconn[str(room)] = {**allconn[str(room)], **user_socket}
                    else:
                        allconn[str(room)] = user_socket

            # allconn[str(userid)] = request.websocket
            print(allconn)
            # 遍历请求地址中的消息
            for message in request.websocket:
                # 将信息发至自己的聊天框
                request.websocket.send(message)
                # 将信息发至其他所有用户的聊天框
                for i in allconn[mid]:
                    if i != str(flag + userid):
                        # 将message字节编码成unicode字符串再loads成python字典数据格式
                        mess = json.loads(message.decode())
                        print(mess)
                        # 把type修改为otherbarrage
                        mess["type"] = 'otherbarrage'
                        message = json.dumps(mess)
                        allconn[mid][i].send(message.encode('utf-8'))
        except:
            allconn[mid].pop(str(flag + userid))
            if not allconn[mid]:
                allconn.pop(str(mid))
                rooms.remove(mid)
            print(rooms)
            print(allconn)
            print("close")


import time


class Sign(APIView):
    """处理签到"""

    def get(self, request, *args, **kwargs):
        """获取签到人员"""
        ret = {
            "data": None,
            "msg": "200"
        }
        try:
            cc = []
            m_id = request.GET.get('m_id')
            print(m_id)
            sign = models.Membership.objects.filter(meeting_id=m_id)
            user = models.User.objects.filter(meeting__m_id=m_id)
            data0 = UserSerializer(user, many=True).data
            data = MembershipSerializer(sign, many=True).data
            # 将签到信息和用户信息共同返回
            for i in range(len(data)):
                cc.append({**data[i], **data0[i]})
            ret["data"] = cc
            return JsonResponse(ret)
        except:
            ret["msg"] = "404"
            return JsonResponse(ret)

    def post(self, request, *args, **kwargs):
        # 签到
        import datetime
        ret = {
            "data": None,
            "msg": "200"
        }
        try:
            u_id = request.data['u_id']
            m_id = request.data['m_id']
            print(u_id, m_id)
            models.Membership.objects.filter(user_id=u_id, meeting_id=m_id).update(sign=True,
                                                                                   sign_time=datetime.datetime.now())
            return JsonResponse(ret)
        except:
            ret["msg"] = "404"
            return JsonResponse(ret)


import uuid


class Signcode(APIView):
    '''签到二维码'''

    def random_sign(self):
        sign_flag = uuid.uuid4()
        print(sign_flag)
        global timer
        timer = threading.Timer(3, self.random_sign)
        timer.start()

    def get(self, request, *args, **kwargs):
        pass


class Vote(APIView):
    # 处理投票的api
    def get(self, request, *args, **kwargs):
        data = {
            'msg':None,
            'data':[]
        }
        try:
            # 定义一个空的字典,用来装返回结果
            m_id = request.GET.get('mid')
            vote_themes = models.Votetheme.objects.filter(meeting=m_id)
            # QuerySet对象可迭代,不为空,循环拿到theme_id
            if vote_themes:
                for vote_theme in vote_themes:
                    # 如果这两个放到外面,后面的值会覆盖前面的,因为内存是一样的,你修改了之后,大家就都一样了
                    r_data = {}
                    choices = []

                    question = VotethemeSerializer(vote_theme).data
                    r_data['question'] = question['theme_name']
                    r_data['time'] = question['vote_time']
                    # 通过_set反向查询
                    vote_options = vote_theme.voteoption_set.all()
                    options = VoteoptionSerializer(vote_options,many=True).data
                    for i in options:
                        choices.append(i['option'])
                    r_data['choices'] = choices
                    data['data'].append(r_data)
            data['msg'] = 'ok'
            return JsonResponse(data)

        except:
            return JsonResponse({'msg': 'no ok'})

    def post(self, request, *args, **kwargs):
        try:
            m_id = request.data['mid']
            votes = request.data['vote']
            print(m_id, votes, type(votes))
            for vote in votes:
                index = ''.join(str(uuid.uuid4()).split('-'))
                models.Votetheme.objects.create(theme_name=vote['question'], theme_id=index, meeting_id=m_id)

                for choice in vote['choices']:
                    models.Voteoption.objects.create(option=choice, votetheme_id=index)
            return JsonResponse({'msg': 'ok'})
        except:
            return JsonResponse({'msg': 'no ok'})

from rest_framework.parsers import MultiPartParser
class File(APIView):
    '''
    处理文件
    '''
    # 处理请求头content - type为multipart / form - data的请求体
    parser_classes = [MultiPartParser,]
    def post(self, request, *args, **kwargs):
        print(request,request.FILES)
        return JsonResponse({'msg':'ok'})