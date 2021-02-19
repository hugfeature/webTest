# author:丑牛
# datetime:2021/1/11 15:30
import datetime
import time
from functools import wraps


def timestamp():
    """时间戳"""
    return time.time()


def sleep(seconds=1):
    """
    进程休眠时间
    :param seconds:
    :return:
    """
    time.sleep(seconds)


def dt_strftime(fmt="%Y-%m-%d"):
    """
    datetime格式化时间
    :param fmt "%Y%m%d %H%M%S
    :return: 返回一定时间格式
    """
    return datetime.datetime.now().strftime(fmt)


def running_time(func):
    """函数运行时间"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = timestamp()
        res = func(*args, **kwargs)
        print("校验元素done！用时%.3f秒！" % (timestamp() - start))
        return res

    return wrapper
