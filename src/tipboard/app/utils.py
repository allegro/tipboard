# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time, os, json
from datetime import datetime
from src.tipboard.app.properties import PROJECT_NAME, TIPBOARD_PATH, LOG
from src.tipboard.app.parser import get_tiles_configs


def getRedisPrefix(tile_id="*"):
    return f'{PROJECT_NAME}:tile:{tile_id}'


def getTimeStr():
    return datetime.now().strftime("%Hh%M")


def getIsoTime():
    localtime = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    tz = '{0:+06.2f}'.format(-float(time.altzone) / 3600)
    iso_time = localtime + tz.replace('.', ':')  # ISO-8601
    return iso_time


def tile_path(tile_name):
    """
    Searches for tile's html file (in user's 'custom_tiles' folder,
    and then in app's 'tiles' folder) and returns full path of
    the tile, or raises exception if html file is not present in none
    of those locations.
    """
    user_tiles_path = os.path.join('.tipboard', '.tipboard/custom_tiles')
    tipboard_tiles_path = os.path.join(TIPBOARD_PATH, 'tiles')
    tile_html = '.'.join((tile_name, 'html'))
    for path in user_tiles_path, tipboard_tiles_path:
        tile_path = os.path.join(path, tile_html)
        if os.path.exists(tile_path):
            return tile_path
    raise UserWarning(f'No such tile: {tile_name}')