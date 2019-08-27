# -*- coding: utf-8 -*-
import datetime, json, requests, time
from src.tipboard.app.properties import TIPBOARD_URL
from src.sensors.utils import getTimeStr, end, sendBVColor

NAME_OF_SENSORS = "GET"
TILE_TEMPLATE = "pie_chartjs"
TILE_ID = "pie_charjs_ex"

def executeScriptToGetData():
    """ Simulate some actions for text tile exemple"""
    return {
        "title": "My title",
        "label": "No label",
        "pie_data_tag": ["Pie 42", "Pie 42", "Pie 42"],
        "pie_data_value": [25, 50, 25]
    }


def sendDataToTipboard(data=None, tile_template=None, tile_id=""):
    configTile = {
        "tile": tile_template, #tile_template name
        "key": tile_id, #tile_template name
        "data": json.dumps(data)
    }
    res = requests.post(TIPBOARD_URL + "/push", data=configTile)
    print(f"{res} -> {tile_id}: {res.text}", flush=True)

def sonde2():
    start_time = time.time()
    data = executeScriptToGetData()
    sendDataToTipboard(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID)
    end(title=f"sensors2 -> {TILE_ID}", start_time=start_time)