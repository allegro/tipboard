from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from src.tipboard.app.applicationconfig import getRedisPrefix
from src.tipboard.app.cache import MyCache, listOfTilesFromLayout
from src.tipboard.app.DefaultData.defaultTileControler import buildFakeDataFromTemplate


class WSConsumer(WebsocketConsumer):
    """ Handles client connections on web sockets and listens on Redis subscriptions """

    def connect(self):
        async_to_sync(self.channel_layer.group_add)('event', self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)('event', self.channel_name)
        self.close()

    def receive(self, text_data, **kwargs):
        """ handle msg sended by client, by 2 way: update all tiles or update 1 specific tile """
        if 'first_connection:' in text_data:
            listOftiles = listOfTilesFromLayout(text_data.replace('first_connection:/', ''))
            for tileId in listOftiles:
                self.update_tile_receive(tile_id=tileId, template_name=listOftiles[tileId]['tile_template'])
        else:
            for tile_id in MyCache().listOfTilesCached():
                self.update_tile_receive(tile_id=tile_id)

    def update_tile_receive(self, tile_id, template_name=None):
        """ Create or update the tile with value and send to the client with websocket """
        tileData = MyCache().get(tile_id=getRedisPrefix(tile_id))
        if tileData is None:
            print(f'[DEBUG] (-) Building fake data for {tile_id}. with template {template_name}', flush=True)
            tileData = buildFakeDataFromTemplate(tile_id, template_name, MyCache())
        self.send(text_data=tileData)

    def update_tile(self, data):
        """ send to client a single tile config """
        self.send(text_data=MyCache().get(tile_id=getRedisPrefix(data['tile_id'])))
