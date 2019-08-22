# -*- coding: utf-8 -*-
import datetime, json, requests, time
from src.tipboard.app.properties import TIPBOARD_URL
from src.sensors.utils import getTimeStr, end, sendBVColor

NAME_OF_SENSORS = "GET"
TILE_TEMPLATE = ""
TILE_ID = "big_value"

def executeScriptToGetData():
    """ Simulate some actions for text tile exemple"""
    return {
        "title": f"Nbr AP connected",
        "description": f"{getTimeStr()} Mist wifi information",
        "big-value": f"39/42",
        "lower-left-label": "Offline AP:",
        "upper-left-label": "Offline AP:",
        "upper-right-label": f"AP42 " + f"& AP37",
        "lower-right-label": f"AP24 " + f"& AP03"
    }


def sendDataToTipboard(data=None, tile_template=None, tile_id=""):
    configTile = {
        "tile": tile_template, #tile_template name
        "key": tile_id, #tile_template name
        "data": json.dumps(data)
    }
    res = requests.post(TIPBOARD_URL + "/push", data=configTile)
    print(f"{res} -> {tile_id}: {res.text}", flush=True)

def sonde1():
    start_time = time.time()
    data = executeScriptToGetData()
    sendDataToTipboard(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID)
    end(title=f"sonde1 -> {TILE_ID}", start_time=start_time)