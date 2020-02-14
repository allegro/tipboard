import time, random
from src.sensors.utils import end, sendUpdateByApi
from src.tipboard.app.properties import BACKGROUND_TAB


def executeScriptToGetData():
    """ Simulate some actions for text tile exemple """
    return {
        'title': 'Sensors title',
        'description': 'Sensors description',
        'just-value': random.randrange(0, 100)
    }


def sonde10(tester=False, tile_id='jv_ex'):
    start_time = time.time()
    data = executeScriptToGetData()
    meta = dict(big_value_color=BACKGROUND_TAB[random.randrange(0, 3)], fading_background=random.choice([False, True]))
    tipboardAnswer = sendUpdateByApi(tileId=tile_id, data=data, tileTemplate='just_value', meta=meta, tester=tester)
    end(title=f'sensors10 -> {tile_id}', startTime=start_time, tipboardAnswer=tipboardAnswer, tileId=tile_id)
