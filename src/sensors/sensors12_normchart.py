import time, random
from src.sensors.utils import end, sendDataToTipboard, getTimeStr
from src.tipboard.app.properties import COLOR_TAB


def executeScriptToGetData():
    datasetLength = random.randrange(1, 4)
    nbrData = random.randrange(5, 15)
    data = dict()
    data['title'] = dict(text='NormChart sensors', color='#FFFFFF', display=True)
    data['labels'] = [f'{i}' for i in range(1, nbrData)]
    data['datasets'] = list()
    for index in range(datasetLength):
        data['datasets'].append(
            dict(label=f'Serie {index + 1}',
                 data=[random.randrange(100, 1000) for _ in range(nbrData)],
                 borderColor=COLOR_TAB[index]))
    print(f'{getTimeStr()} (+) Generated {datasetLength} datasets with labels [{data["labels"]}]', flush=True)
    return data


def sonde12(isTest=False):
    TILE_ID = 'normjs_ex'
    start_time = time.time()
    data = executeScriptToGetData()
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='norm_chart', tile_id=TILE_ID, isTest=isTest)
    end(title=f'sensors12 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
