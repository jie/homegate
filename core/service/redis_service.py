#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang


import json
from tornado.gen import coroutine, Return
from core.redis.async.pool import RedisPool


class EntityError(Exception):
    pass


class EntityNotFound(EntityError):
    pass


class RedisService(object):

    RedisPool = None
    selected_db = None
    redis_settings = {}

    def __init__(self, trace, entity_name, **kwargs):
        super(RedisService, self).__init__(trace, **kwargs)
        self.__entity_name = entity_name

    def genReturn(response={}):
        raise Return(response)

    def __get_entity_key(self, key):
        return "{name}-{key}".format(self.__entity_name, key)

    def get_redis_client(self):
        self.__redis_client = RedisPool.getClient(
            **self.redis_settings)
        self.__redis_client.select(self.selected_db)

    @coroutine
    def get_storage_by_key(self, entity_key):
        self._get_redis_client()
        entity_value = yield self.__redis_client.get(entity_key)
        self.genReture(entity_value)

    @coroutine
    def load(self, key):
        entity_key = self.__get_entity_key(key)
        __entity_map = yield self._get_storage_by_key(entity_key)
        if not __entity_map:
            raise EntityError()
        __entity_map = json.loads(__entity_map)
        self.genReture(self(__entity_map))

    @coroutine
    def save_entity(self, entity_key, store_string):
        self._get_redis_client()
        yield self.__redis_client.set(entity_key, store_string)
        self.genReture()

    @coroutine
    def save(self, key, entity):
        entity_key = self.__get_entity_key(key)
        __entity_string = json.dumps(entity)
        yield self._save_entity(entity_key, __entity_string)
        self.genReture()

    @coroutine
    def update(self, key, field_name, field_value):
        entity = self._load(key)
        setattr(entity, field_name, field_value)
        yield self._save(entity)
        self.genReturn()
