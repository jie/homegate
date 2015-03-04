#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang

import logging
# from uuid import uuid4
# from hashlib import sha1
# from datetime import datetime
# from core import const
# from core import error
import pony.orm
from mixin import BaseModelMixin
from util.pagination import Pagination
# from core.cache import cached
# from util.pagination import Pagination

logger = logging.getLogger('homegate.models.reply')


class ReplyMixin(BaseModelMixin):

    @classmethod
    def getById(cls, item_id):
        return cls.get(id=item_id)

    @classmethod
    def appendReply(cls, news_id, markdown, user_id):
        record = cls(news=news_id, content=markdown, user=user_id)
        pony.orm.flush()
        pony.orm.commit()
        return record

    @classmethod
    def fetchReplies(cls, news_id, page=1, limit=20, **kwargs):
        records = cls.select(lambda r: r.news.id == int(news_id)).order_by(
            lambda r: pony.orm.desc(r.create_at)
        )
        pagination = Pagination(page, limit, records)
        return pagination

    @staticmethod
    def renderReplies(items):
        replies = []
        tpl = """
            <div class="comment">
                <a class="avatar">
                    <img src="{avatar}">
                </a>
                <div class="content">
                    <a class="author">{nickname}</a>
                    <div class="metadata">
                        <span class="date">{create_at}</span>
                    </div>
                    <div class="text">
                        {content}
                    </div>
                </div>
            </div>
        """

        for item in items:
            kwargs = {
                'avatar': item.user.get_avatar(),
                'nickname': item.user.nickname.encode('utf-8'),
                'create_at': item.create_at.strftime("%Y-%m-%d %H:%M:%S"),
                'content': item.content.encode('utf-8')
            }
            replies.append(tpl.format(**kwargs))
        return replies
