# -*- coding: utf-8 -*-
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from src.tipboard.app.applicationconfig import getRedisPrefix
from src.tipboard.app.cache import getCache
from src.tipboard.app.properties import COLORS, JS_LOG_LEVEL, LOG
from src.tipboard.app.fake_data import buildFakeDataFromTemplate
from src.tipboard.app.utils import getTimeStr


cache = getCache()
tipboard_helpers = {#TODO: merge in properties.py
    'color': COLORS,
    'log_level': JS_LOG_LEVEL,
}


class ChatConsumer(WebsocketConsumer):
    """Handles client connections on web sockets and listens on Redis subscriptions """

    def connect(self):
        #self.channel_name = "events"
        async_to_sync(self.channel_layer.group_add)("event", self.channel_name)
        if LOG:
            print(f"{getTimeStr()} (+) WS: New client with channel:{self.channel_name}", flush=True)
        self.accept()

    def disconnect(self, close_code):
        if LOG:
            print(f"{getTimeStr()} (+) WS: client with channel:{self.channel_name} disconnected", flush=True)
        async_to_sync(self.channel_layer.group_discard)("event", self.channel_name)

    def receive(self, text_data, **kwargs):
        """ handle msg sended by client, by 2 way: update all tiles or update 1 specific tile """
        if "first_connection:" in text_data:
            if LOG:
                print("Initiate first ws connect for a client, sending all tiles")
            for tile in cache.listOfTilesFromLayout(text_data.replace("first_connection:/", "")):
                self.update_tile_receive(tile_id=tile['tile_id'], template_name=tile['tile_template'])
        else:
            if LOG:
                print("Clientws ask for tile update")
            for tile_id in cache.listOfTilesCached():
                self.update_tile_receive(tile_id=tile_id)

    def update_tile_receive(self, tile_id, template_name=None):
        """ """
        print("wsHandler::update_tile_receive:" + tile_id)
        tileData = cache.get(tile_id=getRedisPrefix(tile_id))
        if tileData is None:
            if LOG:
                print(f'{getTimeStr()} (-) No data in key {tile_id} on Redis.', flush=True)
            if LOG:
                print(f'{getTimeStr()} (-) Generating fake data for {tile_id}.', flush=True)
            data = buildFakeDataFromTemplate(tile_id, template_name, cache)
        else:
            data = json.loads(tileData)
        if type(data) is str:
            data = json.loads(data)
        #TODO:
        # data is null
        # car dans le redis, la data est null
        # car la fake Data a pas été write, donc renvoie null
        # Ce qui empeche le trigger de la fake data dans le norm.js pour tester la chart :(
        data['tipboard'] = tipboard_helpers
        self.send(text_data=json.dumps(data))

    def update_tile(self, data):
        """ """
        tile_id = getRedisPrefix(data['tile_id'])
        tileData = cache.get(tile_id=tile_id)
        if tileData is None:
            if LOG:
                print(f'{getTimeStr()} (-) No data in key {tile_id} on Redis.', flush=True)
            return
        data = json.loads(tileData)
        if type(data) is str:
            data = json.loads(data)
        data['tipboard'] = tipboard_helpers
        self.send(text_data=json.dumps(data))

