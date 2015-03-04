#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang


import logging
import pony.orm
from tornado.gen import coroutine
from core import error
from core.modules.base_handler import InterfaceBaseHandler
from core.database import News, Reply
from coreutils.redtool.token import Token
# from core import error


logger = logging.getLogger('homegate.homegate')


class IndexHandler(InterfaceBaseHandler):

    TemplatePath = 'index.html'

    @coroutine
    @pony.orm.db_session
    def get(self):
        items = News.fetchHomepage()
        self.render(items=items)


class ShowcaseHandler(InterfaceBaseHandler):

    TemplatePath = 'showcase.html'

    @coroutine
    @pony.orm.db_session
    def get(self, showcase, page=1, *args, **kwargs):
        page = 1 if page is None else int(page)
        pagination = News.fetchByShowcasePage(showcase, page, limit=20)
        self.render(showcase=showcase, pagination=pagination)


class NewsHandler(InterfaceBaseHandler):

    TemplatePath = 'news.html'

    @coroutine
    @pony.orm.db_session
    def get(self, showcase, identity):
        item = News.getById(identity)
        self.render(item=item, showcase=showcase)


class NewsReplyHandler(InterfaceBaseHandler):

    RepliesPageSize = 20
    TokenName = 'homegate-reply'

    @coroutine
    @pony.orm.db_session
    def post_operate(self, *args, **kwargs):
        if not self.current_user.user.tiny_avatar:
            raise error.UserNoTinyAvatarError()

        self.check_reply_token(self.current_user.user.id)

        news_id = self.get_argument('news_id')
        markdown = self.get_argument('markdown')
        reply = Reply.appendReply(
            news_id=news_id,
            markdown=markdown,
            user_id=self.current_user.user.id
        )

        replies = Reply.renderReplies([reply])
        response = {
            'replies': replies,
            'page': 1,
            'content_page': 1,
            'page_size': 20,
        }
        self.set_reply_token(self.current_user.user.id)
        self.genReturn(response)

    def check_reply_token(self, user_id):
        token = Token().check(self.TokenName, str(user_id))
        if token:
            raise error.ReplyRestrictError()

    def set_reply_token(self, user_id):
        token = Token().hset(
            self.TokenName,
            str(user_id),
            maping={'user_id': user_id},
            expire_sec=50
        )
        return token


class NewsRepliesApiHandler(InterfaceBaseHandler):

    RepliesPageSize = 20

    @coroutine
    @pony.orm.db_session
    def post_operate(self, *args, **kwargs):
        news_id = self.get_argument('news_id')
        page = self.get_argument('page', 1)
        content_page = self.get_argument('content_page', 1)
        page = int(page)
        content_page = int(content_page)
        pagination = Reply.fetchReplies(news_id=news_id)
        response = {
            'replies': Reply.renderReplies(pagination.items),
            'page': page,
            'content_page': content_page,
            'page_size': self.RepliesPageSize
        }
        self.genReturn(response)
