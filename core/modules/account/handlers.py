#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang


import logging
from tornado.gen import coroutine
from core import error
from core.database import User
from core.modules.base_handler import InterfaceBaseHandler, authenticated
from util.qiniu_util import QiniuUtil
from pony.orm import db_session
from core.helper import gen_sequence
from tornado.util import ObjectDict
from util.image_util import ImageUtil
from tornado.httpclient import AsyncHTTPClient
from coreutils.redtool.token import Token
from util.mailgun import EmailMessage


logger = logging.getLogger('homegate.account')


class SignupHandler(InterfaceBaseHandler):

    TemplatePath = 'signup.html'

    @coroutine
    def get(self):
        self.render()

    @coroutine
    @db_session
    def post_operate(self, *args, **kwargs):
        nickname = self.get_argument('nickname')
        sign_type = self.get_argument('sign_type', 0)
        email = self.get_argument('email', None)
        phone = self.get_argument('phone', None)
        password = self.get_argument('password')
        repeat_password = self.get_argument('repeat_password')

        if not password or not repeat_password:
            raise error.ArgumentError()

        if email is None and phone is None:
            raise error.ArgumentError()

        if password != repeat_password:
            raise error.RepeatPasswordError()

        sessionid, userinfo = User.signup(
            username=email if sign_type == 0 else phone,
            sign_type=sign_type,
            password=password,
            email=email,
            phone=phone,
            nickname=nickname,
            sessionid=self.current_user.sessionid
        )
        self.session_factory.generate(sessionid, userinfo)
        self.genReturn({'next': self.reverse_url('homegate.index')})


