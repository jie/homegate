#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang


import handlers
from core.module import BaseModule


class Module(BaseModule):

    module_name = 'blog'
    template_prefix = 'blog'

    handlers = [
        {
            'name': 'index',
            'url': 'blog',
            'handler': handlers.BlogIndexHandler
        },
        {
            'name': 'post',
            'url': 'post$',
            'handler': handlers.PostHandler
        }
    ]
