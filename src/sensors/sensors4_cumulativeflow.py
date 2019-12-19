import time, random
from src.sensors.utils import end, sendDataToTipboard, getTimeStr

NAME_OF_SENSORS = "cumuleflow"
TILE_TEMPLATE = "cumulative_flow"
TILE_ID = "cfjs_ex"


# def executeScriptToGetData():
#     """ Simulate some actions for text tile exemple"""
#     label1 = {"label": "label 1", "series": [0, 0, 0, 0, 1, 1, 2, 2, 1, 1, 1, 0, 0, 2, 0]}
#     label2 = {"label": "label 2", "series": [0, 5, 0, 0, 1, 0, 0, 3, 0, 0, 0, 7, 8, 9, 1]}
#     return {"title": "My title:", "series_list": [label1, label2]}

def executeScriptToGetData():
    """ Simulate some actions for text tile exemple"""
    labelLenght = random.randrange(9, 50)
    data = dict()
    data['title'] = {
        "text": "LineChart sensors",
        "color": "#FFFFFF"
    }
    data['labels'] = [f"{i}" for i in range(1, labelLenght)]
    data['datasets'] = [
        {
            'label': 'Serie 1',
            'backgroundColor': 'rgba(114, 191, 68, 0.8)',
            'borderColor': 'rgba(114, 191, 68, 0.8)',
            'data': [random.randrange(200, 1000) for i in range(labelLenght)]
        },
        {
            'label': 'Serie 2',
            'backgroundColor': 'rgba(62, 149, 205, 0.8)',
            'borderColor': 'rgba(62, 149, 205, 0.8)',
            'data': [random.randrange(200, 1000) for i in range(labelLenght)]
        }

    ]
    print(data)
    return data


def sonde4(isTest=False):
    print(f"{getTimeStr()} (+) Starting sensors 4", flush=True)
    start_time = time.time()
    data = executeScriptToGetData()
    tipboardAnswer = sendDataToTipboard(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)
    end(title=f"sensors4 -> {TILE_ID}", start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
