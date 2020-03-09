import requests, time, random, lorem, json
from src.tipboard.app.properties import TIPBOARD_URL
from src.sensors.utils import end
from src.tipboard.app.DefaultData.defaultTileControler import getDefaultText


def executeScriptToGetData(tile_id=None, tile_template=None):
    """ Replace getFakeText with your script to GET text tile data """
    tile = getDefaultText(tile_id=tile_id, template_name=tile_template)
    tile['data']['text'] = '\n'.join([lorem.sentence() for _ in range(6)])
    return tile


def sendDataToTipboard(data=None, tile_template=None, tile_id='', tester=None):
    configTile = dict(tile_id=tile_id, tile_template=tile_template, data=json.dumps(data['data']['text']))
    if tester is None:
        return requests.post(TIPBOARD_URL + '/push', data=configTile)
    else:
        return tester.fakeClient.post(TIPBOARD_URL + '/push', data=configTile)


def sonde1(tester=None, tile_id='txt_ex', tile_template='text'):
    start_time = time.time()
    data = executeScriptToGetData()
    data['text'] = f'Last malware detedted: <br>' \
        f'<h2> {"".join([random.choice("0123456789abcdef") for x in range(32)])}</h2>'
    tipboardAnswer = sendDataToTipboard(data, tile_template=tile_template, tile_id=tile_id, tester=tester)
    end(title=f'sensors1 -> {tile_id}', startTime=start_time, tipboardAnswer=tipboardAnswer, tileId=tile_id)
