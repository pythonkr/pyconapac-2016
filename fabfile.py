# -*- coding: utf-8 -*-
import os

from fabric.api import local, run, cd, prefix, env, sudo

if 'PYCON_HOST' not in os.environ:
    raise Exception('PYCON_HOST should be exported')
if 'PYCON_PORT' not in os.environ:
    raise Exception('PYCON_PORT should be exported')
if 'PYCON_USER' not in os.environ:
    raise Exception('PYCON_USER should be exported')

env.host_string = '{user}@{host}:{port}'.format(
                                            user=os.environ['PYCON_USER'],
                                            host=os.environ['PYCON_HOST'],
                                            port=os.environ['PYCON_PORT']
                                            )

def deploy(target='dev', sha1=None):
    if sha1 is None:
        # get current working git sha1
        sha1 = local('git rev-parse HEAD', capture=True)
    # server code reset to current working sha1
    home_dir = '/home/pyconkr/{target}.pycon.kr/pyconkr-2016'.format(target=target)
    with cd(home_dir):
        sudo('git fetch -p', user='pyconkr')
        sudo('git reset ' + sha1, user='pyconkr')
    # worker reload
    with cd(home_dir):
        sudo('restart.sh', user='pyconkr')
