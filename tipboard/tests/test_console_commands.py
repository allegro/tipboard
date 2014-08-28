#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import random
import re
import shutil
import string
import sys
import time
import unittest

from mock import patch

from tipboard import console, settings


#TODO: mute command's output that goes to stdout
class TestConfigFiles(unittest.TestCase):

    def setUp(self):
        _temp = __import__('tipboard', fromlist=[str('settings')])
        self.settings = _temp.settings
        # we need to make sure that already existing '~/.tipboard' dir won't be
        # affected by tests, so we back it up (and restore it in tearDown)
        if os.path.exists(self.settings._user_config_dir):
            self.orig_conf_dir = self.settings._user_config_dir
            rnd_str = ''.join(
                random.choice(string.ascii_uppercase + string.digits)
                for x in range(8)
            )
            self.bkp_conf_dir = '_'.join((self.orig_conf_dir, rnd_str))
            os.rename(self.orig_conf_dir, self.bkp_conf_dir)

    @patch.object(sys, 'argv', [None, 'create_project', 'test_project'])
    def test_all_files_created(self):
        """
        check if command 'create_project test_project' creates required
        project structure.

        project structure contains:
            ~/.tipboard
                custom_tiles
                layout_config.yaml
                settings-local.py
        """
        console.main()
        config_paths = self.project_config_paths()
        for path_to_check in config_paths:
            self.assertTrue(os.path.exists(path_to_check))

    @patch.object(sys, 'argv', [None, 'create_project', 'test_project'])
    def test_recreate_project(self):
        """
        check if command 'create_project test_project' called twice
        doesn't affect already existing '~/.tipboard' dir
        """
        console.main()
        config_paths = self.project_config_paths()
        first_times, second_times = [], []
        for path in config_paths:
            mod_time = time.ctime(os.path.getmtime(path))
            first_times.append(mod_time)
        time.sleep(0.1)
        console.main()
        for path in config_paths:
            mod_time = time.ctime(os.path.getmtime(path))
            second_times.append(mod_time)
        for first_time, second_time in zip(first_times, second_times):
            item_idx = first_times.index(first_time)
            msg = u"file has changed: {}".format(config_paths[item_idx])
            self.assertEqual(first_time, second_time, msg)

    @patch.object(sys, 'argv', [None, 'create_project', 'test_project'])
    def test_config_contains_project_name(self):
        """check if 'settings-local.py' contains project's name"""
        console.main()
        project_name_line = "PROJECT_NAME = 'test_project'"
        _settings_local = os.path.join(
            settings._user_config_dir, 'settings-local.py'
        )
        msg = 'settings-local.py does not include {}'.format(
            repr(project_name_line)
        )
        with open(_settings_local) as settings_file:
            self.assertIn(project_name_line, settings_file.read(), msg)

    @patch.object(sys, 'argv', [None, 'create_project', 'test_project'])
    def test_config_contains_api_key(self):
        """check if 'settings-local.py' contains API key"""
        console.main()
        api_key_line = re.compile('API_KEY = \'[0-9a-z]{32}\'')
        _settings_local = os.path.join(
            settings._user_config_dir, 'settings-local.py'
        )
        msg = 'settings-local.py does not include API_KEY string'
        with open(_settings_local) as settings_file:
            self.assertRegexpMatches(settings_file.read(), api_key_line, msg)

    def tearDown(self):
        try:
            # delete '~/.tipboard' dir that we created for tests
            shutil.rmtree(self.settings._user_config_dir)
        except (OSError):
            pass
        try:
            if os.path.exists(self.bkp_conf_dir):
                # restore conf dir backed up by setUp
                os.rename(self.bkp_conf_dir, self.orig_conf_dir)
        except AttributeError:
            pass
        self.reset_settings()

    def reset_settings(self):
        reload(self.settings)

    def project_config_paths(self):
        config_paths = [
            self.settings._user_config_dir,
            os.path.join(self.settings._user_config_dir, 'custom_tiles'),
            os.path.join(self.settings._user_config_dir, 'layout_config.yaml'),
            os.path.join(self.settings._user_config_dir, 'settings-local.py'),
        ]
        return config_paths
