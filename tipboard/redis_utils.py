#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import json
import logging
import time

import redis

from tipboard import settings

log = logging.getLogger(__name__)

db_events_path = lambda: '{}:events'.format(settings.PROJECT_NAME)


def get_modified():
    localtime = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    tz = '{0:+06.2f}'.format(-float(time.altzone) / 3600)
    iso_time = localtime + tz.replace('.', ':')  # ISO-8601
    return iso_time


def redis_save(tile_id, data):
    key = '{project_name}:tile:{tile_id}'.format(
        project_name=settings.PROJECT_NAME,
        tile_id=tile_id,
    )
    redis_db = redis.Redis(**settings.REDIS_SYNC)
    # data['modified'] = get_modified()?
    redis_db.set(key, json.dumps(data))
    log.debug(
        'db key: {} set to value: {}'.format(repr(key), repr(data))
    )
    redis_db.publish(db_events_path(), key)
