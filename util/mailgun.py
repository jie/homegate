#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang


import logging
import tornado
from urllib import urlencode
from tornado import httpclient
from tornado.httputil import url_concat
from tornado.gen import coroutine, Return
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from core import error

logger = logging.getLogger('homegate.mailgun')


class Mailgun(object):

    connect_timeout = 30

    def __init__(self, addr, timeout=30, **kwargs):
        self.addr = addr
        self.timeout = timeout
        self.params = kwargs

    @coroutine
    def fetch(self, method, payloads):
        request_map = {
            'url': self.addr,
            'method': method,
            'request_timeout': self.timeout,
            'connect_timeout': self.connect_timeout,
            'auth_username': self.params.get('auth_username'),
            'auth_password': self.params.get('auth_password'),
            'auth_mode': self.params.get('auth_mode', 'basic')
        }

        if method.upper() == 'GET':
            request_map.update(url=url_concat(self.addr, payloads))
        else:
            request_map.update(body=urlencode(payloads))

        try:
            response = yield AsyncHTTPClient().fetch(HTTPRequest(**request_map))
            logger.info(response.body)
            if not response.error:
                data = tornado.escape.json_decode(response.body)
                raise Return(data)
            else:
                raise error.MailgunResponseError()
        except httpclient.HTTPError, e:
            logger.error(e)
            raise error.MailgunConnectError()


class EmailMessage(object):

    def __init__(self, sender, receivers):
        self.sender = sender
        self.receivers = receivers

    def get_verify_email(self, subject, token):
        url = "http://homegate.zhouyang.me/account/verify_email?token=%s" % token
        payloads = {
            'from': self.sender,
            'to': self.receivers,
            'subject': subject.encode('utf-8'),
            'text': url.encode('utf-8')
        }
        return payloads

    def get_reset_password_email(self, subject, token):
        url = "http://homegate.zhouyang.me/account/reset_password?token=%s" % token
        payloads = {
            'from': self.sender,
            'to': self.receivers,
            'subject': subject.encode('utf-8'),
            'text': url.encode('utf-8')
        }
        return payloads
