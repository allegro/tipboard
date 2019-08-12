#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import run

from fabtools import require
from fabtools.python import virtualenv


_TIPBOARD_USER = 'tipboard'
_SOURCE_CODE_URL = 'https://github.com/allegro/tipboard.git'


def install():
    configure_os()

    install_tipboard()

    run('chown -R %(user)s:%(user)s /home/%(user)s' % {'user': _TIPBOARD_USER})


def configure_os():
    require.deb.packages([
        'python',
        'python-dev',
        'python-virtualenv',
        'redis-server',
        'libmysqlclient-dev',
        'supervisor',
        'git',
    ])

    require.user(_TIPBOARD_USER, home='/home/' + _TIPBOARD_USER,
                 shell='/bin/bash')


def install_tipboard():
    venv_path = '/home/%s/tipboard-current' % _TIPBOARD_USER

    require.python.virtualenv(venv_path)

    with virtualenv(venv_path):
        require.python.package('distribute==0.6.28')
        require.python.package('tipboard',
                               url=_SOURCE_CODE_URL + '@master#egg=tipboard')

    require.supervisor.process('tipboard',
                               command='%s/bin/tipboard runserver' % venv_path,
                               directory='/home/%s' % _TIPBOARD_USER,
                               user=_TIPBOARD_USER,
                               stdout_logfile='/home/%s/out.log' %
                                              _TIPBOARD_USER)
