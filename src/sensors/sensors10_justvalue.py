import time
from src.sensors.utils import end
from src.sensors.utils import sendDataToTipboard

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


def sonde10(isTest):
    start_time = time.time()
    data = executeScriptToGetData()
    sendDataToTipboard(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)
    end(title=f"sensors10 -> {TILE_ID}", start_time=start_time)
