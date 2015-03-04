#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang

from math import ceil


class Pagination(object):

    def __init__(self, page, per_page, query):
        self.page = page
        self.per_page = per_page
        self.total_count = query.count()
        self.query = query
        self.get_items()

    def __repr__(self):
        return "page: %s, per_page: %s, total_count: %s" \
            % (self.page, self.per_page, self.total_count)

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    @property
    def next_num(self):
        _next_page = int(self.page) + 1
        return _next_page

    @property
    def prev_num(self):
        page = int(self.page)
        if page == 1:
            _prev_page = 1
        else:
            _prev_page = page - 1
        return _prev_page

    def is_current_page(self, page):
        return str(self.page) == str(page)

    def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

    def get_items(self):
        self.items = self.query.page(self.page, pagesize=self.per_page)
