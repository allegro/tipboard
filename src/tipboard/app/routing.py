from django.conf.urls import url
from src.tipboard.app.views.wshandler import ChatConsumer

websocket_urlpatterns = [
    url(r'^communication/websocket$', ChatConsumer),
]
