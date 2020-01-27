import time
from src.sensors.utils import end, sendDataToTipboard, buildChartUpdateRandomly, getTimeStr


def sonde3(isTest=False):
    TILE_TEMPLATE = 'line_chart'
    TILE_ID = 'line_chartjs_ex'
    print(f'{getTimeStr()} (+) Starting sensors 3', flush=True)
    start_time = time.time()
    data = buildChartUpdateRandomly()
    tipboardAnswer = sendDataToTipboard(data=data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)
    end(title=f'sensors3 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
