#!/usr/bin/env python
# encoding: utf-8
# @author: ZhouYang


import fabric

host = '192.168.2.156'
path = '/usr/api-root/webapps/mswallet'


def output(color, info, sep="="):
    func = getattr(fabric.color, color)
    print func(sep * 30 + info + sep * 30)


@fabric.api.hosts(host)
def reload(path=path):
    """ Restarting
    """
    with fabric.api.cd(path):
        output('green', 'stoping mswallet')
        fabric.api.run('sh shutdown.sh')
        output('green', 'starting mswallet')
        fabric.api.run('sh startup.sh')
        output('green', 'finished success')


@fabric.api.hosts(host)
def stop(path=path):
    """ Stopping
    """
    with fabric.api.cd(path):
        output('green', 'stoping mswallet')
        fabric.api.run('sh shutdown.sh')
        output('green', 'starting mswallet success')


@fabric.api.hosts(host)
def start(path=path):
    """ Starting
    """
    with fabric.api.cd(path):
        output('green', 'starting mswallet')
        fabric.api.run('sh startup.sh')
        output('green', 'starting mswallet success')


@fabric.api.hosts(host)
def update(path=path, sqls=None):
    """ Update
    """
    with fabric.api.cd(path):
        fabric.api.run('git pull')

    if sqls:
        output('green', 'starting execute sql files')
        sqls_list = sqls.split(',')
        for sql in sqls_list:
            output('blue', "executing %s" % sql)
            fabric.api.run(
                "mysql -umswallet -pmswallet mswallet < " + path + "/mswallet/sql/" + sql)
        output('blue', "finished execute sql")
    output('green', "update success")
