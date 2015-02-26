#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang

try:
    import cPickle as pickle
except ImportError as e:
    print(e)
    import pickle

import logging
from addict import Dict
from core.database import User
from pony.orm import db_session

logger = logging.getLogger(__name__)


class Session(object):

    def __init__(self, sessionid, userinfo):
        self.sessionid = sessionid
        self.userinfo = Dict(userinfo)
        self.user = self.get_user()

    @db_session
    def get_user(self):
        if self.userinfo:
            _user = User.get(id=self.userinfo.id)
        else:
            _user = Dict()
        logger.info('_user: %s' % _user)
        return _user


class SessionFactory(object):

    _prefix = 'homegate-session'
    _redis_client = None

    def get_key(self, sessionid):
        return '{prefix}-{key}'.format(prefix=self._prefix, key=sessionid)

    def get_session(self, sessionid, expire_sec=None):
        raw_session = self._redis_client.hgetall(self.get_key(sessionid))
        if not raw_session:
            return None

        if expire_sec:
            key = self.get_key(sessionid)
            self._redis_client.expire(key, expire_sec)

        session = Session(
            sessionid=raw_session['sessionid'],
            userinfo=pickle.loads(raw_session['userinfo'])
        )

        return session

    def expire(self, sessionid, expire_sec=3600):
        key = self.get_key(sessionid)
        self._redis_client.expire(key, expire_sec)

    def generate(self, sessionid, userinfo=None):
        _userinfo = userinfo if userinfo else {}
        userinfo_dumps = pickle.dumps(dict(_userinfo))
        sessioninfo = {
            'userinfo': userinfo_dumps,
            'sessionid': sessionid
        }
        self._redis_client.hmset(self.get_key(sessionid), sessioninfo)
        session = Session(sessionid=sessionid, userinfo=_userinfo)
        return session
