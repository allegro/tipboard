import time, random
from src.sensors.utils import end, sendDataToTipboard, getTimeStr
from src.tipboard.app.properties import COLOR_TAB


def executeScriptToGetData():
    """ Simulate some actions for text tile exemple """
    labelLenght = 1
    nbrData = random.randrange(3, 7)
    data = dict()
    data['title'] = dict(text='PolarChart sensors', color='#FFFFFF')
    data['labels'] = [f'Label {i}' for i in range(1, nbrData)]
    data['datasets'] = list()
    for index in range(labelLenght):
        data['datasets'].append(
            dict(labels=f'Serie {index + 1}',
                 data=[random.randrange(100, 1000) for i in range(1, nbrData)],
                 backgroundColor=COLOR_TAB))
    return data


def sonde15(isTest=False):
    print(f'{getTimeStr()} (+) Starting sensors 15', flush=True)
    start_time = time.time()
    data = executeScriptToGetData()
    tipboardAnswer = sendDataToTipboard(data, tile_template='polararea_chart', tile_id='polararea_ex', isTest=isTest)
    end(title=f'sensors3 -> polararea_ex',
        start_time=start_time,
        tipboardAnswer=tipboardAnswer,
        TILE_ID='polararea_ex')
