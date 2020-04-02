import json, redis
from datetime import datetime
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from apscheduler.schedulers.background import BackgroundScheduler
from src.tipboard.app.properties import REDIS_DB, REDIS_PASSWORD, REDIS_HOST, REDIS_PORT, DEBUG
from src.tipboard.app.DefaultData.defaultTileControler import buildFakeDataFromTemplate
from src.tipboard.app.DefaultData.chartJsDatasetBuilder import buildGenericDataset
from src.tipboard.app.parser import parseXmlLayout
from src.tipboard.app.applicationconfig import getRedisPrefix
from src.tipboard.app.utils import getTimeStr


def listOfTilesFromLayout(layout_name='default_config'):
    """ List all tiles for a specific layout in Config/*.yml """
    return parseXmlLayout(layout_name)['tiles_conf']


def update_dataset_from_tiles(value, previousData, key, tile_template):
    """ Update dict(tile value) with dict comming from the api, recursiv to update dict deeply """
    rcx = 0
    for dataset in value:
        if rcx >= len(previousData[key]):
            previousData[key].append(buildGenericDataset(tile_template=tile_template))
        update_tile_data_from_redis(previousData[key][rcx], dataset, tile_template)
        rcx = rcx + 1
    previousData[key] = previousData[key][0:len(value)]


def update_data_by_type(tile_template, previousData, key, value):
    """
    if dict, call again update_tile_data_from_redis in recursif
    if list, call update for list
    if not just override the value
    :param tile_template:
    :param previousData:
    :param key:
    :param value:
    :return:
    """
    if isinstance(value, dict) and key != 'data' and key in previousData:
        update_tile_data_from_redis(previousData[key], value, tile_template)
    elif isinstance(value, list) and key == 'datasets':
        update_dataset_from_tiles(value, previousData, key, tile_template)
    else:
        previousData[key] = value


def update_meta_if_present(tile_id, meta):
    """ Update the meta(config) of a tile(widget) """
    cachedTile = json.loads(MyCache().redis.get(getRedisPrefix(tile_id)))
    metaTile = cachedTile['meta']['options'] if 'options' in cachedTile['meta'] else cachedTile['meta']
    cachedTile['meta'] = update_tile_data_from_redis(metaTile, json.loads(meta), None)
    return cachedTile['meta']


def update_tile_data_from_redis(previousData, newData, tile_template):
    """ update value(dict) of tile with new data Recursiv & deep inside the tile """
    if isinstance(newData, str):
        previousData['text'] = newData
        return previousData
    for key, value in newData.items():
        update_data_by_type(tile_template, previousData, key, value)
    return previousData


def save_tile(tile_id, template, data, meta):
    redis_cache = MyCache()
    tilePrefix = getRedisPrefix(tile_id)
    if not redis_cache.redis.exists(tilePrefix) and DEBUG:
        buildFakeDataFromTemplate(tile_id, template, redis_cache)  # Build fake data and save it on redis
    cachedTile = json.loads(redis_cache.redis.get(tilePrefix))
    cachedTile['tile_template'] = template
    cachedTile['data'] = update_tile_data_from_redis(cachedTile['data'], json.loads(data), template)
    if meta is not None:
        cachedTile['meta'] = update_meta_if_present(tile_id, meta)
    redis_cache.set(tilePrefix, json.dumps(cachedTile))
    return True


class MyCache(object):
    """ Singleton redis object to handle (de)serialization of tiles and inform the channels to update websocket """
    instance = None

    def __new__(cls):
        if cls.instance is None:
            inst = cls.instance = super(MyCache, cls).__new__(cls)
            try:
                inst.redis = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD,
                                               decode_responses=True, db=REDIS_DB)
                inst.redis.time()
                inst.isRedisConnected = True
                inst.scheduler_sensors = BackgroundScheduler()
                inst.startedTime = datetime.now().strftime("%d %B %Y %T")
                inst.lastUpdateTime = datetime.now().strftime("%d %B %Y %T")
            except Exception:
                print(f'{getTimeStr()} (+) Initializing cache: Redis not connected', flush=True)
                inst.isRedisConnected = False
            return inst
        return cls.instance  # if already exist, return the instance already initialized :)

    def get(self, tile_id):
        if self.isRedisConnected and self.redis.exists(tile_id):
            return self.redis.get(tile_id)
        return None

    def set(self, tile_fullid, dumped_value):
        if self.isRedisConnected:
            self.redis.set(tile_fullid, dumped_value)
            tile_id = tile_fullid.split(':')[-1]  # quick split to get tileId without redis prefix
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)('event', dict(type='update.tile', tile_id=tile_id))
            self.lastUpdateTime = datetime.now().strftime("%d %B %Y %Hh%M")
            return True
        return False

    def delete(self, tile_id):
        if self.redis.exists(getRedisPrefix(tile_id=tile_id)):
            self.redis.delete(getRedisPrefix(tile_id=tile_id))
            return True
        return False

    def getLastUpdateTime(self):
        return self.lastUpdateTime

    def getFirstTimeStarter(self):
        return self.startedTime

    def listOfTilesCached(self):
        return [key for key in self.redis.keys(getRedisPrefix())] if self.isRedisConnected else list()
