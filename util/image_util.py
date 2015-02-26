#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang


import os
import StringIO
import tempfile
from PIL import Image


class ImageUtil(object):

    def __init__(self, imagefile):
        self.image = Image.open(StringIO.StringIO(imagefile))
        self.size = self.image.size
        self.width = self.size[0]
        self.height = self.size[1]

    def crop_by_box(self, box):
        self.conver_box(box)
        frame_height = box.frame / (self.width / self.height)
        img = self.image.resize((box.frame, frame_height), Image.ANTIALIAS)
        crop_box = (box.x1, box.y1, box.x2, box.y2)
        return img.crop(crop_box)

    @staticmethod
    def save(image, size=(50, 50), mode="JPEG"):
        filename = tempfile.mktemp(prefix='hg-avatar-')
        image = image.resize(size, Image.ANTIALIAS)
        image.convert('RGB')
        image.save(filename, mode)
        return filename

    @staticmethod
    def delete(imagepath):
        os.unlink(imagepath)

    @staticmethod
    def conver_box(box):
        for k, v in box.items():
            box[k] = int(v)

if __name__ == '__main__':
    img = ImageUtil(file('/Users/zhouyang/Desktop/stevie.jpg', 'r'))
    img.image.crop((20, 20, 283, 283))
    img.save()
