import time, random
from src.sensors.utils import end, sendDataToTipboard, getTimeStr


def executeScriptToGetData():
    """ Simulate some actions for text tile exemple"""
    labelLenght = random.randrange(4, 11)
    data = dict()
    data['title'] = {
        'text': 'RadarChart sensors',
        'color': '#FFFFFF'
    }
    data['labels'] = [f'Label {i}' for i in range(1, labelLenght)]
    data['datasets'] = [
        {
            'label': 'Series 1',
            'fill': True,
            'backgroundColor': 'rgba(114, 191, 68, 0.8)',
            'borderColor': 'rgba(114, 191, 68, 0.8)',
            'pointBorderColor': 'rgba(114, 191, 68, 0.95)',
            'pointBackgroundColor': 'rgba(255, 255, 255, 0.5)',
            'data': [random.randrange(4, 30) for _ in range(labelLenght)]
        },
        {
            'label': 'Series 2',
            'fill': True,
            'backgroundColor': 'rgba(62, 149, 205, 0.8)',
            'borderColor': 'rgba(62, 149, 205, 0.8)',
            'pointBorderColor': 'rgba(62, 149, 205, 0.95)',
            'pointBackgroundColor': 'rgba(255, 255, 255, 0.5)',
            'data': [random.randrange(4, 30) for _ in range(labelLenght)]
        }
    ]

    return data


def sonde14(isTest=False):
    TILE_ID = 'radar_ex'
    print(f'{getTimeStr()} (+) Starting sensors 14', flush=True)
    start_time = time.time()
    data = executeScriptToGetData()
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='radar_chart', tile_id=TILE_ID, isTest=isTest)
    end(title=f'sensors3 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
