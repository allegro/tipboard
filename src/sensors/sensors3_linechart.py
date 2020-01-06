import time, random
from src.sensors.utils import end, sendDataToTipboard, getTimeStr
from src.tipboard.app.properties import COLOR_TAB


def executeScriptToGetData():
    """ Simulate some actions for linechart tile exemple """
    nbrDataset = random.randrange(1, 5)
    nbrData = random.randrange(9, 20)
    data = dict()
    data['title'] = dict(text='LineChart sensors', color='#FFFFFF')
    data['labels'] = [f'{i}' for i in range(1, nbrData)]
    data['datasets'] = list()
    for index in range(nbrDataset):
        data['datasets'].append(
            dict(label=f'Serie {index + 1}',
                 data=[random.randrange(100, 1000) for i in range(nbrData)],
                 backgroundColor=COLOR_TAB[index], borderColor=COLOR_TAB[index]))
    print(f'{getTimeStr()} (+) Generated {nbrDataset} datasets with labels [{data["labels"]}]', flush=True)
    return data


def sonde3(isTest=False):
    TILE_TEMPLATE = 'line_chart'
    TILE_ID = 'line_chartjs_ex'
    print(f'{getTimeStr()} (+) Starting sensors 3', flush=True)
    start_time = time.time()
    data = executeScriptToGetData()
    tipboardAnswer = sendDataToTipboard(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)
    end(title=f'sensors3 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
