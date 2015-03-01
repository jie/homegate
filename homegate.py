#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang


"""
Usage:
    homegate.py [--config=<arg>][--port=<arg>]

Options:
    --config=<arg>  absolute yaml config config  [default: config/dev.yaml]
    --port=<arg>    server port                  [default: 8080]
"""

import os.path
from core.config import Config


def setup_logger(logger_config):
    import logging
    import logging.config
    logging.config.dictConfig(logger_config)
    logger = logging.getLogger(__name__)
    logger.info('homegate startup')


def setup_redis(redis_config):
    from coreutils.redtool.pool import RedisPool
    from core.session import SessionFactory
    redis_client = RedisPool.getClient(**redis_config)
    SessionFactory._redis_client = redis_client

    from coreutils.redtool.token import Token
    Token.RedisPool = RedisPool
    Token.RedisConfig = redis_config

    from core.cache import RedisCache
    RedisCache.redis_client = redis_client


def setup_qiniu(qiniu_config):
    import qiniu
    from util.qiniu_util import QiniuUtil
    QiniuUtil.BucketName = qiniu_config['bucket_name']
    QiniuUtil.BucketUrl = qiniu_config['bucket_url']
    QiniuUtil.Auth = qiniu.Auth(
        access_key=qiniu_config['access_key'],
        secret_key=qiniu_config['access_secret']
    )


def get_conf_by_cmd():
    from util.docopt import docopt
    ARGS = docopt(__doc__)
    print(ARGS)
    return ARGS['--config'], ARGS['--port']


def main():
    config_path, port = get_conf_by_cmd()
    Config.LoadByEnv(config_path)
    Config.basedir = os.path.dirname(__file__)
    config = Config()

    setup_logger(config.logger)
    setup_redis(config.redis)
    setup_qiniu(config.qiniu)
    from core.server import startup
    startup(config, port)


if __name__ == '__main__':
    main()
