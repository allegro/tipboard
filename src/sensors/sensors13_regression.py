import json, requests, time, random
from src.tipboard.app.properties import TIPBOARD_URL
from src.sensors.utils import end
from src.tipboard.app.FakeData.fake_data import getFakePieChart

NAME_OF_SENSORS = "GET"
TILE_TEMPLATE = "pie_chart"
TILE_ID = "pie_ex"


def getDataLikeTipboard2():
    """ Simulate some actions for text Pie chart exemple"""
    pieData = getFakePieChart(tile_id=TILE_ID, template_name=TILE_TEMPLATE)
    pieData['data']['title'] = 'Sensors title'
    value1 = random.randrange(10, 80)
    limit = 100 - value1
    value2 = random.randrange(10, limit)
    value3 = 100 - value2 - value1
    pieData['data']['pie_data_value'] = [value1, value2, value3]
    pieData['data']['labels'] = ["Fake 1", "Fake 2", "Fake 3"]
    return pieData


def sendDataToTipboard2(data=None, tile_template=None, tile_id="", isTest=False):
    configTile = {
        "tile": tile_template,  # tile_template name
        "key": tile_id,  # tile_template name
        "data": json.dumps(data)
    }
    if not isTest:
        res = requests.post(TIPBOARD_URL + "/push", data=configTile)
        print(f"{res} -> {tile_id}: {res.text}", flush=True)


def getDataLikeTipboard1():
    """ Simulate some actions for text tile exemple"""
    return {
        "title": "My title",
        "pie_data": [["Pie 1", 25],
                     ["Pie 2", 25],
                     ["Pie 3", 50]]
    }


def sendDataToTipboard1(data=None, tile_template=None, tile_id="", isTest=False):
    configTile = {
        "tile": tile_template,  # tile_template name
        "key": tile_id,  # tile_template name
        "data": json.dumps(data)
    }
    res = requests.post(TIPBOARD_URL + "/push", data=configTile)
    print(f"{res} -> {tile_id}: {res.text}", flush=True)


def sonde13(isTest=False):
    """ Test if update sensors like tipboard1.0 is still working on tipboard2.0 """
    start_time = time.time()
    if not isTest:
        data = getDataLikeTipboard1()
        sendDataToTipboard1(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)

        data = getDataLikeTipboard2()
        sendDataToTipboard2(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)

    end(title=f"sensors Test Regression -> {TILE_ID}", start_time=start_time)

# Tester si la maniere de push en Tipboard 1.0 est toujours ok
