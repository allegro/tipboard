import time
from src.sensors.utils import end
from src.sensors.utils import sendDataToTipboard

NAME_OF_SENSORS = "bar_chart"
TILE_TEMPLATE = "bar_chart"
TILE_ID = "barjs_ex"


def executeScriptToGetData():
    """ Simulate some actions for text tile exemple"""
    return {
        "title": "The A-Team",
        "subtitle": "Velocity (Last tree sprints)",
        "ticks": ["n-2", "n-1", "Last (n)"],
        "series_list": [[49, 50, 35], [13, 45, 9]]
    }


def sonde7(isTest):
    start_time = time.time()
    data = executeScriptToGetData()
    sendDataToTipboard(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)
    end(title=f"sensors7 -> {TILE_ID}", start_time=start_time)
