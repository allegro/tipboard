# -*- coding: utf-8 -*-
import datetime, json, requests, time
from src.tipboard.app.properties import TIPBOARD_URL
from src.sensors.utils import getTimeStr, end, sendBVColor

NAME_OF_SENSORS = "linechart"
TILE_TEMPLATE = "line_chart"
TILE_ID = "line_ex"

def executeScriptToGetData():
    """ Simulate some actions for text tile exemple"""
    line1 = [["23.09", 8326], ["24.09", 260630], ["25.09", 240933], ["26.09", 229639],
             ["27.09", 190240], ["28.09", 125272], ["29.09", 3685]]
    line2 = [["23.09", 3685], ["24.09", 125272], ["25.09", 190240], ["26.09", 229639],
             ["27.09", 240933], ["28.09", 260630], ["29.09", 108326]]
    return {"subtitle": "averages from last week",
               "description": "Sales in our dept",
               "series_list": [line1, line2]}


def sendDataToTipboard(data=None, tile_template=None, tile_id="", isTest=False):
    configTile = {
        "tile": tile_template, #tile_template name
        "key": tile_id, #tile_template name
        "data": json.dumps(data)
    }
    if not isTest:
        res = requests.post(TIPBOARD_URL + "/push", data=configTile)
        print(f"{res} -> {tile_id}: {res.text}", flush=True)

def sonde3(isTest):
    start_time = time.time()
    data = executeScriptToGetData()
    sendDataToTipboard(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)
    end(title=f"sensors3 -> {TILE_ID}", start_time=start_time)