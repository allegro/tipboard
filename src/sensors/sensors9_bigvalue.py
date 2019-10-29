import json, requests, time
from src.tipboard.app.properties import TIPBOARD_URL
from src.sensors.utils import getTimeStr, end, buildConfigTile

NAME_OF_SENSORS = "big_value"
TILE_TEMPLATE = "big_value"
TILE_ID = "bv_ex"


def executeScriptToGetData():
    """ Simulate some actions for text tile exemple"""
    return {
        "title": "Tickets",
        "description": "number of blockers",
        "big-value": "314",
        "upper-left-label": "critical:",
        "upper-left-value": "1020",
        "lower-left-label": "major:",
        "lower-left-value": "8609",
        "upper-right-label": "minor:",
        "upper-right-value": "7532",
        "lower-right-label": "all:",
        "lower-right-value": "19 853"
    }


def sendDataToTipboard(data=None, tile_template=None, tile_id="", isTest=False):
    configTile = buildConfigTile(tile_id=tile_id, tile_template=tile_template, data=data)
    if not isTest:
        res = requests.post(TIPBOARD_URL + "/push", data=configTile)
        print(f"{getTimeStr()}:{res} -> {tile_id}: {res.text}", flush=True)


def sonde9(isTest):
    start_time = time.time()
    data = executeScriptToGetData()
    sendDataToTipboard(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)
    end(title=f"sensors9 -> {TILE_ID}", start_time=start_time)

