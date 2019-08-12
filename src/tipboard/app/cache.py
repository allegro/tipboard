# -*- coding: utf-8 -*-
import json, redis
from asgiref.sync import async_to_sync
from src.tipboard.app.properties import REDIS_DB, REDIS_PASSWORD, REDIS_HOST, REDIS_PORT, LOCAL, LOG
from src.tipboard.app.utils import getTimeStr, getRedisPrefix

cache = None


def getCache():
    global cache
    if cache is None:
        cache = MyCache()
    return cache


class MyCache:
    def __init__(self):
        try:
            self.redis = self.setup_redis()
            self.redis.time()
            self.isRedisConnected = True
            if LOG:
                print(f"{getTimeStr()} (+) Initializing cache from redis server with {len(self.listOfTilesCached())} key", flush=True)
            self.clientsWS = list()
        except:
            self.isRedisConnected = False
        pass

    def delete(self, tile_id, value=None, tile=None):
        if self.redis.exists(getRedisPrefix(tile_id=tile_id)):
            self.redis.delete(getRedisPrefix(tile_id=tile_id))
            return True
        if LOG:
            print(f"{getTimeStr()}(-) tile: {tile_id} not found in redis", flush=True)
        return False

    def get(self, tile_id):
        if LOG:
            print(f"cache.get({tile_id})", flush=True)
        prefix = tile_id
        if self.redis.exists(prefix):
            return json.dumps(self.redis.get(prefix))
        if LOG:
            print(f"{getTimeStr()} (-) tile: {prefix} not found in redis", flush=True)
        return None

    def setup_redis(self):
        if LOCAL:
            return redis.StrictRedis(host="0.0.0.0", port=REDIS_PORT, password=None, decode_responses=True, db=REDIS_DB)
        else:
            return redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True,
                                     db=REDIS_DB)

    def set(self, key, dumped_value):
        self.redis.set(key, dumped_value)
        if LOG:
            print(f"{getTimeStr()} (+) Redis save and publish: {key}", flush=True)
        key = key.split(":")[-1]
        from channels.layers import get_channel_layer
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)("event", {"type": "update.tile",  "tile_id": key}, )

    def listOfTilesCached(self):
        listOfTiles = list()
        for key in self.redis.keys(getRedisPrefix()):
            listOfTiles.append(key)
        return listOfTiles

