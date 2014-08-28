#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime, timedelta
import binascii
import json
import os
import urllib

from mock import patch
from tornado.testing import AsyncHTTPTestCase

from tipboard import settings, __version__
from tipboard.api import api_version
from tipboard.app import app

TILE_ID = '_'.join(('test_tile',  binascii.b2a_hex(os.urandom(5))))


# TODO: mock fake project id
class TestRestApi(AsyncHTTPTestCase):
    """
    Basic tests for API resources provided by Tipboard, i.e.:
    - push (POST)
    - tileconfig (POST, DELETE)
    - tiledata (GET, DELETE)
    - info (GET)
    """

    def shortDescription(self):
        # suppress printing tests' docstrings when verbosity level is >= 2
        return None

    def get_app(self):
        return app

    # in case of strange timeouts uncommenting this method may help
    # (see: https://github.com/facebook/tornado/issues/663)
    #def get_new_ioloop(self):
    #    return tornado.ioloop.IOLoop.instance()

    # I know that tests should be independent, but in this case it is
    # much better to run them in particular order.
    def test_01_api_key(self):
        """Test API key validation."""
        valid_key = settings.API_KEY
        invalid_key = 'some_invalid_key'
        url = '/'.join(('', 'api', api_version, valid_key, 'info'))
        self.http_client.fetch(self.get_url(url), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        url = '/'.join(('', 'api', api_version, invalid_key, 'info'))
        self.http_client.fetch(self.get_url(url), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 404)

    def test_02_info_resource(self):
        """Test if API resource 'info' works."""
        url = '/'.join(('', 'api', api_version, settings.API_KEY, 'info'))
        self.http_client.fetch(self.get_url(url), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        info_expected = {
            'tipboard_version': __version__,
            'project_name': settings.PROJECT_NAME,
            'project_layout_config': settings.LAYOUT_CONFIG,
            'redis_db': settings.REDIS,
        }
        info_expected = json.dumps(info_expected)
        self.assertEqual(response.body, info_expected)

    def test_03_push_resource(self):
        """Test if posting tile's data works."""
        url = '/'.join(('', 'api', api_version, settings.API_KEY, 'push'))
        data_to_push = {
            'tile': 'text',
            'key': TILE_ID,
            'data': json.dumps('test string'),
        }
        body = urllib.urlencode(data_to_push)
        fake_config = {
            'tiles_keys': [TILE_ID],
            'tiles_names': ['text'],
        }
        with patch('tipboard.api.get_tiles_configs') as m:
            m.return_value = fake_config
            self.http_client.fetch(
                self.get_url(url), self.stop, method='POST', body=body
            )
            response = self.wait()
        self.assertEqual(response.code, 200)

    def test_04_tileconfig_resource_post(self):
        """Test if posting tile's config works."""
        url = '/'.join(('', 'api', api_version, settings.API_KEY, 'tileconfig',
                        TILE_ID))
        config_to_push = {
            'value': json.dumps("{'font_color': '#00FF00'}"),
        }
        body = urllib.urlencode(config_to_push)
        fake_config = {
            'tiles_keys': [TILE_ID],
            'tiles_names': ['text'],
        }
        with patch('tipboard.api.process_layout_config') as m:
            m.return_value = fake_config
            self.http_client.fetch(
                self.get_url(url), self.stop, method='POST', body=body
            )
            response = self.wait()
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, "Tile's config updated.\n")

    def test_05_tiledata_resource_get(self):
        """Test if we can get back tile's data and config."""
        url = '/'.join(('', 'api', api_version, settings.API_KEY, 'tiledata',
                        TILE_ID))
        fake_config = {
            'tiles_keys': [TILE_ID],
            'tiles_names': ['text'],
        }
        with patch('tipboard.api.process_layout_config') as m:
            m.return_value = fake_config
            self.http_client.fetch(self.get_url(url), self.stop)
            mod_time_expected = datetime.now()
            response = self.wait()
        self.assertEqual(response.code, 200)
        data_received = json.loads(response.body)
        mod_time_received = datetime.strptime(data_received.pop('modified'),
                                              '%Y-%m-%d %H:%M:%S')
        data_expected = {
            'tile_template': 'text',
            'meta': "{'font_color': '#00FF00'}",
            'data': 'test string',
            'id': TILE_ID,
        }
        self.assertEqual(data_received, data_expected)
        # 'sanity_diff' is just a safety margin
        sanity_diff = timedelta(seconds=5)
        self.assertLessEqual(mod_time_expected - mod_time_received,
                             sanity_diff)

    def test_06_tileconfig_resource_delete(self):
        """Test if we can delete tile's config."""
        url = '/'.join(('', 'api', api_version, settings.API_KEY, 'tileconfig',
                        TILE_ID))
        fake_config = {
            'tiles_keys': [TILE_ID],
            'tiles_names': ['text'],
        }
        with patch('tipboard.api.process_layout_config') as m:
            m.return_value = fake_config
            self.http_client.fetch(self.get_url(url), self.stop,
                                   method='DELETE')
            response = self.wait()
        self.assertEqual(response.code, 200)
        # now let's check if 'meta' field is empty (it should be)
        url = '/'.join(('', 'api', api_version, settings.API_KEY, 'tiledata',
                        TILE_ID))
        with patch('tipboard.api.process_layout_config') as m:
            m.return_value = fake_config
            self.http_client.fetch(self.get_url(url), self.stop)
            response = self.wait()
        self.assertEqual(response.code, 200)
        data_received = json.loads(response.body)
        self.assertEqual(data_received['meta'], {})

    def test_07_tiledata_resource_delete(self):
        """Test if deleting tile's key works."""
        url = '/'.join(('', 'api', api_version, settings.API_KEY, 'tiledata',
                        TILE_ID))
        fake_config = {
            'tiles_keys': [TILE_ID],
            'tiles_names': ['text'],
        }
        with patch('tipboard.api.process_layout_config') as m:
            m.return_value = fake_config
            self.http_client.fetch(self.get_url(url), self.stop,
                                   method='DELETE')
            response = self.wait()
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, "Tile's data deleted.\n")
