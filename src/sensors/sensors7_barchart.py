import time, random
from src.sensors.utils import end, sendDataToTipboard, getTimeStr
from src.tipboard.app.properties import COLOR_TAB


def executeScriptToGetData():
    ''' Simulate some actions for text tile exemple'''
    labelLenght = random.randrange(2, 4)
    nbrData = random.randrange(1, 4)
    data = dict()
    data['title'] = dict(text=f'{labelLenght} label by sensors', color='#FFFFFF', display=random.choice([True, False]))
    data['legend'] = dict(display=False if labelLenght > 6 else random.choice([True, False]))
    data['labels'] = [f'{i}' for i in range(1, nbrData)]
    data['datasets'] = list()
    for index in range(labelLenght):
        newDataset = {
            'label': f'Serie {index + 1}',
            'data': [random.randrange(100, 1000) for i in range(nbrData)],
            'backgroundColor': COLOR_TAB[index]
        }
        data['datasets'].append(newDataset)
    return data


def sonde7(isTest=False, isHorizontal=False):
    TILE_TEMPLATE = 'bar_chart' if isHorizontal else 'vbar_chart'
    TILE_ID = 'barjs_ex' if isHorizontal else 'vbarjs_ex'
    print(f'{getTimeStr()} (+) Starting sensors 7', flush=True)
    start_time = time.time()
    data = executeScriptToGetData()
    tipboardAnswer = sendDataToTipboard(data=data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)
    end(title=f'sensors7 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
