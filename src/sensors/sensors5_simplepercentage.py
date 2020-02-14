import time, random
from src.sensors.utils import end, sendUpdateByApi


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


def sonde5(tester=False, tile_id='sp_ex'):
    start_time = time.time()
    data = executeScriptToGetData()
    tipboardAnswer = sendUpdateByApi(tileId=tile_id, data=data, tileTemplate='simple_percentage', tester=tester)
    # TODO: Ajouter les meta
    end(title=f'sensors5 -> {tile_id}', startTime=start_time, tipboardAnswer=tipboardAnswer, tileId=tile_id)
