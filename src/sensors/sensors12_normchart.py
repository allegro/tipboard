import time, random
from src.sensors.utils import end, sendDataToTipboard, getTimeStr

NAME_OF_SENSORS = 'norm_chart'
TILE_TEMPLATE = 'norm_chart'
TILE_ID = 'normjs_ex'


def executeScriptToGetData():
    labelLenght = random.randrange(9, 50)
    data = dict()
    data['title'] = {
        'text': 'NormChart sensors',
        'color': '#FFFFFF'
    }
    data['labels'] = [f'{i}' for i in range(1, labelLenght)]
    data['datasets'] = [
        {
            'label': 'Serie 1',
            'data': [random.randrange(100, 1000) for i in range(labelLenght)],
        },
        {
            'label': 'Serie 2',
            'data': [random.randrange(100, 1000) for i in range(labelLenght)],
        }
    ]
    return data


def sonde12(isTest=False):
    print(f'{getTimeStr()} (+) Starting sensors 12', flush=True)
    start_time = time.time()
    data = executeScriptToGetData()
    tipboardAnswer = sendDataToTipboard(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)
    end(title=f'sensors12 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
