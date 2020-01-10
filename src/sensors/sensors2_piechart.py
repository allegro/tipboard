import time, random
from src.sensors.utils import end
from src.tipboard.app.FakeData.fake_data import getFakePieChart
from src.sensors.utils import sendDataToTipboard, getTimeStr


def executeScriptToGetData(TILE_ID="ex_pie", TILE_TEMPLATE='pie_chart'):
    """ Simulate some actions for text Pie chart exemple"""
    pieData = getFakePieChart(tile_id=TILE_ID, template_name=TILE_TEMPLATE)
    labelLenght = random.randrange(2, 5)
    pieData['data']['title'] = 'Sensors title'
    pieData['title'] = dict(text=f'by sensors', color='#FFFFFF', display=random.choice([True, False]))
    pieData['legend'] = dict(display=False if labelLenght > 6 else random.choice([True, False]))
    pieData['labels'] = [f"Label {i}" for i in range(1, labelLenght)]
    pieData['data']['pie_data_value'] = [random.randrange(4, 50) for i in range(labelLenght)]
    return pieData


def sonde2(isTest=False):
    TILE_ID = 'pie_chartjs_ex'
    print(f'{getTimeStr()} (+) Starting sensors 2', flush=True)
    start_time = time.time()
    data = executeScriptToGetData(TILE_ID, 'pie_chart')
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='pie_chart', tile_id=TILE_ID, isTest=isTest)
    end(title=f'sensors2 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
