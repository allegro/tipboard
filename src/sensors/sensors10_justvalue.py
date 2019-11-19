import requests, time
from src.tipboard.app.properties import TIPBOARD_URL
from src.sensors.utils import end, buildConfigTile

NAME_OF_SENSORS = "GET"
TILE_TEMPLATE = "just_value"
TILE_ID = "jv_ex"


def executeScriptToGetData():
    """ Simulate some actions for text tile exemple"""
    return {
        "title": "Next release:",
        "description": "(days remaining)",
        "just-value": "23"
    }


def sendDataToTipboard(data=None, tile_template=None, tile_id="", isTest=False):
    configTile = buildConfigTile(tile_id=tile_id, tile_template=tile_template, data=data)
    if not isTest:
        res = requests.post(TIPBOARD_URL + "/push", data=configTile)
        print(f"{res} -> {tile_id}: {res.text}", flush=True)


def sonde10(isTest):
    start_time = time.time()
    data = executeScriptToGetData()
    sendDataToTipboard(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)
    end(title=f"sensors10 -> {TILE_ID}", start_time=start_time)
