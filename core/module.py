#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang


import os.path
from tornado.web import url, StaticFileHandler


class ModuleMeta(type):

    def __new__(mcs, name, bases, attrs):
        HANDLERS = []

        if 'handlers' in attrs and 'template_prefix' in attrs:
            for handler in attrs['handlers']:
                handlerName = "%s.%s" % (attrs['module_name'], handler['name'])
                handlerCls = handler['handler']

                if handler['url']:
                    handlerUrl = r"/%s/%s" % (attrs['module_name'], handler['url'])
                else:
                    handlerUrl = r"/$"
                if getattr(handlerCls, 'TemplatePath'):
                    handlerCls.TemplatePath = os.path.join(
                        attrs['template_prefix'],
                        handlerCls.TemplatePath
                    )
                handlerCls.ModuleName = attrs['module_name']
                handlerCls.PageName = handler['name']
                handlerCls.ReverseName = handlerName
                HANDLERS.append(url(handlerUrl, handlerCls, name=handlerName))

        klass = type.__new__(mcs, name, bases, attrs)
        klass.Handlers.extend(HANDLERS)
        return klass


class BaseModule(object):

    __metaclass__ = ModuleMeta

    Handlers = [
        url(r'/static/(.*)', StaticFileHandler),
    ]
