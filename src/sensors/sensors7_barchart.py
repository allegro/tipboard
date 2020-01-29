import time, random
from src.sensors.utils import end, sendDataToTipboard, getTimeStr, buildChartUpdateRandomly
from src.tipboard.app.properties import COLOR_TAB


def executeScriptToGetData():
    """ Simulate some actions for text tile exemple """
    nbrDataset = random.randrange(2, 7)
    nbrLabel = random.randrange(1, 4)
    data = dict()
    data['title'] = dict(text=f'{nbrDataset} dataset & {nbrLabel} labels',
                         color='#FFFFFF', display=random.choice([True, False]))
    data['legend'] = dict(display=False if nbrDataset > 6 else random.choice([True, False]))
    data['labels'] = [f'{i + 1}/{nbrLabel}' for i in range(nbrLabel)]
    data['datasets'] = list()
    for index in range(nbrDataset):
        data['datasets'].append(dict(label=f'Dataset {index + 1}', backgroundColor=COLOR_TAB[index],
                                     data=[random.randrange(100, 1000) for _ in range(nbrLabel)]))
    return data


def sonde7(isTest=False, isHorizontal=False):
    TILE_TEMPLATE = 'bar_chart' if isHorizontal else 'vbar_chart'
    TILE_ID = 'barjs_ex' if isHorizontal else 'vbarjs_ex'
    print(f'{getTimeStr()} (+) Starting sensors 7', flush=True)
    start_time = time.time()
#    data = executeScriptToGetData()
    data = buildChartUpdateRandomly(nbrDataset=random.randrange(2, 7), nbrLabel=random.randrange(1, 4), colorTabIndataset=False)
    tipboardAnswer = sendDataToTipboard(data=data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)
    end(title=f'sensors7 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
