import json
import os
import random
import threading

from django.utils.encoding import escape_uri_path
from userapi import models
from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework.request import Request
from django.http import JsonResponse, FileResponse, Http404
from unit.serializer import UserSerializer, MeetingSerializer, MembershipSerializer, VotethemeSerializer, \
    VoteoptionSerializer, DocumentSerializer, LotterySerializer
from unit.md5 import getcurrenttime, md5

from bijian import settings
import time
import datetime


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
            # # 抓取会议管理员id,加到data中返回
            # admins = models.Membership.objects.filter(admin=1).values('user_id')
            # for admin in admins:
            #     data.append(admin)
            # print(data)
            ret["data"] = data
            return JsonResponse(ret)

    # 创建会议
    def post(self, request, *args, **kwargs):
        global type
        ret = {
            "data": None,
            "msg": "ok"
        }
        # 获取当前时间
        current_time = getcurrenttime()
        try:
            meetingdata = request.data
            u_id = meetingdata["u_id"]
            title = meetingdata["title"]
            dec = meetingdata["dec"]
            serect = meetingdata["serect"]
            location = meetingdata["location"]
            create_date = meetingdata["date"]
            # 标签
            label = json.dumps(meetingdata["label"], ensure_ascii=False)
            # 会议类型
            type = meetingdata["type"]
            # 人数限制
            limit = meetingdata["limit"]
            # 时间
            start_date = meetingdata["start_date"]
            start_time = meetingdata["start_time"]
            stop_date = meetingdata["stop_date"]
            stop_time = meetingdata["stop_time"]
            # 会议标识符
            sign = uuid.uuid1().hex
            # 创建会议
            models.Meeting.objects.create(msign_id=sign, gcontent=type, vcontent=serect, e_time=start_date,
                                          s_time=stop_date, m_title=title, c_time=start_time, m_place=location,
                                          m_content=dec, mcreator_id=u_id, mlabel=label, b_time=stop_time, limits=limit)

            obj = models.Meeting.objects.get(msign_id=sign)
            data = MeetingSerializer(obj).data
            # 在menbership中注册为管理员
            models.Membership.objects.create(user_id=u_id, meeting_id=data["m_id"], admin=True)
            print(data)
            ret["data"] = data
            return JsonResponse(ret)
        except:
            return JsonResponse({"ddd": "not"})

    def put(self, request, *args, **kwargs):
        """用户修改会议"""
        ret = {
            "data": None,
            "msg": "ok"
        }
        # 获取当前时间
        current_time = getcurrenttime()
        try:
            meetingdata = request.data
            m_id = meetingdata["mid"]
            title = meetingdata["title"]
            dec = meetingdata["dec"]
            serect = meetingdata["serect"]
            location = meetingdata["location"]
            # 标签
            label = json.dumps(meetingdata["label"], ensure_ascii=False)
            # 会议类型
            type = meetingdata["type"]
            # 人数限制
            limit = meetingdata["limit"]
            # 时间
            start_date = meetingdata["start_date"]
            start_time = meetingdata["start_time"]
            stop_date = meetingdata["stop_date"]
            stop_time = meetingdata["stop_time"]
            # 修改会议
            models.Meeting.objects.filter(m_id=m_id).update(gcontent=type, vcontent=serect, e_time=start_date,
                                                            s_time=stop_date, m_title=title, c_time=start_time,
                                                            m_place=location, m_content=dec, mlabel=label,
                                                            b_time=stop_time, limits=limit)
            return JsonResponse(ret)
        except:
            return JsonResponse({"ddd": "not"})

    def delete(self, request, *args, **kwargs):
        '''删除会议'''
        mid = request.data["mid"]
        print(mid)
        # 先删除membership的关系,不能直接删除会议
        try:
            models.Membership.objects.filter(meeting_id=mid).delete()
            models.Meeting.objects.filter(m_id=mid).delete()
            return JsonResponse({'msg': 'ok'})
        except:
            return JsonResponse({'msg': 'no ok'})


