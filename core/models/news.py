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

logger = logging.getLogger('homegate.models.news')


class NewsMixin(BaseModelMixin):

    @classmethod
    def fetchBySite(cls, site, limit=10):
        return cls.select(lambda r: r.site == site).order_by(lambda r: pony.orm.desc(r.create_at))[:]

    @classmethod
    @cached(cache_key='homepage')
    @pony.orm.db_session
    def fetchHomepage(cls):
        hacknews_items = cls.fetchBySite('hacknews')
        jobs_items = cls.fetchBySite('jobs')
        games_items = cls.fetchBySite('tgbus')

        records = {
            'hacknews': hacknews_items,
            'jobs': jobs_items,
            'games': games_items
        }

        return records
