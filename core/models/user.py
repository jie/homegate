#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang

import time
import logging
from uuid import uuid4
from hashlib import sha1
from datetime import datetime
from core import const
from core import error
from util.qiniu_util import QiniuUtil
from pony.orm import ObjectNotFound, flush, commit, db_session
from addict import Dict
from mixin import BaseModelMixin

logger = logging.getLogger('homegate.models.user')


class UserMixin(BaseModelMixin):

    @staticmethod
    def generate_password(password, create_at):
        s = sha1(password)
        s.update(str(time.mktime(create_at.timetuple())))
        return s.hexdigest()

    @staticmethod
    def generate_sessionid():
        return str(uuid4())

    @classmethod
    def signup(cls, nickname, username, password, sign_type, sessionid, **kwargs):

        try:
            user = cls.get(username=username)
        except ObjectNotFound:
            pass

        if user:
            raise error.UsernameExisted(username=username)

        create_at = datetime.now()
        update_at = datetime.now()
        user = cls(
            nickname=nickname,
            username=username,
            sign_type=sign_type,
            is_enable=const.UserEnable.OK,
            status=const.UserStatus.OK,
            password=cls.generate_password(password, create_at),
            email=kwargs.get('email'),
            phone=kwargs.get('phone'),
            create_at=create_at,
            update_at=update_at,
        )

        flush()
        commit()
        return user.signin(password, sessionid)

    def signin(self, password, sessionid=None, **kwargs):
        input_password = self.generate_password(password, self.create_at)
        if self.password != input_password:
            kwargs['callback'](self.username, kwargs['password_check_count'])
            raise error.VerifyPasswordError(username=self.username)

        self.login_at = datetime.now()
        flush()

        userinfo = dict(
            id=self.id,
            nickname=self.nickname,
            username=self.username,
            avatar=self.avatar,
            tiny_avatar=self.tiny_avatar
        )
        userinfo = Dict(userinfo)
        return sessionid or self.generate_sessionid(), userinfo

    @classmethod
    def UpdateAvatar(cls, id, name):
        user = cls.get(id=id)
        user.avatar = name
        flush()
        commit()
        return user

    @classmethod
    @db_session
    def UpdateTinyAvatar(cls, id, name, box):
        user = cls.get(id=id)
        user.tiny_avatar = name
        user.avatar_frame = ','.join(
            (str(box.x1), str(box.y1), str(box.x2), str(box.y2)))
        flush()
        commit()
        return user

    @classmethod
    def GetByUsername(cls, username):
        try:
            user = cls.get(username=username)
        except ObjectNotFound:
            raise error.UserNotFound(username=username)
        return user

    @classmethod
    @db_session
    def VerifyEmail(cls, email, user_id, **kwargs):

        try:
            existed = cls.get(username=email)
        except ObjectNotFound:
            existed = None

        if existed:
            raise error.UsernameExisted(username=email)

        try:
            user = cls.get(id=user_id)
            user.email = email
            user.username = email
            user.status = const.UserStatus.ACTIVED
            flush()
            commit()
        except ObjectNotFound:
            raise error.UserNotFound(email=email)
        return user

    def get_avatar(self, name=None):
        return QiniuUtil.GetURL(name or self.avatar, 'jpg')

    def get_tiny_avatar(self, name=None):
        return QiniuUtil.GetURL(name or self.tiny_avatar, 'jpg')

    def get_frame(self):
        frame = Dict()
        if self.avatar_frame:
            _frame = self.avatar_frame.split(',')
            frame.x1 = _frame[0]
            frame.y1 = _frame[1]
            frame.x2 = _frame[2]
            frame.y2 = _frame[3]
        return frame

    def check_modify_date(self):
        return ((datetime.now() - self.userinfo_modified).days > 7) if self.userinfo_modified else True

    @classmethod
    def UpdateUserinfo(cls, user, nickname, signature, gender, **kwargs):
        if user.nickname != nickname:
            try:
                existed = cls.get(nickname=nickname)
            except ObjectNotFound:
                existed = None

            if existed:
                raise error.UsernameExisted(nickname=nickname)

        user.nickname = nickname
        user.signature = signature
        user.gender = gender
        user.userinfo_modified = datetime.now()
        flush()
        commit()

    def change_password(self, password, new_password, repeat_password, **kwargs):
        if self.password != self.generate_password(password, self.create_at):
            raise error.VerifyPasswordError()

        if new_password != repeat_password:
            raise error.RepeatPasswordError()

        self.password = self.generate_password(new_password, self.create_at)
        flush()
        commit()

    def reset_password(self, password, repeat_password, **kwargs):
        if password != repeat_password:
            raise error.RepeatPasswordError()

        self.password = self.generate_password(password, self.create_at)
        flush()
        commit()
