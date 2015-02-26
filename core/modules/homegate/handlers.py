#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang


import logging
from tornado.gen import coroutine
from core.modules.base_handler import InterfaceBaseHandler


logger = logging.getLogger('homegate.homegate')


class IndexHandler(InterfaceBaseHandler):

    TemplatePath = 'index.html'

    @coroutine
    def get(self):
        print self.current_user
        print self.current_user.sessionid
        print self.current_user.userinfo
        print type(self.current_user.userinfo)
        self.render()
