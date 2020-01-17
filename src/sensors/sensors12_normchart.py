import time
from src.sensors.utils import end, sendDataToTipboard, buildChartUpdateRandomly, getTimeStr


def sonde12(isTest=False):
    TILE_ID = 'normjs_ex'
    start_time = time.time()
    print(f'{getTimeStr()} (+) Starting sensors 3', flush=True)
    data = buildChartUpdateRandomly(colorTabIndataset=False)
    tipboardAnswer = sendDataToTipboard(tile_template='norm_chart', tile_id=TILE_ID, data=data, isTest=isTest)
    end(title=f'sensors12 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
