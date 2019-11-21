import time
from src.sensors.utils import end
from src.sensors.utils import sendDataToTipboard

NAME_OF_SENSORS = "listing"
TILE_TEMPLATE = "listing"
TILE_ID = "listing_ex"


def executeScriptToGetData():
    """ Simulate some actions for text tile exemple"""
    return {
        "items":
            ["Leader: 5",
             "Product Owner: 0",
             "Scrum Master: 3",
             "Developer: 0"
             ]
    }


def sonde6(isTest):
    start_time = time.time()
    data = executeScriptToGetData()
    sendDataToTipboard(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)
    end(title=f"sensors6 -> {TILE_ID}", start_time=start_time)
