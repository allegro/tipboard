from django.conf.urls import url
from tipboard.views.wshandler import ChatConsumer

websocket_urlpatterns = [
    url(r'^communication/websocket$', ChatConsumer),
]
