import json, redis
from asgiref.sync import async_to_sync
from src.tipboard.app.parser import parseXmlLayout
from src.tipboard.app.applicationconfig import getRedisPrefix
from src.tipboard.app.properties import REDIS_DB, REDIS_PASSWORD, REDIS_HOST, REDIS_PORT, LOG
from src.tipboard.app.utils import getTimeStr
from channels.layers import get_channel_layer

cache = None


def getCache():
    global cache
    if cache is None:
        cache = MyCache()
    return cache


def listOfTilesFromLayout(layout_name='layout_config'):
    rcx = 0
    listOfTiles = list()
    config = parseXmlLayout(layout_name)
    for tile in config['tiles_keys']:
        listOfTiles.append(dict(tile_id=tile, tile_template=config['tiles_names'][rcx]))
        rcx += 1
    return listOfTiles


class MyCache:
    def __init__(self):
        try:
            self.redis = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD,
                                           decode_responses=True, db=REDIS_DB)
            self.redis.time()
            self.isRedisConnected = True
            if LOG:
                print(f'{getTimeStr()} (+) Connect redis server with {len(self.listOfTilesCached())} key', flush=True)
            self.clientsWS = list()
        except Exception:
            print(f'{getTimeStr()} (+) Initializing cache: Redis not connected', flush=True)
            self.isRedisConnected = False

    def get(self, tile_id):
        prefix = tile_id
        if self.isRedisConnected and self.redis.exists(prefix):
            return json.dumps(self.redis.get(prefix))
        if LOG:
            print(f'{getTimeStr()} (-) tile: {prefix} not found in redis', flush=True)
        return None

    def set(self, tile_id, dumped_value, sendToWS=True):
        if LOG:
            print(f'{getTimeStr()} (+) Redis save and publish: {tile_id}', flush=True)
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
        if LOG:
            print(f'{getTimeStr()}(-) tile: {tile_id} not found in redis', flush=True)
        return False

    def listOfTilesCached(self):
        return [key for key in self.redis.keys(getRedisPrefix())] if self.isRedisConnected else list()
