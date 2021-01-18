from datetime import datetime
from src.tipboard.app.properties import API_KEY


def getTimeStr():
    return datetime.now().strftime("%Hh%M")


def checkAccessToken(method='GET', request=None, unsecured=False):
    """ Check if API_TOKEN is correct. Who cares about api version ?"""
    if unsecured:
        return True
    if method == 'GET' or method == 'POST' or method == 'DELETE' and \
            request.GET.get('API_KEY', 'NO_API_KEY_FOUND') == API_KEY:
        return True
    return False
