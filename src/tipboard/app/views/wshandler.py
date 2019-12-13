import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from src.tipboard.app.applicationconfig import getRedisPrefix
from src.tipboard.app.cache import getCache
from src.tipboard.app.properties import LOG
from src.tipboard.app.FakeData.fake_data import buildFakeDataFromTemplate
from src.tipboard.app.utils import getTimeStr

cache = getCache()


class WSConsumer(WebsocketConsumer):
    """Handles client connections on web sockets and listens on Redis subscriptions """

    def connect(self):  # pragma: no cover
        # self.channel_name = "events"
        async_to_sync(self.channel_layer.group_add)("event", self.channel_name)
        self.accept()

    def disconnect(self, close_code):  # pragma: no cover
        if LOG:
            print(f"{getTimeStr()} (+) WS: client with channel:{self.channel_name} disconnected", flush=True)
        async_to_sync(self.channel_layer.group_discard)("event", self.channel_name)
        self.close()

    def receive(self, text_data, **kwargs):  # pragma: no cover
        """ handle msg sended by client, by 2 way: update all tiles or update 1 specific tile """
        if "first_connection:" in text_data:
            for tile in cache.listOfTilesFromLayout(text_data.replace("first_connection:/", "")):
                self.update_tile_receive(tile_id=tile['tile_id'], template_name=tile['tile_template'])
        else:
            for tile_id in cache.listOfTilesCached():
                self.update_tile_receive(tile_id=tile_id)

    def update_tile_receive(self, tile_id, template_name=None):  # pragma: no cover
        """ """
        tileData = cache.get(tile_id=getRedisPrefix(tile_id))
        if tileData is None:
            if LOG:
                print(f'{getTimeStr()} (-) No data in key {tile_id} on Redis.', flush=True)
                print(f'{getTimeStr()} (-) Generating fake data for {tile_id}.', flush=True)
            data = buildFakeDataFromTemplate(tile_id, template_name, cache)
        else:
            data = json.loads(tileData)
        if type(data) is str:
            data = json.loads(data)
        self.send(text_data=json.dumps(data))

    def update_tile(self, data):  # pragma: no cover
        """ send to client a single tile config """
        tile_id = getRedisPrefix(data['tile_id'])
        tileData = cache.get(tile_id=tile_id)
        if tileData is None:
            if LOG:
                print(f'{getTimeStr()} (-) No data in key {tile_id} on Redis.', flush=True)
            return
        data = json.loads(tileData)
        if isinstance(data, str):
            data = json.loads(data)
        self.send(text_data=json.dumps(data))
