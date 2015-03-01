#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang

try:
    import cPickle as pickle
except ImportError as e:
    print(e)
    import pickle


import functools


class RedisCache(object):

    _prefix = 'homegate-cache'
    redis_client = None

    def get_key(self, key):
        return '{prefix}-{key}'.format(prefix=self._prefix, key=key)


def cached(cache_key=None):
    def outer_wrapper(method):

        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            redis_cache = RedisCache()
            key = redis_cache.get_key(cache_key)
            cached_data = redis_cache.redis_client.get(key)
            print cached_data
            if not cached_data:
                data = method(*args, **kwargs)
                redis_cache.redis_client.set(key, pickle.dumps(data))
                redis_cache.redis_client.expire(key, 300)
            else:
                data = pickle.loads(cached_data)
                print data
            return data

        return wrapper
    return outer_wrapper