class Getmeeting(APIView):
    # 返回会议详细数据
    def get(self, request, *args, **kwargs):
        ret = {
            "data": None,
            "msg": "ok"
        }
        try:
            m_id = request.GET.get('mid')
            type = request.GET.get('type')
            print(m_id, type)
            # 返回单个具体会议详情
            if type == 'getmeetingdetail':
                obj = models.Meeting.objects.get(m_id=m_id)
                data = MeetingSerializer(obj).data
                ret["data"] = data
                return JsonResponse(ret)
            # 返回签到人数和报名人数
            elif type == 'getappend':
                data = []
                obj = models.Membership.objects.values('sign').filter(meeting_id=m_id)
                username = models.Meeting.objects.get(m_id=m_id).members.all().values("username")
                for k in username:
                    print(k)
                    data.append(k)
                ret["data"] = data
                return JsonResponse(ret)
            # 返回会议详情页信息
            elif type == 'getmeetingmember':
                # 获取用户id,用来判断用户是否已加入该会议
                u_id = request.GET.get('uid')
                # 获取报名该会议人数
                # 通过Meeting抓取到所有参加人员的信息
                m_append = models.Meeting.objects.get(m_id=m_id).members.all().count()
                # 已签到人数
                m_sgin = models.Membership.objects.filter(meeting_id=m_id, sign=1).count()
                # 获取会议信息
                meeting_obj = models.Meeting.objects.get(m_id=m_id)
                # 管理员登录密码,暂无

                # 会议标识符,用来生成会议邀请码
                flag = meeting_obj.msign_id

                # 判断用户是否参加该会议
                isappend = models.Membership.objects.get(user_id=u_id, meeting_id=m_id)
                if isappend:
                    isappend = '1'
                else:
                    isappend = '0'
                ret['data'] = {'m_append': m_append, "m_sign": m_sgin, 'flag': flag, 'append_flag': isappend}
                return JsonResponse(ret)
        except:
            ret['data'] = 'no ok'
            return JsonResponse(ret)

    # 声请加入
    def post(self, request, *args, **kwargs):
        ret = {
            "data": None,
            "msg": "200"
        }
        joindata = request.data
        type = joindata['type']
        u_id = joindata["u_id"]
        m_id = joindata['m_id']
        # 加入会议
        if type == 'join':
            try:
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
        # 退订会议
        elif type == 'back':
            models.Membership.objects.filter(user_id=u_id, meeting_id=m_id).delete()
            return JsonResponse(ret)


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
            # 如果type=sugnin,只取签到了的用户
            if request.GET.get('type') == 'signin':
                sign = models.Membership.objects.filter(meeting_id=m_id, sign=True)
                user = models.User.objects.filter(meeting__m_id=m_id)
                for s in sign:
                    for u in user:
                        if s.user_id == u.id:
                            cc.append(u.image)
                            break
                data = MembershipSerializer(sign, many=True).data
                return JsonResponse({'msg': 'ok', 'data': cc})
            # 返回签到用用户id
            sign = models.Membership.objects.filter(meeting_id=m_id)
            # 返回参与用户
            user = models.User.objects.filter(meeting__m_id=m_id)
            data0 = UserSerializer(user, many=True).data
            print(data0)
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

        ret = {
            "data": None,
            "msg": "200"
        }
        try:
            u_id = request.data['u_id']
            m_id = request.data['m_id']
            print(u_id, m_id)
            sign_member = models.Membership.objects.get(user_id=u_id, meeting_id=m_id)
            # 如果签到用户参加了会议
            if sign_member:
                # 判断是否签到
                if sign_member.sign:
                    sign_member.update(sign=True, sign_time=datetime.datetime.now())
                    ret['data'] = 'success'
                    return JsonResponse(ret)
                # 已签到
                else:
                    ret['data'] = 'completed'
                    return JsonResponse(ret)
            else:
                ret['data'] = 'fail'
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
            'msg': None,
            'data': []
        }
        try:
            vote_id = request.GET.get('vote_id')
            print(vote_id)
            if vote_id:  # 如果存在,只抓取相应的投票信息
                vote_theme = models.Votetheme.objects.get(theme_id=vote_id)
                vote_options = vote_theme.voteoption_set.all()
                options = VoteoptionSerializer(vote_options, many=True).data
                return JsonResponse({'msg': 'ok', 'data': options})
            m_id = request.GET.get('mid')
            print(m_id)
            vote_themes = models.Votetheme.objects.filter(meeting=m_id)
            # QuerySet对象可迭代,不为空,循环拿到theme_id
            if vote_themes:
                for vote_theme in vote_themes:
                    # 如果这两个放到外面,后面的值会覆盖前面的,因为内存是一样的,你修改了之后,大家就都一样了
                    r_data = {}  # 问题数据
                    choices = []  # 选项

                    question = VotethemeSerializer(vote_theme).data
                    r_data['question'] = question['theme_name']
                    r_data['time'] = question['vote_time']
                    r_data['flag'] = question['theme_id']
                    # 通过_set反向查询
                    vote_options = vote_theme.voteoption_set.all()
                    options = VoteoptionSerializer(vote_options, many=True).data
                    for i in options:
                        choices.append(i)
                    r_data['choices'] = choices
                    data['data'].append(r_data)
            data['msg'] = 'ok'
            return JsonResponse(data)

        except:
            return JsonResponse({'msg': 'no ok'})

    def post(self, request, *args, **kwargs):
        try:
            # 参与者投票
            if request.data['type'] == 'vote_append':
                uid = request.data['uid']
                oid = request.data['option_id']
                print(uid, oid)
                for k, v in oid.items():
                    print(k, v)
                    # 插入用户投票记录
                    vote = models.Voteuser.objects.filter(username=uid, votetheme_id=k)
                    if vote:
                        vote.update(answer=v)
                    else:
                        models.Voteuser.objects.create(username=uid, votetheme_id=k, answer=v)
                    # 更新投票总数
                    option = models.Voteoption.objects.filter(id=v)
                    if option[0].result:
                        result = int(option[0].result) + 1
                        option.update(result=result)
                    else:
                        option.update(result=1)

                return JsonResponse({'msg': 'ok'})

            # 投票发起
            else:
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
    parser_classes = [MultiPartParser, ]

    def readFile(self, filename, chunk_size=512):
        """
        缓冲流下载文件方法
        :param filename:
        :param chunk_size:
        :return:
        """
        with open(filename, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    def get(self, request, *args, **kwargs):
        '''请求文件列表'''
        role = request.GET.get('role')
        mid = request.GET.get('mid')
        # 是否为管理者
        if role == 'manage':
            try:
                document_all = models.Document.objects.filter(meeting=mid)
                data = DocumentSerializer(document_all, many=True).data
                return JsonResponse({'msg': 'ok', 'data': data})
            except:
                return JsonResponse({'msg': 'no ok'})
        # 是否为参加者
        elif role == 'append':
            try:
                document_all = models.Document.objects.filter(meeting=mid, Dstatus=1)
                data = DocumentSerializer(document_all, many=True).data
                return JsonResponse({'msg': 'ok', 'data': data})
            except:
                return JsonResponse({'msg': 'no ok'})
        elif role == 'download':
            """
            前端传来下载file的id，后端传给它下载地址
            """
            file_id = request.GET.get('file_id')
            doc = models.Document.objects.only('Dpath').filter(id=file_id, meeting=mid).first()

            if doc:
                doc_url = doc.Dpath
                doc_url = settings.BASE_DIR + doc_url
                print(doc_url)
                try:
                    res = FileResponse(self.readFile(doc_url))
                except Exception as e:
                    raise Http404('文件获取异常')
                file_end = doc_url.split('.')[-1]
                if not file_end:
                    raise Http404('文档路径出错')
                else:
                    file_end = file_end.lower()
                if file_end == "pdf":
                    res["Content-type"] = "application/pdf"
                elif file_end == "zip":
                    res["Content-type"] = "application/zip"
                elif file_end == "doc":
                    res["Content-type"] = "application/msword"
                elif file_end == "xls":
                    res["Content-type"] = "application/vnd.ms-excel"
                elif file_end == "docx":
                    res["Content-type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                elif file_end == "ppt":
                    res["Content-type"] = "application/vnd.ms-powerpoint"
                elif file_end == "pptx":
                    res["Content-type"] = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
                else:
                    raise Http404("文档格式不正确！")
                doc_filename = escape_uri_path(doc_url.split('/')[-1])
                # http1.1 中的规范
                # 设置为inline，会直接打开
                # attachment 浏览器会开始下载
                res["Content-Disposition"] = "attachment; filename*=UTF-8''{}".format(doc_filename)
                return res

            else:
                return JsonResponse({'msg': 'no ok'})

    def post(self, request, *args, **kwargs):
        # 保存路径
        base_dir = settings.BASE_DIR
        filepath = base_dir + '/static/'
        # 取得会议id
        mid = request.POST.get('mid')
        print(mid)
        print(request.FILES)
        # 生成当前时间
        timeYMD = datetime.datetime.now().strftime('%Y-%m-%d')

        # 取到文件
        files = request.FILES.get('filename')
        # 取得附带信息中文件在本地真正的文件名
        fname = request.POST.get('fname')
        print(fname)
        # 判断文件是否为空
        if files:
            # 获取前端上传时的临时文件名
            filename = files.name
            # 切割成数据库需要的索引名
            db_name = ('.').join(filename.split('.')[-2:]).lower()
            # 获取文件大小
            filesize = files.size
            # 获取文件后缀
            suffix = filename.split('.')[-1].lower()
            # 判断格式是否正确
            if suffix in ['ppt', 'pdf', 'doc', 'docx']:
                try:
                    with open(filepath + db_name, 'wb+') as f:
                        for chunk in files.chunks():  # 保证即使文件过大,也不会消耗很大内存
                            f.write(chunk)
                    # 存入数据库
                    db_path = '/static/' + db_name
                    print(type(fname), type(suffix), type(filesize), type(db_path), type(mid))
                    if fname:
                        models.Document.objects.create(Dname=fname, Dstyle=suffix, Dsize=filesize, Dpath=db_path,
                                                       meeting_id=mid)
                        return JsonResponse(
                            {'msg': 'ok',
                             'data': {'Dname': fname, 'Dstyle': suffix, 'Dtime': timeYMD, 'Dstatus': True}})
                    else:
                        models.Document.objects.create(Dname=db_name, Dstyle=suffix, Dsize=filesize, Dpath=db_path,
                                                       meeting_id=mid)
                        return JsonResponse(
                            {'msg': 'ok',
                             'data': {'Dname': db_name, 'Dstyle': suffix, 'Dtime': timeYMD, 'Dstatus': True,
                                      'Dsize': filesize}})


                except:
                    return JsonResponse({'msg': 'no ok'})
            else:
                return JsonResponse({'msg': '格式错误'})
        else:
            return JsonResponse({'msg': '发送失败'})

    def delete(self, request, *args, **kwargs):
        mid = request.GET.get('mid')
        # 要删除的文件id
        fid = request.GET.get('fid')
        try:
            del_file = models.Document.objects.filter(id=fid,meeting_id=mid)
            if del_file:
                c_file = del_file[0]
                c_file.delete()
                # 要删除文件的路径
                del_file_path = settings.BASE_DIR+ c_file.Dpath
                # os.remove可删除文件
                if os.path.exists(del_file_path):
                    os.remove(del_file_path)
                    return JsonResponse({'msg': 'ok'})
            else:

                return JsonResponse({'msg': 'no ok'})
        except:
            return JsonResponse({'msg': 'no ok'})


class Lottery(APIView):
    '''处理抽奖'''

    def get(self, request, *args, **kwargs):
        '''获取奖品列表'''
        mid = request.GET.get('mid')
        type = request.GET.get('type')
        if type == "getLotteryList":
            lottery_lists = models.Meeting.objects.get(m_id=mid).lottery_set.all()
            lottery_list = LotterySerializer(lottery_lists, many=True).data
            for i in lottery_list:
                i['award_name'] = eval(i['award_name'])
            return JsonResponse({'msg': 'ok', 'data': lottery_list})
        return JsonResponse({'msg': 'ok'})

    def post(self, request, *args, **kwargs):
        '''发起抽奖'''
        mid = request.data['mid']
        lotterys = request.data['lottrey']
        print(mid, lotterys)
        for lottery in lotterys:
            models.Lottery.objects.create(award_name=lottery['awards'], meeting_id=mid, award_leval=lottery['grade'])
        return JsonResponse({'msg': 'ok'})
