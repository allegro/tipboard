import requests, time, random
from src.tipboard.app.properties import TIPBOARD_URL
from src.sensors.utils import end, buildConfigTile, getTimeStr
from src.tipboard.app.FakeData.fake_data import getFakeText

NAME_OF_SENSORS = "text_exemple"
TILE_TEMPLATE = "text"
TILE_ID = "txt_ex"


def executeScriptToGetData(tile_id=None, tile_template=None):
    """ Replace getFakeText with your script to GET text tile data """
    return getFakeText(tile_id=tile_id, template_name=tile_template)


def sendDataToTipboard(data=None, tile_template=None, tile_id="", isTest=False):
    configTile = buildConfigTile(tile_id=tile_id, tile_template=tile_template, data=data['data']['text'])
    if not isTest:
        return requests.post(TIPBOARD_URL + "/push", data=configTile)


def sonde1(isTest):
    print(f"----------------------------------------------------------------------------------------------", flush=True)
    print(f"{getTimeStr()} (+) Starting sensors 1", flush=True)
    start_time = time.time()
    data = executeScriptToGetData()
    data['text'] = f'Last malware detedted: <br>' \
        f'<h2> {"".join([random.choice("0123456789abcdef") for x in range(32)])}</h2>'
    tipboardAnswer = sendDataToTipboard(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)
    end(title=f"sensors1 -> {TILE_ID}", start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
