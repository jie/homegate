#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang


import logging
import time
from tornado.log import LogFormatter


class IHTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):

    def shouldRollover(self, record):
        now = time.time()
        t = int(now)
        if t >= self.rolloverAt:
            return 1
        elif (now / self.interval) > (self.rolloverAt / self.interval):
            return 1
        # print "No need to rollover: %d, %d" % (t, self.rolloverAt)
        return 0


class IHFormatter(logging.Formatter):

    def format(self, record):
        if not hasattr(record, 'trace'):
            record.trace = '-'
        return super(IHFormatter, self).format(record)


class ColoredConsoleFormatter(LogFormatter):

    def format(self, record):
        if not hasattr(record, 'trace'):
            record.trace = '-'
        return super(ColoredConsoleFormatter, self).format(record)
