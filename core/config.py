#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang


import os
import yaml
from tornado.util import ObjectDict


class Config(object):

    CONFIG_MAP = None
    ENV_NAME = 'HomeGateConfig'

    @classmethod
    def LoadYaml(cls, path):
        if not path:
            exit('[Config] path must not %s' % path)
        file_path = os.path.abspath(os.path.expanduser(path))

        try:
            yaml_map = yaml.load(open(file_path, 'r'))
            cls.CONFIG_MAP = ObjectDict(yaml_map)
        except Exception as e:
            exit("[Config] yaml format error: {}".format(e))

    @classmethod
    def LoadByEnv(cls, path=None):
        conf_path = os.getenv(cls.ENV_NAME)
        print(conf_path)
        if not conf_path:
            print('[Config] ENV %s NOT SET ...' % cls.ENV_NAME)
            print('[Config] TRY TO LOAD PATH BY CMD ...')
            if not path:
                exit('[Config] CMD ARGS --conf NOT SET ...')
            conf_path = path
        else:
            print('[Config] LOADING YAML [%s]' % conf_path)
        cls.LoadYaml(conf_path)

    def __getattr__(self, attr):
        return self.CONFIG_MAP[attr]

    def __setattr__(self, attr, value):
        raise Exception('setattr is not allowed')


if __name__ == '__main__':

    pass
