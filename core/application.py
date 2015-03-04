#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang

import logging
import tornado.web
from core.session import SessionFactory
from jinja2 import Environment, FileSystemLoader
logger = logging.getLogger(__name__)


class CoreApplication(tornado.web.Application):

    def __init__(self, *args, **kwargs):
        super(CoreApplication, self).__init__(*args, **kwargs)
        self._jinja_env = Environment(
            loader=FileSystemLoader(kwargs['template_path']),
            auto_reload=kwargs.get('debug', True),
            autoescape=False,
            extensions=['jinja2.ext.do']
        )

        self.session_factory = SessionFactory()

    def log_request(self, handler):
        """
        Rewrite tornado web log, add trace
        """
        if "log_function" in self.settings:
            self.settings["log_function"](handler)
            return
        if handler.get_status() < 400:
            log_method = logger.info
        elif handler.get_status() < 500:
            log_method = logger.warning
        else:
            log_method = logger.error
        request_time = 1000.0 * handler.request.request_time()

        if hasattr(handler, 'trace'):
            log_method("[REQ] %d %s %.2fms" % (
                handler.get_status(),
                handler._request_summary(),
                request_time),
                extra={'trace': handler.trace}
            )
        else:
            log_method("[REQ] %d %s %.2fms" % (
                handler.get_status(),
                handler._request_summary(),
                request_time)
            )
