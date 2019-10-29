import requests, time
from src.tipboard.app.properties import TIPBOARD_URL
from src.sensors.utils import end, buildConfigTile

NAME_OF_SENSORS = "fancy_listing"
TILE_TEMPLATE = "fancy_listing"
TILE_ID = "fancy_ex"


def executeScriptToGetData():
    """ Simulate some actions for text tile exemple"""
    return [
        {"label": "My label 1", "text": "Lorem ipsum", "description": "such description"},
        {"label": "My label 2", "text": "Dolor sit", "description": "yet another"},
        {"label": "My label 3", "text": "Amet", "description": ""}
    ]


def sendDataToTipboard(data=None, tile_template=None, tile_id="", isTest=False):
    configTile = buildConfigTile(tile_id=tile_id, tile_template=tile_template, data=data)
    if not isTest:
        res = requests.post(TIPBOARD_URL + "/push", data=configTile)
        print(f"{res} -> {tile_id}: {res.text}", flush=True)


def sonde8(isTest):
    start_time = time.time()
    data = executeScriptToGetData()
    sendDataToTipboard(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)
    end(title=f"sensors8 -> {TILE_ID}", start_time=start_time)
