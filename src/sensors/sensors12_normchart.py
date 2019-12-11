import time
from src.sensors.utils import end, sendDataToTipboard, getTimeStr

NAME_OF_SENSORS = "norm_chart"
TILE_TEMPLATE = "norm_chart"
TILE_ID = "normjs_ex"


def executeScriptToGetData():
    return {
        "title": "My title",
        "description": "Some description",
        "plot_data": [[[1, 2], [4, 5.12], [5, 13.1], [6, 33.6], [10, 85.9], [11, 219.9]],
                      [[6, 2], [3, 5.12], [6.5, 13.1], [7.5, 33.6], [9, 85.9], [11, 219.9]]]
    }


def sonde12(isTest=False):
    print(f"{getTimeStr()} (+) Starting sensors 12", flush=True)
    start_time = time.time()
    data = executeScriptToGetData()
    tipboardAnswer = sendDataToTipboard(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)
    end(title=f"sensors12 -> {TILE_ID}", start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
