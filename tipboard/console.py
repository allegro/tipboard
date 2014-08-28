#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tipboard - flexible framework for creating dashboards.

Usage:
    tipboard runserver
    tipboard runserver [<port>]
    tipboard runserver [<host>] [<port>]
    tipboard create_project <name>
    tipboard test --list | -l
    tipboard test [<test_selector>]...
    tipboard (-h | --help)
    tipboard --version

Arguments:
    <test_selector> name of a test. Run "tipboard test --list" command to see
    names.

Options:
    -l --list     Show list of tests.
    -h --help     Show this screen.
    --version     Show version.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import logging.handlers
import os
import errno
import shutil
import sys
import unittest
import uuid

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


def _create_project_dir(project_name):
    user_config_dir = os.path.join(os.path.expanduser("~"), '.tipboard')
    try:
        os.mkdir(user_config_dir)
    except OSError as e:
        if all((e.errno == errno.EEXIST, os.path.isdir(user_config_dir))):
            pass
    custom_tiles_dir = os.path.join(user_config_dir, 'custom_tiles')
    if not os.path.exists(custom_tiles_dir):
        os.mkdir(custom_tiles_dir)


def _create_local_settings(project_name):
    user_config_dir = os.path.join(os.path.expanduser("~"), '.tipboard')
    user_layout_config = os.path.join(user_config_dir, 'layout_config.yaml')
    settings_local = os.path.join(user_config_dir, 'settings-local.py')
    if not os.path.exists(user_layout_config):
        shutil.copy2(
            os.path.join(
                settings.TIPBOARD_PATH, 'defaults/layout_config.yaml'  # noqa
            ),
            user_layout_config,
        )
    if not os.path.exists(settings_local):
        shutil.copy2(
            os.path.join(
                settings.TIPBOARD_PATH, 'defaults/settings-local.py'
            ),
            settings_local
        )
        api_key = str(uuid.uuid4()).replace('-', '')
        to_settings = (
            "PROJECT_NAME = '%s'" % project_name,
            "API_KEY = '%s'" % api_key,
        )
        with open(settings_local, 'a') as file_:
            for item in to_settings:
                file_.write('%s\n' % item)
            file_.write('\n')
    else:
        error_msg = "Can't override file: %s" % settings_local
        log.error(error_msg)
        print(error_msg)


def create_project(project_name):
    user_config_dir = os.path.join(os.path.expanduser("~"), '.tipboard')
    if not os.access(os.path.expanduser("~"), os.W_OK):
        print('Your home directory is not writable. Aborting.')
        return
    if not os.path.isdir(user_config_dir):
        _create_project_dir(project_name)
        _create_local_settings(project_name)
        print('Configuration files created in: %s' % user_config_dir)
    else:
        print('Configuration directory ~/.tipboard already exist. Aborting.')


def runserver(address=None, port=None):
    def populate_key_cache():
        client = redis.StrictRedis(**settings.REDIS)
        keys = ':'.join([settings.PROJECT_NAME, 'tile', '*'])
        for key in client.keys(keys):
            try:
                json.loads(client.get(key))
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


def run_tests(test_names_list):
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    if test_names_list:
        for test_name in test_names_list:
            full_name = '.'.join(['tipboard.tests', test_name])
            try:
                found = loader.loadTestsFromName(full_name)
                suite.addTests(found)
            except (AttributeError, ImportError) as e:
                print("No such test: {}".format(test_name))
                print("Running tests - STOPPED.")
                print("Run:\n  {}\nto see list of tests.".format(
                    "tipboard test --list"
                ))
                return False
    else:
        tests_path = os.path.join(settings.TIPBOARD_PATH, 'tests')
        suite = unittest.TestLoader().discover(tests_path, pattern='test*.py')
        if suite.countTestCases() == 0:
            print("Could not find any tests.")
            return False
    # mute useless communicates
    out_hdlr = open(os.devnull, "w")
    sys.stdout = out_hdlr
    logging.disable(logging.CRITICAL)
    unittest.TextTestRunner(verbosity=2).run(suite)


def show_test_names():
    """
    Prints available tests list, easy to be copied and run.
    """
    def _found_tests():
        tests_path = os.path.join(settings.TIPBOARD_PATH, 'tests')
        suite = loader.discover(tests_path, pattern='test*.py')
        for file_tests in suite._tests:
            for class_tests in file_tests._tests:
                for test in class_tests._tests:
                    yield test

    print('Available test names:')
    loader = unittest.TestLoader()
    last_test_file_name, last_test_case_name = '', ''
    for test in _found_tests():
        test_file_name, test_case_name = (
            str(test).split(' ')[1][1:-1].split('.')
        )
        test_name = test._testMethodName
        if last_test_file_name != test_file_name:
            to_print = '  ' + test_file_name
            print(to_print)
            last_test_file_name = test_file_name
        if last_test_case_name != test_case_name:
            to_print = '  {}'.format(
                '.'.join([to_print, test_case_name])
            )
            print(to_print)
            last_test_case_name = test_case_name
        print('  {}'.format('.'.join([to_print, test_name])))


def main():
    arguments = docopt(
        __doc__,
        version='Tipboard {}'.format(__version__)
    )
    if arguments.get('runserver'):
        runserver(
            address=arguments.get('<host>'), port=arguments.get('<port>')
        )
    if arguments.get('create_project'):
        create_project(arguments.get('<name>'))

    if arguments.get('test'):
        if arguments.get('--list'):
            show_test_names()
        else:
            run_tests(arguments.get('<test_selector>'))

if __name__ == '__main__':
    main()
