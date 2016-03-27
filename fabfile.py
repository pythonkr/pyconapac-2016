# -*- coding: utf-8 -*-
import os

from fabric.api import local, run, cd, prefix, env, sudo
from deploy import server

env.host_string = '{user}@{host}:{port}'.format(
                                            user=env.pycon_user,
                                            host=env.pycon_host,
                                            port=env.pycon_port
                                            )


def deploy(target='dev', sha1=None):
    if sha1 is None:
        # get current working git sha1
        sha1 = local('git rev-parse HEAD', capture=True)
    # server code reset to current working sha1
    home_dir = '/home/pyconkr/{target}.pycon.kr/pyconkr-2016'.format(target=target)
    python_env = '/home/pyconkr/.pyenv/versions/pyconkr-2016'
    with cd(home_dir):
        sudo('git fetch --all -p', user='pyconkr')
        sudo('git reset --hard ' + sha1, user='pyconkr')
        sudo('bower install', user='pyconkr')
        sudo('%s/bin/pip install -r requirements.txt' % python_env, user='pyconkr')
        sudo('%s/bin/python manage.py compilemessages' % python_env, user='pyconkr')
        sudo('%s/bin/python manage.py makemigrations' % python_env, user='pyconkr')
        sudo('%s/bin/python manage.py migrate' % python_env, user='pyconkr')
        sudo('%s/bin/python manage.py collectstatic --noinput' % python_env, user='pyconkr')
        sudo('%s/bin/python manage.py loaddata pyconkr/fixtures/flatpages.json' % python_env, user='pyconkr')
    # worker reload
    with cd(home_dir):
        if target == 'dev':
            sudo('restart pyconkr-2016/uwsgi-%s' % target)
        else:
            sudo('restart pyconkr-2016/uwsgi' % target)
