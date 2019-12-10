import time
from src.sensors.utils import end, sendDataToTipboard, getTimeStr

NAME_OF_SENSORS = "linechart"
TILE_TEMPLATE = "line_chart"
TILE_ID = "line_chartjs_ex"


# def executeScriptToGetData():
#     """ Simulate some actions for text tile exemple"""
#     line1 = [["23.09", 8326], ["24.09", 260630], ["25.09", 240933], ["26.09", 229639],
#              ["27.09", 190240], ["28.09", 125272], ["29.09", 3685]]
#     line2 = [["23.09", 3685], ["24.09", 125272], ["25.09", 190240], ["26.09", 229639],
#              ["27.09", 240933], ["28.09", 260630], ["29.09", 108326]]
#     return {
#         "subtitle": "Sensors line exemple",
#         "description": "Random value",
#         "series_list": [line1, line2]
#     }

def executeScriptToGetData():
    """ Simulate some actions for text tile exemple"""
    data = dict()
    data['title'] = {
        "text": "LineChart sensors",
        "color": "#FFFFFF"
    }
    data['labels'] = ["23.09", "24.09", "25.09", "26.09", "27.09", "28.09", "29.09"]
    data['datasets'] = [
        {
            'label': 'Serie 1',
            'backgroundColor': 'rgba(114, 191, 68, 0.8)',
            'data': [8326, 260630, 240933, 229639, 190240, 125272, 3685]
        },
        {
            'label': 'Serie 2',
            'backgroundColor': 'rgba(62, 149, 205, 0.8)',
            'data': [3685, 125272, 190240, 229639, 240933, 260630, 108326]
        }

    ]
    return data


def sonde3(isTest):
    print(f"{getTimeStr()} (+) Starting sensors 3", flush=True)
    start_time = time.time()
    data = executeScriptToGetData()
    tipboardAnswer = sendDataToTipboard(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)
    end(title=f"sensors3 -> {TILE_ID}", start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
