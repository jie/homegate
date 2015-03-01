#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang


import logging
from tornado.gen import coroutine
from core.modules.base_handler import InterfaceBaseHandler
from core.database import News
import pony.orm

logger = logging.getLogger('homegate.homegate')


class IndexHandler(InterfaceBaseHandler):

    TemplatePath = 'index.html'

    @coroutine
    @pony.orm.db_session
    def get(self):
        homepage = News.fetchHomepage()
        self.render(
            hacknews=homepage['hacknews'][:10], 
            jobs=homepage['jobs'][:10],
            games=homepage['games'][:10]
        )
