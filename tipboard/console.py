#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tipboard - flexible framework for creating dashboards.

Usage:
    tipboard runserver
    tipboard runserver [<port>]
    tipboard runserver [<host>] [<port>]
    tipboard (-h | --help)
    tipboard --version

Options:
    -h --help     Show this screen.
    --version     Show version.
"""

import logging
import logging.handlers
import os

from docopt import docopt
import json
import redis
import tornado.ioloop
import tornado.options
import tornado.web

from tipboard import __version__, settings
from tipboard.app import app, DashboardSocketHandler


def _setup_logger():
    log_file_path = os.path.join(os.path.expanduser("~"), 'tipboard.log')
    # for the explaination of the options below see method
    # 'define_logging_options' in Tornado's sources (file 'log.py')
    args = [
        # first element is skipped (parse_command_line emulates sys.argv)
        'tipboard',
        # logging to STDERR
        '--logging=debug',
        '--log_to_stderr=true',
        # logging to file with Tornado's logrotate
        # (10 MB for the current log + 1 backup)
        '--log_file_prefix={}'.format(log_file_path),
        '--log_file_max_size={}'.format(10 * 1000 * 1000),
        '--log_file_num_backups={}'.format(1),
    ]
    tornado.options.parse_command_line(args=args)


_setup_logger()
log = logging.getLogger(__name__)


def runserver(address=None, port=None):
    def populate_key_cache():
        client = redis.StrictRedis(**settings.REDIS)
        keys = ':'.join([settings.PROJECT_NAME, 'tile', '*'])
        for key in client.keys(keys):
            key = key.decode('utf8')
            try:
                json.loads(client.get(key).decode('utf8'))
            except Exception:
                log.warn('Key %s in Redis holds invalid data.', key)
                continue
            DashboardSocketHandler.cache.add(key)
        log.info('Following keys already in Redis:\n{}'.format(
            '\n'.join(sorted(DashboardSocketHandler.cache)),
        ))

    if not address:
        address = settings.HOST
    if not port:
        port = settings.PORT
    else:
        try:
            int(port)
        except ValueError:
            print(u'Passed port {} is not integer'.format(port))
            return False
    populate_key_cache()
    app.listen(port, address=address)
    log.info("Listening on port {}:{}...".format(address, port))
    tornado.ioloop.IOLoop.instance().start()


def main():
    arguments = docopt(
        __doc__,
        version='Tipboard {}'.format(__version__)
    )
    if arguments.get('runserver'):
        runserver(
            address=arguments.get('<host>'), port=arguments.get('<port>')
        )

if __name__ == '__main__':
    main()
