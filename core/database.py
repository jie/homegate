#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang

from datetime import datetime
from pony.orm import *
from core.config import Config
from core.models.user import UserMixin

config = Config()

db = Database(
    "mysql",
    host=config.mysql['host'],
    port=config.mysql['port'],
    user=config.mysql['user'],
    passwd=config.mysql['passwd'],
    db=config.mysql['db'],
    charset="utf8"
)


class User(db.Entity, UserMixin):
    id = PrimaryKey(int, auto=True)
    sign_type = Required(int)
    username = Required(str, 32, unique=True)
    password = Required(str, 40)
    nickname = Optional(unicode, 12, unique=True, nullable=True)
    email = Optional(str, 32, nullable=True)
    phone = Optional(str, 16, nullable=True)
    avatar = Optional(str, unique=True, nullable=True)
    tiny_avatar = Optional(str, unique=True, nullable=True)
    avatar_frame = Optional(str, nullable=True)
    create_at = Required(datetime)
    update_at = Required(datetime)
    login_at = Optional(datetime)
    is_enable = Required(int, default=1)
    status = Required(int, default=0)
    signature = Optional(str, nullable=True)
    gender = Optional(str, nullable=True)
    userinfo_modified = Optional(datetime, nullable=True)


# class Inbox(db.Entity):
#     pass


# class Article(db.Entity):
#     pass

sql_debug(False)
db.generate_mapping()
