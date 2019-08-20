# -*- coding: utf-8 -*-
import time, datetime
from django.apps import AppConfig
from src.tipboard.app.properties import PROJECT_NAME


class TipboardConfig(AppConfig):
    name = 'tipboard'
    verbose_name = "DjangoBoard"


def getIsoTime():
    localtime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    tz = '{0:+06.2f}'.format(-float(time.altzone) / 3600)
    iso_time = localtime + tz.replace('.', ':')  # ISO-8601
    return iso_time


def getRedisPrefix(tile_id="*"):
    return f'{PROJECT_NAME}:tile:{tile_id}'
