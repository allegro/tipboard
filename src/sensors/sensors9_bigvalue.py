import time, random
from src.sensors.utils import end, sendDataToTipboard, getTimeStr

NAME_OF_SENSORS = "big_value"
TILE_TEMPLATE = "big_value"
TILE_ID = "bv_ex"


def executeScriptToGetData():
    """ Simulate some actions for text tile exemple"""
    ulv = random.randrange(42, 420)
    llv = random.randrange(42, 420)
    urv = random.randrange(42, 420)
    lrv = ulv + llv + urv
    bv = lrv - random.randrange(42)
    return {
        "title": "Sensors title",
        "description": "Sensors description",
        "big-value": random.randrange(214, 514),
        "upper-left-label": "Critical:",
        "upper-left-value": ulv,
        "lower-left-label": "Major:",
        "lower-left-value": llv,
        "upper-right-label": "Minor:",
        "upper-right-value": urv,
        "lower-right-label": "All:",
        "lower-right-value": lrv
    }


def sonde9(isTest=False):
    print(f"{getTimeStr()} (+) Starting sensors 9", flush=True)
    start_time = time.time()
    data = executeScriptToGetData()
    tipboardAnswer = sendDataToTipboard(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)
    end(title=f"sensors9 -> {TILE_ID}", start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
