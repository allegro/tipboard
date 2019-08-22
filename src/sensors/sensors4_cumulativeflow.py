# -*- coding: utf-8 -*-
import datetime, json, requests, time
from src.tipboard.app.properties import TIPBOARD_URL
from src.sensors.utils import getTimeStr, end, sendBVColor

NAME_OF_SENSORS = "cumuleflow"
TILE_TEMPLATE = "cumulative_flow"
TILE_ID = "cf_ex"

def executeScriptToGetData():
    """ Simulate some actions for text tile exemple"""
    label1 = {"label": "label 1", "series": [0, 0, 0, 0, 1, 1, 2, 2, 1, 1, 1, 0, 0, 2, 0]}
    label2 = {"label": "label 2", "series": [0, 5, 0, 0, 1, 0, 0, 3, 0, 0, 0, 7, 8, 9, 1]}
    return {"title": "My title:", "series_list": [label1, label2]}


def sendDataToTipboard(data=None, tile_template=None, tile_id=""):
    configTile = {
        "tile": tile_template, #tile_template name
        "key": tile_id, #tile_template name
        "data": json.dumps(data)
    }
    res = requests.post(TIPBOARD_URL + "/push", data=configTile)
    print(f"{res} -> {tile_id}: {res.text}", flush=True)

def sonde4():
    start_time = time.time()
    data = executeScriptToGetData()
    sendDataToTipboard(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID)
    end(title=f"sensors4 -> {TILE_ID}", start_time=start_time)