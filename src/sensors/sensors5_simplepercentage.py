import requests, time
from src.tipboard.app.properties import TIPBOARD_URL
from src.sensors.utils import end, buildConfigTile

NAME_OF_SENSORS = "simple_percentage"
TILE_TEMPLATE = "simple_percentage"
TILE_ID = "sp_ex"


def executeScriptToGetData():
    """ Simulate some actions for text tile exemple"""
    return {"title": "My title",
            "subtitle": "My subtitle",
            "big_value": "100%",
            "left_label":  "smaller label 1", "left_value": "50%",
            "right_label": "smaller label 2", "right_value": "25%"}


def sendDataToTipboard(data=None, tile_template=None, tile_id="", isTest=False):
    configTile = buildConfigTile(tile_id=tile_id, tile_template=tile_template, data=data)
    if not isTest:
        res = requests.post(TIPBOARD_URL + "/push", data=configTile)
        print(f"{res} -> {tile_id}: {res.text}", flush=True)


def sonde5(isTest):
    start_time = time.time()
    data = executeScriptToGetData()
    sendDataToTipboard(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)
    end(title=f"sensors5 -> {TILE_ID}", start_time=start_time)
