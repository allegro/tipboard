import time, random
from src.sensors.utils import end, sendDataToTipboard, getTimeStr, sendBVColor
from src.tipboard.app.properties import BACKGROUND_TAB


def executeScriptToGetData():
    """ Simulate some actions for text tile exemple """
    lv = random.randrange(1, 49)
    rl = random.randrange(1, 49)
    bv = lv + rl
    return {'title': 'Sensor title',
            'subtitle': 'Sensor subtitle',
            'big_value': f'{bv}%',
            'left_label': 'Random label 1', 'left_value': f'{lv}%',
            'right_label': 'Random label 2', 'right_value': f'{rl}%'}


def sonde5(isTest=False):
    TILE_ID = 'sp_ex'
    print(f'{getTimeStr()} (+) Starting sensors 5', flush=True)
    start_time = time.time()
    data = executeScriptToGetData()
    tipboardAnswer = sendDataToTipboard(tile_id=TILE_ID, data=data, tile_template='simple_percentage', isTest=isTest)
    fade = False if not random.randrange(0, 1) else True
    sendBVColor(tile_id=TILE_ID, color=BACKGROUND_TAB[random.randrange(0, 3)], fading=fade)
    end(title=f'sensors5 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
