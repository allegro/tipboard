#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import random
import shutil
import string
import sys
import unittest

from mock import patch

from tipboard import console, parser, settings

DEFAULT_CONFIG_NAME = 'layout_config'
SECOND_CONFIG_NAME = '2nd-' + DEFAULT_CONFIG_NAME


@patch.object(sys, 'argv', [None, 'create_project', 'test_project'])
def _create_test_project():
    console.main()


class TestConfigParser(unittest.TestCase):

    def setUp(self):
        # backup userspace .tipboard
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
        _create_test_project()

    def test_get_rows(self):
        """simple call of get_rows method and check rows count"""
        EXPECTED = 2
        config_file = parser.process_layout_config(DEFAULT_CONFIG_NAME)
        found_rows = parser._get_rows(config_file['layout'])
        rows_count = len(found_rows)
        msg = u'Found {} rows instead of expected {}'.format(
            rows_count, EXPECTED
        )
        self.assertEqual(rows_count, EXPECTED, msg)

    def test_get_rows_cols_validator(self):
        """
        negative test: checks if parser's get_rows method find wrong rows count
        """
        config_file = parser.process_layout_config(DEFAULT_CONFIG_NAME)
        broken_layout = config_file['layout'][:]
        popped_row = broken_layout.pop()
        row_class, cols_data = popped_row.items()[0]
        broken_key = row_class.replace('1', '5')
        broken_row = {
            broken_key: cols_data,
        }
        broken_layout.append(broken_row)
        try:
            parser._get_rows(broken_layout)
        except parser.WrongSumOfRows:
            # test passed
            pass
        else:
            raise Exception("Parser's get_rows method skipped layout error")

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
        reload(self.settings)


class TestConfigFiles(unittest.TestCase):

    def setUp(self):
        # backup userspace .tipboard
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
        _create_test_project()
        self._create_second_config()

    def test_finding_configs_files(self):
        """
        Check if function get_config_files_names finds all configs files in
        user space
        """
        expected_configs_names = [DEFAULT_CONFIG_NAME, SECOND_CONFIG_NAME]
        found_configs_names = parser.get_config_files_names()
        self.assertEqual(
            len(expected_configs_names), len(found_configs_names),
            "Expected config number: {}, found: {}".format(
                len(expected_configs_names), len(found_configs_names)
            )
        )
        for config_name in found_configs_names:
            config_file_path = parser.config_file_name2path(config_name)
            self.assertTrue(
                os.path.exists(config_file_path),
                'File does not exists: {}'.format(config_file_path),
            )

    def test_collecting_tiles_data(self):
        """
        Checks if function get_tiles_configs returns:
            - correct number of tile ids
            - correct number of tile types
            - all required tiles_types and tiles_keys
        """
        tile_types_number = 2  # from data_to_check
        tile_ids_number = 3  # from data_to_check
        data_to_check = (
            ('empty', 'empty'),
            ('text', 'id1'),
            ('text', 'id2'),
        )
        read_data = parser.get_tiles_configs()

        self.assertEqual(
            len(read_data['tiles_names']), tile_types_number,
            'Expected tile_types number: {} found {}'.format(
                tile_types_number, len(read_data['tiles_names'])
            )
        )
        self.assertEqual(
            len(read_data['tiles_keys']), tile_ids_number,
            'Expected tile_ids number: {} found {}'.format(
                tile_types_number, len(read_data['tiles_names'])
            )
        )
        for tile_name, tile_key in data_to_check:
            self.assertIn(tile_name, read_data['tiles_names'])
            self.assertIn(tile_key, read_data['tiles_keys'])

    def _create_second_config(self):
        file_content = """
details:
    page_title: Empty Dashboard
layout:
    - row_1_of_2:
        - col_1_of_1:
            - tile_template: text
              tile_id: id1
              title: Empty Tile
              classes:

    - row_1_of_2:
        - col_1_of_1:
            - tile_template: text
              tile_id: id2
              title: Empty Tile
              classes: """
        dst = os.path.join(
            settings._user_config_dir, '.'.join([SECOND_CONFIG_NAME, 'yaml'])
        )
        with open(dst, 'wb') as config_file:
            config_file.write(str(file_content))

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
        reload(self.settings)
