# -*- coding: utf-8 -*-
from datetime import datetime
from src.tipboard.app.properties import API_KEY


def getTimeStr():
    return datetime.now().strftime("%Hh%M")


def checkAccessToken(method='GET', request=None, unsecured=False):
    """ Check if API_TOKEN is correct. Who cares about api version ?"""
    if unsecured:
        return True
    key = "NO_KEY_FOUND"
    if method == 'GET':
        key = request.GET.get('API_KEY', 'NO_API_KEY_FOUND')
        if key == API_KEY:
            return True
    elif method == 'POST':
        key = request.POST.get('API_KEY', 'NO_API_KEY_FOUND')
        if request.POST.get('API_KEY', 'NO_API_KEY') == API_KEY:
            return True
    elif method == 'DELETE': #TODO: check if it's work with delete
        key = request.POST.get('API_KEY', 'NO_API_KEY_FOUND')
        if request.POST.get('API_KEY', 'NO_API_KEY') == API_KEY:
            return True
    print(f"{getTimeStr()} (-) Access Token error: {key}")
    return False

