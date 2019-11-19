import requests, time
from src.tipboard.app.properties import TIPBOARD_URL
from src.sensors.utils import end, buildConfigTile
from src.tipboard.app.fake_data import getFakeText

NAME_OF_SENSORS = "text_exemple"
TILE_TEMPLATE = "text"
TILE_ID = "txt_ex"


def executeScriptToGetData(tile_id=None, tile_template=None):
    """ Simulate some actions for text tile exemple"""
    return getFakeText(tile_id=tile_id, template_name=tile_template)


def sendDataToTipboard(data=None, tile_template=None, tile_id="", isTest=False):
    configTile = buildConfigTile(tile_id=tile_id, tile_template=tile_template, data=data['data']['text'])
    if not isTest:
        res = requests.post(TIPBOARD_URL + "/push", data=configTile)
        print(f"{res} -> {tile_id}: {res.text}", flush=True)


def sonde1(isTest):
    start_time = time.time()
    data = executeScriptToGetData()
    sendDataToTipboard(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)
    end(title=f"sensors1 -> {TILE_ID}", start_time=start_time)
