"""序列化类"""
from rest_framework import serializers
# from userapi import models
# 自己写字符匹配
from userapi import models


class UserSerializers(serializers.Serializer):
    # 数字
    id = serializers.IntegerField()
    # 字符串
    name = serializers.CharField()
    # 带选择的
    sex = serializers.CharField(source="get_sex_display")


# 调用restframework的类来匹配,简化操作
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Meeting
        # fields要传入元组,如果一个数据时,记得带上逗号啊
        fields = '__all__'
class MembershipSerializer(serializers.ModelSerializer):
    # 解决日期带T
    sign_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = models.Membership
        # fields要传入元组,如果一个数据时,记得带上逗号啊
        fields = ('sign','sign_time')
class VotethemeSerializer(serializers.ModelSerializer):
    # 解决日期带T
    vote_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = models.Votetheme
        fields = '__all__'
class VoteoptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Voteoption
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    Dtime = serializers.DateTimeField(format='%Y-%m-%d')

    class Meta:
        model = models.Document
        fields = '__all__'

class LotterySerializer(serializers.ModelSerializer):
    '''抽奖表序列化'''
    award_time = serializers.DateTimeField(format='%Y-%m-%d')

    class Meta:
        model = models.Lottery
        fields = '__all__'
