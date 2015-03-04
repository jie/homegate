#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang


import handlers
from core.module import BaseModule


class Module(BaseModule):

    module_name = 'homegate'
    template_prefix = 'homegate'

    handlers = [
        {
            'name': 'index',
            'url': None,
            'handler': handlers.IndexHandler
        },
        {
            'name': 'showcase',
            'url': 'showcase/(\w+)$',
            'handler': handlers.ShowcaseHandler
        },
        {
            'name': 'showcase_page',
            'url': 'showcase/(\w+)/(\d+)$',
            'handler': handlers.ShowcaseHandler
        },
        {
            'name': 'news',
            'url': 'p/(\w+)/(\d+)$',
            'handler': handlers.NewsHandler
        },
        {
            'name': 'reply',
            'url': 'news/reply$',
            'handler': handlers.NewsReplyHandler
        },
        {
            'name': 'fetch_replies',
            'url': 'news/replies$',
            'handler': handlers.NewsRepliesApiHandler
        },
    ]
