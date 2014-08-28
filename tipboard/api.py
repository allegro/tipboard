#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import json
import urlparse

import tornado.escape
import tornado.ioloop
import tornado.web

import tipboard

from tipboard import redis_utils, settings
from tipboard.parser import (
    get_config_files_names,
    get_tiles_configs,
    process_layout_config,
)

logger = logging.getLogger(__name__)

api_version = 'v0.1'


class ValidatorMixin(object):
    """
    Validators returning None if everything is OK - otherwise suitable HTTP
    status and message is set.
    """
    def validate_post_request(self, post_field, allowed_fields):
        error_msg = None
        dict_diff = list(set(post_field) - set(allowed_fields))
        if dict_diff:
            self.set_status(400)
            error_msg = 'There are fields not allowed in your request.'
        for field in allowed_fields:
            if field not in post_field.keys():
                self.set_status(400)
                error_msg = "There is no '{}' field in your request.".format(
                    field,
                )
                break
        return error_msg

    def validate_with_config_file(self, post, parsed_config):
        error_msg = None
        if post['tile'][0] not in parsed_config['tiles_names']:
            self.set_status(404)
            error_msg = "Tile's name not found in the configuration file.\n"
        elif post['key'][0] not in parsed_config['tiles_keys']:
            self.set_status(404)
            error_msg = "Tile's key/id not found in the configuration file.\n"
        return error_msg

    def validate_with_config_files(self, post):
        tiles_configs = get_tiles_configs()
        error_msg = self.validate_with_config_file(post, tiles_configs)
        return error_msg

    def validate_with_json(self, jsoned_data):
        error_msg = None
        try:
            json.loads(jsoned_data)
        except ValueError:
            self.set_status(400)
            logger.debug('invalid json data: {}'.format(repr(jsoned_data)))
            error_msg = 'Invalid JSON data.\n'
        return error_msg


class ProjectInfo(tornado.web.RequestHandler):
    """Handles project info requests (for debugging/diagnostics)."""
    def get(self):
        # TODO: add info regarding custom/default tiles being used
        response = {
            'tipboard_version': tipboard.__version__,
            'project_name': settings.PROJECT_NAME,
            'project_layout_config': settings.LAYOUT_CONFIG,
            'redis_db': settings.REDIS,
        }
        self.write(response)


class Push(tornado.web.RequestHandler, ValidatorMixin):
    """
    Handles pushing tile's data.
    For pushing tile's config see MetaProperty class.
    """
    def post(self):
        validation_error = None
        post_field = urlparse.parse_qs(self.request.body)
        validation_error = self.validate_post_request(
            post_field,
            ['tile', 'key', 'data'],
        )
        if validation_error:
            self.write(validation_error)
            return
        validation_error = self.validate_with_config_files(post_field)
        if validation_error:
            self.write(validation_error)
            return
        validation_error = self.validate_with_json(post_field['data'][0])
        if validation_error:
            self.write(validation_error)
            return
        try:
            redis_utils.redis_actions(
                method='post',
                tile_id=post_field['key'][0],
                value=post_field['data'][0],
                tile=post_field['tile'][0],
            )
        except Exception as e:
            self.set_status(500)
            self.write(e.message)
        else:
            self.write("Tile's data pushed successfully.\n")


class TileData(tornado.web.RequestHandler):
    """Handles reading and deleting of tile's data."""
    # TODO: "it's better to ask forgiveness than permission" ;)
    def get(self, tile_key):
        if redis_utils.key_exist(tile_key):
            self.write(redis_utils.redis_actions('get', tile_key))
        else:
            self.set_status(404)
            self.write('%s key does not exist.\n' % tile_key)

    def delete(self, tile_key):
        if redis_utils.key_exist(tile_key):
            redis_utils.redis_actions('delete', tile_key)
            self.write("Tile's data deleted.\n")
        else:
            self.set_status(404)
            self.write('%s key does not exist.\n' % tile_key)


class MetaProperty(tornado.web.RequestHandler, ValidatorMixin):
    """Handles requests related to tile config changes."""
    def post(self, tile_key):
        post_field = urlparse.parse_qs(self.request.body)
        validation_error = self.validate_post_request(
            post_field,
            ['value'],
        )
        if validation_error:
            self.write(validation_error)
            return
        try:
            tile_data = redis_utils.get_redis_value(tile_key)
        except Exception:
            self.set_status(404)
            self.write("Can't find key %s.\n" % tile_key)
            return
        validation_error = self.validate_with_json(post_field['value'][0])
        if validation_error:
            self.write(validation_error)
            return
        tile_data['meta'] = json.loads(post_field['value'][0])
        redis_utils.set_redis_value(tile_key, tile_data)
        self.write("Tile's config updated.\n")

    def delete(self, tile_key):
        try:
            tile_data = redis_utils.get_redis_value(tile_key)
        except Exception:
            self.set_status(404)
            self.write('Cant find %s.\n' % tile_key)
        else:
            tile_data['meta'] = {}
            redis_utils.set_redis_value(tile_key, tile_data)
            self.write("Tile's config deleted.\n")
