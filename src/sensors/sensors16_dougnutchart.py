import time, random
from src.sensors.utils import end, sendDataToTipboard, getTimeStr
from src.tipboard.app.properties import COLOR_TAB

NAME_OF_SENSORS = 'doughnut sensors'
TILE_TEMPLATE = 'doughnut_chart'
TILE_ID = 'doughnut_ex'


def executeScriptToGetData():
    ''' Simulate some actions for text tile exemple'''
    datasetLength = random.randrange(2, 8)
    data = dict()
    data['title'] = dict(text='Doughnut sensors', color='#FFFFFF', display=True)
    data['labels'] = [f'Serie {i + 1}' for i in range(datasetLength)]
    data['datasets'] = list()
#    for index in range(datasetLength):
    data['datasets'].append(
        dict(data=[random.randrange(100, 1000) for i in range(datasetLength)],
             backgroundColor=COLOR_TAB))
    return data


def sonde16(isTest=False):
    print(f'{getTimeStr()} (+) Starting sensors 16', flush=True)
    start_time = time.time()
    data = executeScriptToGetData()
    tipboardAnswer = sendDataToTipboard(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)
    end(title=f'sensors3 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
