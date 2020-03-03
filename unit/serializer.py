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
        fields = ('u_id', 'token', 'username', 'image')