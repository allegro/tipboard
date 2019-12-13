import time, random
from src.sensors.utils import end, sendDataToTipboard, getTimeStr

NAME_OF_SENSORS = "linechart"
TILE_TEMPLATE = "line_chart"
TILE_ID = "line_chartjs_ex"

# STATIC_DATA = 'data': [8326, 260630, 240933, 229639, 190240, 125272, 3685]
# STATIC_DATA = 'data': [3685, 125272, 190240, 229639, 240933, 260630, 108326]


def executeScriptToGetData():
    """ Simulate some actions for text tile exemple"""
    labelLenght = random.randrange(9, 100)
    data = dict()
    data['title'] = {
        "text": "LineChart sensors",
        "color": "#FFFFFF"
    }
    data['labels'] = [f"{i}h" for i in range(9, labelLenght)]
    data['datasets'] = [
        {
            'label': 'Serie 1',
            'backgroundColor': 'rgba(114, 191, 68, 0.8)',
            'data': [random.randrange(500, 1000) for i in range(labelLenght)]
        },
        {
            'label': 'Serie 2',
            'backgroundColor': 'rgba(62, 149, 205, 0.8)',
            'data': [random.randrange(500, 1000) for i in range(labelLenght)]
        }

    ]
    print(data)
    return data


def sonde3(isTest=False):
    print(f"{getTimeStr()} (+) Starting sensors 3", flush=True)
    start_time = time.time()
    data = executeScriptToGetData()
    tipboardAnswer = sendDataToTipboard(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)
    end(title=f"sensors3 -> {TILE_ID}", start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
