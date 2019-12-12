import time, random
from src.sensors.utils import end, sendDataToTipboard, getTimeStr

NAME_OF_SENSORS = "radar_chart"
TILE_TEMPLATE = "radar_chart"
TILE_ID = "radar_ex"

# STATIC_DATA = 'data': [8326, 260630, 240933, 229639, 190240, 125272, 3685]
# STATIC_DATA = 'data': [3685, 125272, 190240, 229639, 240933, 260630, 108326]


def executeScriptToGetData():
    """ Simulate some actions for text tile exemple"""
    labelLenght = random.randrange(3, 11)
    data = dict()
    data['title'] = {
        "text": "RadarChart sensors",
        "color": "#FFFFFF"
    }
    data['labels'] = [f"Label {i}" for i in range(1, labelLenght)]
    data['datasets'] = [
      {
        "label": "Series 1",
        "fill": True,
        "backgroundColor": "rgba(114, 191, 68, 0.8)",
        "borderColor": "rgba(114, 191, 68, 0.8)",
        "pointBorderColor": "rgba(114, 191, 68, 0.95)",
        "pointBackgroundColor": "rgba(255, 255, 255, 0.5)",
        "data": [random.randrange(4, 30) for i in range(labelLenght)]
      },
      {
        "label": "Series 2",
        "fill": True,
        "backgroundColor": "rgba(62, 149, 205, 0.8)",
        "borderColor": "rgba(62, 149, 205, 0.8)",
        "pointBorderColor": "rgba(62, 149, 205, 0.95)",
        "pointBackgroundColor": "rgba(255, 255, 255, 0.5)",
        "data": [random.randrange(4, 30) for i in range(labelLenght)]
      }
    ]
    print(data)
    return data


def sonde14(isTest=False):
    print(f"{getTimeStr()} (+) Starting sensors 14", flush=True)
    start_time = time.time()
    data = executeScriptToGetData()
    tipboardAnswer = sendDataToTipboard(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)
    end(title=f"sensors3 -> {TILE_ID}", start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
