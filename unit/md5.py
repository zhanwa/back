import hashlib
import time


from urllib import request


def md5(user):
    # 使用md5生成随机字符串

    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


# 获取当前时间
def getcurrenttime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

# 获取网络图片
def getInetpicture(url):
    request.urlretrieve(url,'media/avatarImg')

#响应返回基本格式
def rep():
    data = {'msg':'ok','data':None}
    return data