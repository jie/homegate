#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang


from tornado.gen import coroutine
from core.modules.base_handler import InterfaceBaseHandler


class ForumHandler(InterfaceBaseHandler):

    TemplatePath = 'forum.html'

    @coroutine
    def get(self):
        print dir(self.current_user)
        self.render()


class ArticleHandler(InterfaceBaseHandler):

    TemplatePath = 'article.html'

    @coroutine
    def get(self):
        print dir(self.current_user)
        self.render()
