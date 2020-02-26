import json, redis
from asgiref.sync import async_to_sync
from src.tipboard.app.parser import parseXmlLayout
from src.tipboard.app.applicationconfig import getRedisPrefix, getIsoTime
from src.tipboard.app.properties import REDIS_DB, REDIS_PASSWORD, REDIS_HOST, REDIS_PORT, DEBUG
from src.tipboard.app.utils import getTimeStr
from channels.layers import get_channel_layer
from src.tipboard.app.FakeData.fake_data import buildFakeDataFromTemplate
from src.tipboard.app.FakeData.datasetbuilder import buildGenericDataset

cache = None


def getCache():
    global cache
    if cache is None:
        cache = MyCache()
    return cache


def listOfTilesFromLayout(layout_name='layout_config'):
    """ List all tiles for a specific layout in Config/*.yml"""
    tmp = parseXmlLayout(layout_name)['tiles_conf']
    return tmp


def update_dataset_from_tiles(value, previousData, key, tile_template):
    """ Update dict(tile value) with dict comming from the api, recursiv to update dict deeply """
    rcx = 0
    for dataset in value:
        if rcx >= len(previousData[key]):
            previousData[key].append(buildGenericDataset(tile_template=tile_template))
        update_tile_data_from_redis(previousData[key][rcx], dataset, tile_template)
        rcx = rcx + 1
    previousData[key] = previousData[key][0:len(value)]


def update_tile_data_from_redis(previousData, newData, tile_template):
    """ update value(dict) of tile with new data Recursiv & deep inside the tile """
    if isinstance(newData, str):
        previousData['text'] = newData
        return previousData
    for key, value in newData.items():
        if isinstance(value, dict) and key != 'data' and key in previousData:
            update_tile_data_from_redis(previousData[key], value, tile_template)
        elif isinstance(value, list) and key == 'datasets':
            update_dataset_from_tiles(value, previousData, key, tile_template)
        else:
            previousData[key] = value
    return previousData


def save_tile_ToRedis(tile_id, tile_template, tile_data):
    cache = getCache()
    tilePrefix = getRedisPrefix(tile_id)
    if not cache.redis.exists(tilePrefix) and DEBUG:  # if tile don't exist, create it with template, DEBUG mode only
        buildFakeDataFromTemplate(tile_id, tile_template, cache)
    cachedTile = json.loads(cache.redis.get(tilePrefix))
    cachedTile['data'] = update_tile_data_from_redis(cachedTile['data'], json.loads(tile_data), tile_template)
    cachedTile['modified'] = getIsoTime()
    cachedTile['tile_template'] = tile_template
    cache.set(tilePrefix, json.dumps(cachedTile))
    return True


class MyCache:
    def __init__(self, isTest=False):
        try:
            dbInRedis = "" if isTest else REDIS_DB
            self.redis = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD,
                                           decode_responses=True, db=dbInRedis)
            self.redis.time()
            self.isRedisConnected = True
            self.clientsWS = list()
        except Exception:
            print(f'{getTimeStr()} (+) Initializing cache: Redis not connected', flush=True)
            self.isRedisConnected = False

    def get(self, tile_id):
        prefix = tile_id
        if self.isRedisConnected and self.redis.exists(prefix):
            return json.dumps(self.redis.get(prefix))
        return None

    def set(self, tile_id, dumped_value, sendToWS=True):
        if self.isRedisConnected:
            self.redis.set(tile_id, dumped_value)
            if sendToWS:
                tile_id = tile_id.split(':')[-1]
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)('event', dict(type='update.tile', tile_id=tile_id))
            return True
        return False

    def delete(self, tile_id):
        if self.redis.exists(getRedisPrefix(tile_id=tile_id)):
            self.redis.delete(getRedisPrefix(tile_id=tile_id))
            return True
        return False

    def listOfTilesCached(self):
        return [key for key in self.redis.keys(getRedisPrefix())] if self.isRedisConnected else list()
