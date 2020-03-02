import time, random
from src.sensors.utils import end, sendUpdateByApi
from src.tipboard.app.properties import BACKGROUND_TAB


def executeScriptToGetData():
    """ Simulate some actions for text tile exemple """
    lv = random.randrange(1, 49)
    rl = random.randrange(1, 49)
    bv = lv + rl
    return {'title': random.choice(['Sensors title', None]),
            'subtitle': random.choice(['Sensors description', None]),
            'big_value': f'{bv}%',
            'left_label': 'Random label 1', 'left_value': f'{lv}%',
            'right_label': 'Random label 2', 'right_value': f'{rl}%'}


def sonde5(tester=False, tile_id='sp_ex'):
    start_time = time.time()
    data = executeScriptToGetData()
    meta = dict(big_value_color=BACKGROUND_TAB[random.randrange(0, 3)], fading_background=random.choice([False, True]))
    tipboardAnswer = sendUpdateByApi(tileId=tile_id, data=data, tileTemplate='simple_percentage',
                                     tester=tester, meta=meta)
    end(title=f'sensors5 -> {tile_id}', startTime=start_time, tipboardAnswer=tipboardAnswer, tileId=tile_id)
