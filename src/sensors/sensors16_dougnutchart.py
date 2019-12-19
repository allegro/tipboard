import time, random
from src.sensors.utils import end, sendDataToTipboard, getTimeStr

NAME_OF_SENSORS = 'doughnut sensors'
TILE_TEMPLATE = 'doughnut_chart'
TILE_ID = 'doughnut_ex'


def executeScriptToGetData():
    ''' Simulate some actions for text tile exemple'''
    labelLenght = random.randrange(3, 5)
    data = dict()
    data['title'] = {
        'text': 'NormChart sensors',
        'color': '#FFFFFF'
    }
    data['labels'] = [f'label {i}' for i in range(1, labelLenght)]
    data['title'] = {'display': True, 'text': 'Doughnut Sensors'}
    data['datasets'] = [
        {
            'data': [random.randrange(20, 50) for i in range(labelLenght)]
        }
    ]
    return data


def sonde16(isTest=False):
    print(f'{getTimeStr()} (+) Starting sensors 16', flush=True)
    start_time = time.time()
    data = executeScriptToGetData()
    tipboardAnswer = sendDataToTipboard(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)
    end(title=f'sensors3 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
