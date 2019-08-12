# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time, os, json
from datetime import datetime
from src.tipboard.app.properties import PROJECT_NAME, TIPBOARD_PATH, LOG
from src.tipboard.app.parser import get_tiles_configs


def validate_post_request(post_field, allowed_fields):
    """
    Validators returning None if everything is OK - otherwise suitable HTTP
    status and message is set.
    """
    error_msg = None
    dict_diff = list(set(post_field) - set(allowed_fields))
    if dict_diff:
        error_msg = 'There are fields not allowed in your request.'
    for field in allowed_fields:
        if field not in post_field.keys():
            error_msg = "There is no '{}' field in your request.".format(
                field,
            )
            break
    return error_msg


def validate_with_config_file(post, parsed_config):
    error_msg = None
    if post['tile'][0] not in parsed_config['tiles_names']:
        error_msg = "Tile's name not found in the configuration file.\n"
    elif post['key'][0] not in parsed_config['tiles_keys']:
        error_msg = "Tile's key/id not found in the configuration file.\n"
    return error_msg


def validate_with_config_files(post):
    tiles_configs = get_tiles_configs()
    error_msg = validate_with_config_file(post, tiles_configs)
    return error_msg


def validate_with_json(jsoned_data):
    error_msg = None
    try:
        json.loads(jsoned_data)
    except ValueError:
        if LOG:
            print(f'{getTimeStr()} (-) invalid json data: {repr(jsoned_data)}', flush=True)
        error_msg = 'Invalid JSON data.\n'
    return error_msg


def getRedisPrefix(tile_id="*"):
    return f'{PROJECT_NAME}:tile:{tile_id}'


def getTimeStr():
    return datetime.now().strftime("%Hh%M")


def getIsoTime():
    localtime = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    tz = '{0:+06.2f}'.format(-float(time.altzone) / 3600)
    iso_time = localtime + tz.replace('.', ':')  # ISO-8601
    return iso_time


def verify_statics(static_file):
    user_tiles_path = os.path.join(
        '.tipboard', '.tipboard/custom_tiles'
    )
    tipboard_tiles_path = os.path.join(TIPBOARD_PATH, 'tiles')
    found = False
    for path in user_tiles_path, tipboard_tiles_path:
        if os.path.exists(os.path.join(path, static_file)):
            found = True
            break
    return found


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