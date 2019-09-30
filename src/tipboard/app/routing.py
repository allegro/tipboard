from django.conf.urls import url
from src.tipboard.app.views.wshandler import WSConsumer

websocket_urlpatterns = [
    url(r'^communication/websocket$', WSConsumer),
]
