import hashlib
import time


# 使用md5生成随机字符串
def md5(user):
    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


# 获取当前时间
def getcurrenttime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
