import time, random
from src.sensors.utils import end
from src.tipboard.app.FakeData.fake_data import getFakePieChart
from src.sensors.utils import sendDataToTipboard, getTimeStr

NAME_OF_SENSORS = "GET"
TILE_TEMPLATE = "pie_chart"
TILE_ID = "pie_chartjs_ex"


def executeScriptToGetData():
    """ Simulate some actions for text Pie chart exemple"""
    pieData = getFakePieChart(tile_id=TILE_ID, template_name=TILE_TEMPLATE)
    pieData['data']['title'] = 'Sensors title'
    value1 = random.randrange(10, 80)
    limit = 100 - value1
    value2 = random.randrange(10, limit)
    value3 = 100 - value2 - value1
    pieData['data']['labels'] = ["Fake 1", "Fake 2", "Fake 3"]
    pieData['data']['pie_data_value'] = [value1, value2, value3]
    return pieData


def sonde2(isTest=False):
    print(f"{getTimeStr()} (+) Starting sensors 2", flush=True)
    start_time = time.time()
    data = executeScriptToGetData()
    tipboardAnswer = sendDataToTipboard(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)
    end(title=f"sensors2 -> {TILE_ID}", start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
