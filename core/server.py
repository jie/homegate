#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang


import os.path
import tornado
import tornado.web
import tornado.ioloop
import tornado.httpserver
from util.mailgun import Mailgun
from core.module import BaseModule
from core.application import CoreApplication
from core.modules import *


def startup(config, port):
    locale_path = os.path.join(config.basedir, config.interface['locale'])
    static_path = os.path.join(config.basedir, config.interface['static'])
    template_path = os.path.join(config.basedir, config.interface['template'])
    mailgun = Mailgun(
        addr=config.mailgun['addr'],
        auth_username=config.mailgun['auth_username'],
        auth_password=config.mailgun['auth_password'],
        timeout=config.mailgun['timeout']
    )
    settings = {
        'config': config,
        'debug': config.server['debug'],
        'static_path': static_path,
        'locale_path': locale_path,
        'template_path': template_path,
        'cookie_secret': config.interface['cookie']['secret'],
        'mailgun': mailgun
    }

    application = CoreApplication(BaseModule.Handlers, **settings)
    server = tornado.httpserver.HTTPServer(application)
    tornado.locale.load_translations(locale_path)
    server.listen(int(port))
    tornado.ioloop.IOLoop.configure('tornado.platform.asyncio.AsyncIOLoop')
    tornado.ioloop.IOLoop.instance().start()
