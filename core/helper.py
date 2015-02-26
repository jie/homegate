#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang


import functools
from uuid import uuid1
# from tornado.gen import coroutine
from core import error
from datetime import datetime
from json import JSONEncoder
# from utils.concurrent.futures import ThreadPoolExecutor
# thread_pool = ThreadPoolExecutor(30)


class TraceAbleObject(object):

    def make_trace(self, trace=None, **kwargs):
        self.trace = trace if trace else 'TRACE:' + str(uuid1()).upper()


# @coroutine
# def coroutine_call(func, args):
#     '''
#     使用线程方式无阻塞调用函数
#     '''
#     yield thread_pool.submit(func, args)


def authenticated(method):

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user and not self.current_user.userinfo:
            raise error.SessionRequiredError()
        return method(self, *args, **kwargs)
    return wrapper


class MyJsonEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


def gen_sequence(pk, prefix='u', suffix=None):
    sequence = prefix + ('000000000' + str(pk))[-8:]
    if suffix is None:
        sequence = sequence + datetime.now().strftime('%Y%m%d%H%M%S')
    else:
        sequence = sequence + suffix
    return sequence

if __name__ == '__main__':
    t = TraceAbleObject()
    t.make_trace()
    print t.trace
