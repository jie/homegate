#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang


import json
import logging
import urlparse
import functools
import user_agents
from urllib import urlencode
from uuid import uuid4
from tornado import locale
from tornado.util import ObjectDict
from tornado.web import RequestHandler, HTTPError
from tornado.gen import coroutine, Return
from core.helper import TraceAbleObject
from core import error


logger = logging.getLogger('homegate')


class InterfaceBaseHandler(RequestHandler, TraceAbleObject):

    TemplatePath = None

    def __init__(self, *args, **kwargs):
        super(InterfaceBaseHandler, self).__init__(*args, **kwargs)
        self.make_trace()

    def genReturn(self, response={}):
        raise Return(response)

    def is_active_page(self, reverse_name, second_name=None):
        return 'active' if reverse_name == self.ReverseName else ''

    def is_active_showcase(self, second_name, showcase):
        return 'active' if second_name == showcase else ''

    def initialize(self, *args, **kwargs):
        self.cookies_name = self.config.interface['cookie']['name']
        cookie = self.get_secure_cookie(self.cookies_name)

        self.cookie_data = ObjectDict(
            json.loads(cookie)) if cookie else ObjectDict()

    def check_browser(self):
        useragent = user_agents.parse(self.request.header.user_agent)
        if useragent.browser.family == 'Microsoft IE' and int(useragent.browser.version) < 9:
            message = self.translate('Microsoft IE is not supported')
            raise error.CheckBrowerError(message)

    def update_cookies(self, **kwargs):
        self.cookie_data.update(**kwargs)
        self.set_secure_cookie(
            self.cookies_name,
            json.dumps(self.cookie_data)
        )

    @property
    def config(self):
        return self.application.settings['config']

    @property
    def env(self):
        return self.application._jinja_env

    @property
    def session_factory(self):
        return self.application.session_factory

    @property
    def mailgun(self):
        return self.application.settings['mailgun']

    def _render(self, template, **kwargs):
        self.env.globals.update(
            translate=self.translate,
            reverse_url=self.reverse_url,
            current_user=self.current_user,
            is_active_page=self.is_active_page,
            is_active_showcase=self.is_active_showcase,
            config=self.config
        )

        template = self.env.get_template(template)
        self.env.globals['static_url'] = self.static_url
        self.write(template.render(kwargs))

    def render(self, **kwargs):
        self._render(self.TemplatePath, **kwargs)

    def get_current_user(self):
        sessionid = self.cookie_data.get('sessionid')
        if not sessionid:
            session = self.create_session()
        else:
            session = self.session_factory.get_session(
                sessionid, expire_sec=3600)

            if not session:
                self.clear_cookie(self.cookies_name)
                session = self.create_session()

        self.session = session
        return session

    def create_session(self):
        sessionid = uuid4().get_hex()
        session = self.session_factory.generate(sessionid)
        self.set_secure_cookie(
            self.cookies_name,
            json.dumps({'sessionid': sessionid})
        )
        return session

    def get_login_url(self):
        return self.reverse_url('account.signin')

    def get_user_locale(self):
        return locale.get(self.cookie_data.get('locale', 'zh_CN'))

    def translate(self, text):
        return self.get_user_locale().translate(text)

    def _get_argument(self, name, default, source, strip=True):
        args = self._get_arguments(name, source, strip=strip)
        if not args:
            print 'default is self._ARG_DEFAULT:', (default is self._ARG_DEFAULT)
            if default is self._ARG_DEFAULT:
                raise error.ArgumentError(name=name)
            return default
        return args[-1]

    def redirect_to(self, reverse_name, **kwargs):
        self.redirect(self.reverse_url(reverse_name, **kwargs))

    def output(self, response):
        response['data']['trace'] = self.trace
        self._chunk = json.dumps(response)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(self._chunk)
        self.finish()

    def make_response(self, data, **kwargs):
        return {
            'success': True,
            'message': data.get('message') or 'ok',
            'data': data
        }

    def make_error(self, error, **kwargs):
        return {
            'success': False,
            'message': error.msg,
            'data': {}
        }

    def make_exception(self, **kwargs):
        return {
            'success': False,
            'message': 'system_error',
            'data': {}
        }

    @coroutine
    def handle(self, *args, **kwargs):
        try:
            data = yield self.post_operate(*args, **kwargs)
            response = self.make_response(data)
        except error.LogicError, e:
            logger.error(e, extra={'trace': self.trace})
            response = self.make_error(e)
        except error.SysError, e:
            logger.error(e, exc_info=True, extra={'trace': self.trace})
            response = self.make_error(e)
        except Exception, e:
            logger.exception(e, extra={'trace': self.trace})
            response = self.make_exception()
        self.output(response)

    def post(self, *args, **kwargs):
        return self.handle(*args, **kwargs)


def authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user or not self.current_user.userinfo:
            if self.request.method in ("GET", "HEAD"):
                url = self.get_login_url()
                if "?" not in url:
                    if urlparse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper
