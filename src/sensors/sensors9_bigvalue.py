import time
from src.sensors.utils import end, sendDataToTipboard, getTimeStr

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


def sonde9(isTest):
    print(f"{getTimeStr()} (+) Starting sensors 9", flush=True)
    start_time = time.time()
    data = executeScriptToGetData()
    tipboardAnswer = sendDataToTipboard(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)
    end(title=f"sensors9 -> {TILE_ID}", start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
