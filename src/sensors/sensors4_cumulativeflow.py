import time, random
from src.sensors.utils import end, sendDataToTipboard, getTimeStr
from src.tipboard.app.properties import COLOR_TAB


def executeScriptToGetData():
    """ Simulate some actions for text tile exemple """
    datasetLength = random.randrange(1, 3)
    labelLenght = random.randrange(8, 15)
    data = dict()
    data['title'] = dict(text='Cumulative sensors', color='#FFFFFF')
    data['labels'] = [f"{i}" for i in range(1, labelLenght)]
    data['datasets'] = list()
    for index in range(datasetLength):
        data['datasets'].append(
            dict(label=f'Serie {index + 1}',
                 data=[random.randrange(200, 1000) for _ in range(labelLenght)],
                 borderColor=COLOR_TAB[index], backgroundColor=COLOR_TAB[index]))
    print(f'{getTimeStr()} (+) Generated {datasetLength} datasets with labels [{data["labels"]}]', flush=True)
    return data


def sonde4(isTest=False):
    TILE_ID = 'cfjs_ex'
    print(f'{getTimeStr()} (+) Starting sensors 4', flush=True)
    start_time = time.time()
    data = executeScriptToGetData()
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='cumulative_flow', tile_id=TILE_ID, isTest=isTest)
    end(title=f'sensors4 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
