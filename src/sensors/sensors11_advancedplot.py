# -*- coding: utf-8 -*-
import datetime, json, requests, time
from src.tipboard.app.properties import TIPBOARD_URL
from src.sensors.utils import getTimeStr, end, sendBVColor

NAME_OF_SENSORS = "advanced_plot"
TILE_TEMPLATE = "advanced_plot"
TILE_ID = "ap_ex"

def executeScriptToGetData():
    """ Simulate some actions for text tile exemple"""
    return {
        "title": "Metric Tons per Year",
        "description": "",
        "plotData": [[[2, 1], [4, 2], [6, 3], [3, 4]],
                     [[5, 1], [1, 2], [3, 3], [4, 4]],
                     [[4, 1], [7, 2], [1, 3], [2, 4]]]
    }


def sendDataToTipboard(data=None, tile_template=None, tile_id="", isTest=False):
    configTile = {
        "tile": tile_template, #tile_template name
        "key": tile_id, #tile_template name
        "data": json.dumps(data)
    }
    if not isTest:
        res = requests.post(TIPBOARD_URL + "/push", data=configTile)
        print(f"{res} -> {tile_id}: {res.text}", flush=True)

def sonde11(isTest):
    start_time = time.time()
    data = executeScriptToGetData()
    sendDataToTipboard(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)
    end(title=f"sensors11 -> {TILE_ID}", start_time=start_time)