class SigninHandler(InterfaceBaseHandler):

    TemplatePath = 'signin.html'

    @coroutine
    def get(self):
        self.render()

    @coroutine
    @db_session
    def post_operate(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        _next = self.get_argument('next', None)
        user = User.GetByUsername(username=username)
        sessionid, userinfo = user.signin(
            password, self.current_user.sessionid)
        self.session_factory.generate(sessionid, userinfo)
        self.genReturn({'next': _next or self.reverse_url('homegate.index')})


class SignoutHandler(InterfaceBaseHandler):

    @coroutine
    @authenticated
    def get(self):
        next = self.get_argument('next', self.reverse_url('blog.index'))
        self.clear_cookie(self.cookies_name)
        self.session_factory.expire(self.current_user.sessionid, 1)
        self.redirect(next)


class SettingsHandler(InterfaceBaseHandler):

    TemplatePath = 'settings.html'

    @coroutine
    @authenticated
    def get(self):
        self.render()


class MessagesHandler(InterfaceBaseHandler):

    TemplatePath = 'messages.html'

    @coroutine
    @authenticated
    def get(self):
        self.render()


class MessageDetailHandler(InterfaceBaseHandler):

    TemplatePath = 'message_detail.html'

    @coroutine
    @authenticated
    def get(self):
        self.render()


class AvatarHandler(InterfaceBaseHandler):
    TemplatePath = 'avatar.html'

    @coroutine
    @authenticated
    def get(self):
        print self.current_user.user
        self.render()

    @coroutine
    @db_session
    @authenticated
    def post_operate(self, *args, **kwargs):
        sequence = gen_sequence(self.current_user.userinfo.id)
        quniu_util = QiniuUtil()
        key = "{name}.{ext}".format(name=sequence, ext='jpg')
        ret, info = quniu_util.upload_file(key, self.request.body)
        if info.status_code != 200:
            raise error.AvatarUploadError()
        user = User.UpdateAvatar(self.current_user.userinfo.id, sequence)
        avatar = user.get_avatar(sequence)
        self.genReturn({'avatar': avatar})


class TinyAvatarHandler(InterfaceBaseHandler):

    @coroutine
    @db_session
    @authenticated
    def post_operate(self, *args, **kwargs):
        box = ObjectDict()
        box.x1 = self.get_argument('x1')
        box.y1 = self.get_argument('y1')
        box.x2 = self.get_argument('x2')
        box.y2 = self.get_argument('y2')
        box.width = self.get_argument('width')
        box.height = self.get_argument('height')
        box.frame = self.get_argument('frame')
        tiny_avatar = yield self.get_avatar_from_qiniu()
        image_util = ImageUtil(tiny_avatar)
        image_croped = image_util.crop_by_box(box)
        imagepath = image_util.save(image_croped)
        sequence = gen_sequence(self.current_user.userinfo.id, prefix='t')
        key = "{name}.{ext}".format(name=sequence, ext='jpg')
        quniu_util = QiniuUtil()
        ret, info = quniu_util.upload_file(key, file(imagepath, 'r').read())
        image_util.delete(imagepath)
        if info.status_code != 200:
            raise error.AvatarUploadError()
        user = User.UpdateTinyAvatar(
            self.current_user.userinfo.id, sequence, box)
        tiny_avatar = user.get_tiny_avatar(sequence)
        self.genReturn({'tiny_avatar': tiny_avatar})

    @coroutine
    def get_avatar_from_qiniu(self):
        async_client = AsyncHTTPClient()
        response = yield async_client.fetch(self.current_user.user.get_avatar())
        if not response.error:
            self.genReturn(response.body)
        raise error.QiniuRequestError()


class SendVerifyEmailHandler(InterfaceBaseHandler):

    TokenName = 'homegate-verify-email'

    @coroutine
    @db_session
    @authenticated
    def post_operate(self, *args, **kwargs):
        email = self.get_argument('email')
        token = Token().generate(
            self.TokenName,
            maping={
                'email': email,
                'user_id': self.current_user.user.id
            },
            expire_sec=3600
        )
        email_message = EmailMessage(self.config.mailgun['postmaster'], email)
        subject = self.translate('Homegate Verify Email Request')
        payloads = email_message.get_verify_email(subject, token)
        yield self.mailgun.fetch('POST', payloads)
        self.genReturn({'message': self.translate('verify email send')})


class VerifyEmailHandler(InterfaceBaseHandler):

    TokenName = 'homegate-verify-email'

    @coroutine
    @db_session
    def get(self):
        token = self.get_argument('token')
        maping = Token().check(self.TokenName, token)

        if not maping:
            raise error.VerifyEmailTokenError()

        User.VerifyEmail(**maping)
        self.redirect_to('account.settings')


class UpdateUserinfoHandler(InterfaceBaseHandler):

    @coroutine
    @db_session
    def post_operate(self):
        # if not self.current_user.user.check_modify_date():
        #     raise error.ChecktModifyUserinfoDateError()
        nickname = self.get_argument('nickname')
        signature = self.get_argument('signature')
        gender = self.get_argument('gender')

        User.UpdateUserinfo(
            self.current_user.user,
            nickname=nickname,
            signature=signature,
            gender=gender
        )
        self.genReturn({'message': self.translate('userinfo updated')})


class ChangePasswordHandler(InterfaceBaseHandler):

    @coroutine
    @db_session
    def post_operate(self):
        password = self.get_argument('password')
        new_password = self.get_argument('new_password')
        repeat_password = self.get_argument('repeat_password')
        self.current_user.user.change_password(
            password,
            new_password,
            repeat_password
        )
        self.genReturn({'message': self.translate('user password changed')})


class ResetPasswordHandler(InterfaceBaseHandler):

    TokenName = 'homegate-reset-password'
    TemplatePath = 'reset_password.html'

    @coroutine
    @db_session
    def get(self):
        token = self.get_argument('token')
        maping = Token().check(self.TokenName, token)
        if not maping:
            raise error.TokenCheckError()
        self.render(token=token, email=maping['email'])

    @coroutine
    @db_session
    def post_operate(self):
        token = self.get_argument('token')
        password = self.get_argument('password')
        repeat_password = self.get_argument('repeat_password')
        maping = Token().check(self.TokenName, token)
        if not maping:
            raise error.TokenCheckError()

        user = User.GetByUsername(maping['email'])
        user.reset_password(
            password,
            repeat_password
        )
        Token().delete(self.TokenName, token)
        self.genReturn({'message': self.translate('user password reseted')})


class ForgetPasswordHandler(InterfaceBaseHandler):

    TokenName = 'homegate-reset-password'
    TemplatePath = 'forget_password.html'

    @coroutine
    @db_session
    def get(self):
        self.render()

    @coroutine
    @db_session
    def post_operate(self):
        email = self.get_argument('email')
        token = Token().generate(
            self.TokenName,
            maping={
                'email': email
            },
            expire_sec=3600
        )
        email_message = EmailMessage(self.config.mailgun['postmaster'], email)
        subject = self.translate('Homegate Reset Password Request')
        payloads = email_message.get_reset_password_email(subject, token)
        yield self.mailgun.fetch('POST', payloads)
        self.genReturn({'message': self.translate('reset password email send')})
