#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime
import json
import logging
import time

import redis

from tipboard import settings

log = logging.getLogger(__name__)

db_events_path = lambda: '{}:events'.format(settings.PROJECT_NAME)


class KeyNotFound(Exception):
    def __init__(self, key):
        self.key = key
        self.message = "Key '{}' was not found in db".format(self.key)


def redis_actions(method, tile_id, value=None, tile=None):
    key = '%s:tile:%s' % (settings.PROJECT_NAME, tile_id)
    try:
        redis_db = redis.Redis(**settings.REDIS_SYNC)
    except Exception as e:
        raise TypeError('Redis: %s' % e)
    else:
        if method.lower() == 'post':
            try:
                last_tile_data = get_redis_value(tile_id)
            except KeyNotFound as e:
                meta = {}
            else:
                meta = last_tile_data.get('meta')
            localtime = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            tz = '{0:+06.2f}'.format(-float(time.altzone) / 3600)
            iso_time = localtime + tz.replace('.', ':')  # ISO-8601
            required_structure = dict(
                id=tile_id,
                tile_template=tile,
                data=json.loads(value),
                meta=meta,
                modified=iso_time,
            )
            dumped_value = json.dumps(required_structure)
            redis_db.set(key, dumped_value)
            log.debug(
                'db key: {} set to value: {}'.format(
                    repr(key), repr(dumped_value)
                )
            )
            redis_db.publish(db_events_path(), key)
            return 'Push success.'

        elif method.lower() == 'get':
            db_value = redis_db.get(key)
            log.debug('got db value: {}'.format(db_value))
            return db_value
        elif method.lower() == 'delete':
            redis_db.delete(key)
            log.debug('deleted db key: {} '.format(key))
            return 'Deleted.'
        else:
            return 'Unkown method.'


def get_redis_value(tile_id):
    key = '%s:tile:%s' % (settings.PROJECT_NAME, tile_id)
    try:
        redis_db = redis.Redis(**settings.REDIS_SYNC)
    except Exception as e:
        raise TypeError('Redis: %s' % e)
    else:
        jsoned = redis_db.get(key)
        if not jsoned:
            raise KeyNotFound(key)
        db_data = json.loads(jsoned)
    return db_data


def set_redis_value(tile_id, data):
    key = '%s:tile:%s' % (settings.PROJECT_NAME, tile_id)
    try:
        redis_db = redis.Redis(**settings.REDIS)
    except Exception as e:
        raise TypeError('Redis: %s' % e)
    else:
        dumped_value = json.dumps(data)
        redis_db.set(key, dumped_value)
        redis_db.publish(db_events_path(), key)


def key_exist(key_id):
    key = '%s:tile:%s' % (settings.PROJECT_NAME, key_id)
    redis_db = redis.Redis(**settings.REDIS)
    return True if redis_db.get(key) else False
