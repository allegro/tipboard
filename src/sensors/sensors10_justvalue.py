import time, random
from src.sensors.utils import end, sendDataToTipboard, getTimeStr


def executeScriptToGetData():
    """ Simulate some actions for text tile exemple """
    return {
        'title': 'Sensors title',
        'description': 'Sensors description',
        'just-value': random.randrange(0, 100)
    }


def sonde10(isTest=False):
    TILE_ID = 'jv_ex'
    print(f'{getTimeStr()} (+) Starting sensors 10', flush=True)
    start_time = time.time()
    data = executeScriptToGetData()
    tipboardAnswer = sendDataToTipboard(data, tile_template='just_value', tile_id=TILE_ID, isTest=isTest)
    end(title=f'sensors10 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
