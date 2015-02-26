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
    ]
