# -*- coding: utf-8 -*-
from datetime import datetime
import json, redis, time
from asgiref.sync import async_to_sync
from tipboard.properties import *
from tipboard.utils import getTimeStr, getRedisPrefix

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
            self.listOfTilesCached = list()
            from tipboard.properties import PROJECT_NAME
            keys = ':'.join([PROJECT_NAME, 'tile', '*'])
            print(f"{getTimeStr()} (+) Initializing cache from redis server", flush=True)
            for key in self.redis.keys(keys):
                try:
                    json.loads(self.redis.get(key))
                except Exception:
                    print(f'{getTimeStr()} (-) Key {key} in Redis holds invalid data.', flush=True)
                    continue
                self.listOfTilesCached.append(key)
            self.clientsWS = list()
        except:
            self.isRedisConnected = False
        pass

    def getTiles(self):
        # if not self.isRedisConnected: return dict()
        # keys = self.redis.keys(TILES_PREFIX + '*')
        # result = list()
        # listTiles = self.redis.mget(keys=keys)
        # for site in listTiles:
        #     siteFromCache = json.loads(site)
        #     result.append(siteFromCache)
        return self.listOfTilesCached

    def getTile(self, tile_id):
        if not self.isRedisConnected: return dict()
        tile = self.redis.keys(getRedisPrefix(tile_id=tile_id))
        return tile

    def getHealthcheck(self):
        return {"Success": 'Connection succeed' if self.isRedisConnected else "Connection failure: Redis not connected",
                "Version": VERSION,
                "SendUsIssue": "https://github.com/adeo/issues/new/choose",
                "Documentation": "https://github.com/adeo/wiki",
                "Environment": SITE_ENV}

    def delete(self, tile_id, value=None, tile=None):
        if self.redis.exists(getRedisPrefix(tile_id=tile_id)):
            self.redis.delete(getRedisPrefix(tile_id=tile_id))
            return True
        print(f"{getTimeStr()}(-) tile: {tile_id} not found in redis", flush=True)
        return False

    def get(self, tile_id):
        prefix = tile_id
        if self.redis.exists(prefix):
            return json.dumps(self.redis.get(prefix))
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
        print(f"{getTimeStr()} (+) Redis save and publish: {key}", flush=True)
        key = key.split(":")[-1]
        from channels.layers import get_channel_layer
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)("chat", {"type": "update.tile",  "tile_id": key}, )


