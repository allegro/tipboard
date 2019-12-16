import time, random
from src.sensors.utils import end, sendDataToTipboard, getTimeStr

NAME_OF_SENSORS = "norm_chart"
TILE_TEMPLATE = "norm_chart"
TILE_ID = "normjs_ex"


def executeScriptToGetData():
    # return {
    #     "title": "My title",
    #     "description": "Some description",
    #     "plot_data": [[[1, 2], [4, 5.12], [5, 13.1], [6, 33.6], [10, 85.9], [11, 219.9]],
    #                   [[6, 2], [3, 5.12], [6.5, 13.1], [7.5, 33.6], [9, 85.9], [11, 219.9]]]
    # }
    labelLenght = random.randrange(9, 50)
    data = dict()
    data['title'] = {
        "text": "NormChart sensors",
        "color": "#FFFFFF"
    }
    data['labels'] = [f"{i}" for i in range(1, labelLenght)]
    data['datasets'] = [
        {
            'label': 'Serie 1',
            'backgroundColor': 'rgba(114, 191, 68, 0.8)',
            'data': [random.randrange(100, 1000) for i in range(labelLenght)]
        },
        {
            'label': 'Serie 2',
            'backgroundColor': 'rgba(62, 149, 205, 0.8)',
            'data': [random.randrange(100, 1000) for i in range(labelLenght)]
        }

    ]
    return data


def sonde12(isTest=False):
    print(f"{getTimeStr()} (+) Starting sensors 12", flush=True)
    start_time = time.time()
    data = executeScriptToGetData()
    tipboardAnswer = sendDataToTipboard(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)
    end(title=f"sensors12 -> {TILE_ID}", start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)

# tu implemantes la sensors norm_chart
# inspirait de la line_chart qui fonctionne
# tu n'arrives pas à update le redis, car tu

#   File "/home/the-maux/tipboard/src/tipboard/app/views/api.py", line 112, in update_tile_data
#     previousData[key] = value
# TypeError: 'str' object does not support item assignment
