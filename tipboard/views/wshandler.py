# -*- coding: utf-8 -*-
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from tipboard.cache import getCache
from tipboard.properties import COLORS, JS_LOG_LEVEL
from tipboard.utils import getRedisPrefix, getTimeStr

cache = getCache()
tipboard_helpers = {
    'color': COLORS,
    'log_level': JS_LOG_LEVEL,
}


class ChatConsumer(WebsocketConsumer):
    """Handles client connections on web sockets and listens on a Redis
    subscription."""

    def connect(self):
        async_to_sync(self.channel_layer.group_add)("event", self.channel_name)
        print(f"{getTimeStr()} (+) WS: New client with channel:{self.channel_name}", flush=True)
        self.accept()

    def disconnect(self, close_code):
        print(f"{getTimeStr()} (+) WS: client with channel:{self.channel_name} disconnected", flush=True)
        async_to_sync(self.channel_layer.group_discard)("event", self.channel_name)

    def receive(self, text_data, **kwargs):
        for tile_id in cache.listOfTilesCached:
            self.update_tile_receive(tile_id=tile_id)

    def update_tile_receive(self, tile_id):
        tileData = cache.get(tile_id=tile_id)
        if tileData is None:
            print(f'{getTimeStr()} (-) No data in key {tile_id} on Redis.', flush=True)
            #                stale_keys.add(tile_id)
            return
        data = json.loads(tileData)
        if type(data) is str:
            data = json.loads(data)
        data['tipboard'] = tipboard_helpers
        self.send(text_data=json.dumps(data))

    def update_tile(self, data):
        tile_id = getRedisPrefix(data['tile_id'])
        tileData = cache.get(tile_id=tile_id)
        if tileData is None:
            print(f'{getTimeStr()} (-) No data in key {tile_id} on Redis.', flush=True)
            return
        data = json.loads(tileData)
        if type(data) is str:
            data = json.loads(data)
        data['tipboard'] = tipboard_helpers
        self.send(text_data=json.dumps(data))
