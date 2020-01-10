import time, random
from src.sensors.utils import end, sendDataToTipboard, getTimeStr
from src.tipboard.app.properties import COLOR_TAB


def executeScriptToGetData():
    """ Simulate some actions for text tile exemple """
    labelLenght = random.randrange(2, 8)
    datasetLength = random.randrange(1, 3)
    if labelLenght % 2 != 0:
        datasetLength = 1
    data = dict()
    data['title'] = dict(text=f'{datasetLength} dataset', color='#FFFFFF', display=random.choice([True, False]))
    data['legend'] = dict(display=False if labelLenght > 6 else random.choice([True, False]))
    data['labels'] = [f'Serie {i + 1}' for i in range(labelLenght)]
    data['datasets'] = list()
    for _ in range(datasetLength):
        data['datasets'].append(
            dict(data=[random.randrange(100, 1000) for _ in range(labelLenght)],
                 backgroundColor=COLOR_TAB))
    print(f'{getTimeStr()} (+) Generated {datasetLength} datasets with labels [{data["labels"]}]', flush=True)
    return data


def sonde16(isTest=False):
    TILE_ID = 'doughnut_ex'
    print(f'{getTimeStr()} (+) Starting sensors 16', flush=True)
    start_time = time.time()
    data = executeScriptToGetData()
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='doughnut_chart', tile_id=TILE_ID, isTest=isTest)
    end(title=f'sensors3 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
