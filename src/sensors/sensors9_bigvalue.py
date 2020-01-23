import time, random
from src.sensors.utils import end, sendDataToTipboard, getTimeStr, sendBVColor
from src.tipboard.app.properties import BACKGROUND_TAB


def executeScriptToGetData():
    """ Simulate some actions for text tile exemple """
    ulv = random.randrange(42, 420)
    llv = random.randrange(42, 420)
    urv = random.randrange(42, 420)
    lrv = ulv + llv + urv
    return {
        'title': 'Sensors title',
        'description': 'Sensors description',
        'big-value': random.randrange(214, 514),
        'upper-left-label': 'Critical:',
        'upper-left-value': ulv,
        'lower-left-label': 'Major:',
        'lower-left-value': llv,
        'upper-right-label': 'Minor:',
        'upper-right-value': urv,
        'lower-right-label': 'All:',
        'lower-right-value': lrv
    }


def sonde9(isTest=False):
    TILE_ID = 'bv_ex'
    print(f'{getTimeStr()} (+) Starting sensors 9', flush=True)
    start_time = time.time()
    data = executeScriptToGetData()
    meta = dict(big_value_color=BACKGROUND_TAB[random.randrange(0, 3)],
                fading_background=random.choice([False, True]))
    tipboardAnswer = sendDataToTipboard(tile_id=TILE_ID, data=data, tile_template='big_value', isTest=isTest, meta=meta)
    end(title=f'sensors9 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
