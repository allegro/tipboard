# -*- coding: utf-8 -*-
from datetime import datetime
from src.tipboard.app.properties import API_KEY, DEBUG


def getTimeStr():
    return datetime.now().strftime("%Hh%M")


def checkAccessToken(method='GET', request=None, unsecured=False):
    """ Check if API_TOKEN is correct. Who cares about api version ?"""
    key = "NO_KEY_FOUND"
    if unsecured or DEBUG:
        return True
    elif method == 'GET' or method == 'POST' or method == 'DELETE':  # TODO: check if it's work with delete:
        if request.GET.get('API_KEY', 'NO_API_KEY_FOUND') == API_KEY:
            return True
    print(f"{getTimeStr()} (-) Access Token error: {key}")
    return False
