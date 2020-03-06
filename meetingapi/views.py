import json
from userapi import models
from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework.request import Request
from django.http import JsonResponse
from unit.serializer import UserSerializer, MeetingSerializer
from unit.md5 import getcurrenttime, md5


class Setmeeting(APIView):
    # 获取用户创建的会议信息
    def get(self, request, *args, **kwargs):

        u_id = request.GET.get('u_id')
        print(u_id)
        obj = models.Meeting.objects.filter(mcreator_id=u_id)
        data = MeetingSerializer(obj, many=True).data
        ret = {
            "data": None,
            "msg": "ok"
        }
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
            "msg": "ok"
        }
        try:
            joindata = request.data
            u_id = joindata["u_id"]
            m_id = joindata['m_id']
            print(u_id,m_id)
            models.Membership.objects.create(user_id=u_id,meeting_id=m_id)
            return JsonResponse(ret)
        except:
            return JsonResponse({"ddd": "not"})
