#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang


import handlers
from core.module import BaseModule


class Module(BaseModule):

    module_name = 'forum'
    template_prefix = 'forum'

    handlers = [
        {
            'name': 'index',
            'url': 'f/(.*)$',
            'handler': handlers.ForumHandler
        },
        {
            'name': 'p/(.*)$/(.*)$',
            'url': '',
            'handler': handlers.ArticleHandler
        }
    ]
