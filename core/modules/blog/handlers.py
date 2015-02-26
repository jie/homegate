#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang


from tornado.gen import coroutine
from core.modules.base_handler import InterfaceBaseHandler


class BlogIndexHandler(InterfaceBaseHandler):

    TemplatePath = 'blog.html'

    @coroutine
    def get(self):
        print dir(self.current_user)
        self.render()


class PostHandler(InterfaceBaseHandler):

    TemplatePath = 'post.html'

    @coroutine
    def get(self):
        print dir(self.current_user)
        self.render()
