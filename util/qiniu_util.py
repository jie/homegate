#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang


import logging
import qiniu

logger = logging.getLogger(__name__)


class QiniuError(Exception):
    pass


class QiniuUtil(object):

    Auth = None
    BucketName = None
    BucketUrl = None

    def upload_file(self, key, filedata, mime_type='image/jpeg', check_crc=True, bucket_name=None):

        token = self.Auth.upload_token(bucket_name or self.BucketName)
        ret, info = qiniu.put_data(
            token, key, filedata, mime_type=mime_type, check_crc=check_crc)

        try:
            assert ret['key'] == key
        except AssertionError:
            raise QiniuError()
        print 'qiniu res: %s' % ret
        return ret, info

    @classmethod
    def GetURL(self, name, ext):
        return "{url}{name}.{ext}".format(url=self.BucketUrl, name=name, ext=ext)
