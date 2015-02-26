#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang


import random
from uuid import uuid1
from captcha.image import ImageCaptcha


image = ImageCaptcha()


class Captcha(object):

    def generate(self):

        code = str(random.randint(100000, 999999))
        response = {
            'code': code,
            'data': image.write(code, '%s.png' % uuid1().get_hex()[:10])
        }
        return response
