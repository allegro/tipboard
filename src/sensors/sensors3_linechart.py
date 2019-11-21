import time
from src.sensors.utils import end
from src.sensors.utils import sendDataToTipboard

NAME_OF_SENSORS = "linechart"
TILE_TEMPLATE = "line_chart"
TILE_ID = "line_chartjs_ex"


def executeScriptToGetData():
    """ Simulate some actions for text tile exemple"""
    line1 = [["23.09", 8326], ["24.09", 260630], ["25.09", 240933], ["26.09", 229639],
             ["27.09", 190240], ["28.09", 125272], ["29.09", 3685]]
    line2 = [["23.09", 3685], ["24.09", 125272], ["25.09", 190240], ["26.09", 229639],
             ["27.09", 240933], ["28.09", 260630], ["29.09", 108326]]
    return {
        "subtitle": "averages from last week",
        "description": "Sales in our dept",
        "series_list": [line1, line2]
    }


def sonde3(isTest):
    start_time = time.time()
    data = executeScriptToGetData()
    sendDataToTipboard(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)
    end(title=f"sensors3 -> {TILE_ID}", start_time=start_time)
