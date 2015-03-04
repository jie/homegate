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
from core.cache import cached
from util.pagination import Pagination

logger = logging.getLogger('homegate.models.news')


class NewsMixin(BaseModelMixin):

    def get_replies(self, reverse=True):
        return sorted(self.replies, reverse=reverse, key=lambda k: k.create_at)

    @property
    def summary(self):
        return self.description or "%s [...]" % self.content[:60] if self.content else ''

    @property
    def tags(self):
        return self.tag.split(',') if self.tag else []

    @classmethod
    def getById(cls, item_id):
        return cls.get(id=item_id)

    @classmethod
    def fetchByShowcase(cls, showcase, limit=10):
        return cls.select(lambda r: r.showcase == showcase).order_by(lambda r: pony.orm.desc(r.create_at))[:limit]

    @classmethod
    def fetchByShowcasePage(cls, showcase, page, limit=10):
        records = cls.select(lambda r: r.showcase == showcase).order_by(lambda r: pony.orm.desc(r.create_at))
        pagination = Pagination(page, limit, records)
        return pagination

    @classmethod
    @cached(cache_key='homepage')
    @pony.orm.db_session
    def fetchHomepage(cls):
        hacknews_items = cls.fetchByShowcase('news')
        acgn_items = cls.fetchByShowcase('acgn')
        coding_items = cls.fetchByShowcase('coding')

        records = {
            'news': hacknews_items,
            'acgn': acgn_items,
            'coding': coding_items
        }

        return records
