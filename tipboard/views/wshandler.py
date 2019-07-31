# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#from tipboard.cache import getCache
from tipboard.properties import *
#from tipboard.utils import getRedisPrefix
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

#cache = getCache()
tipboard_helpers = {
    'color': COLORS,
    'log_level': JS_LOG_LEVEL,
}


class ChatConsumer(WebsocketConsumer):
    """Handles client connections on web sockets and listens on a Redis
    subscription."""

    def connect(self):
        #self.channel_name = "events"
        print(f"{getTimeStr()} (+) WS: New client with channel:{self.channel_name}", flush=True)

    def disconnect(self, close_code):
        print(f"{getTimeStr()} (+) WS: client with channel:{self.channel_name} disconnected", flush=True)


    def receive(self, text_data, **kwargs):
        pass

