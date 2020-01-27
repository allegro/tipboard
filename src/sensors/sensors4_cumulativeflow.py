import time
from src.sensors.utils import end, sendDataToTipboard, getTimeStr, buildChartUpdateRandomly


def sonde4(isTest=False):
    TILE_ID = 'cfjs_ex'
    print(f'{getTimeStr()} (+) Starting sensors 4', flush=True)
    start_time = time.time()
    data = buildChartUpdateRandomly()
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='cumulative_flow', tile_id=TILE_ID, isTest=isTest)
    end(title=f'sensors4 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
