import time, random
from src.sensors.utils import end, sendDataToTipboard, getTimeStr, buildChartUpdateRandomly


def sonde17(isTest=False):
    TILE_ID = 'hal_doughnut_ex'
    print(f'{getTimeStr()} (+) Starting sensors 17', flush=True)
    start_time = time.time()
    data = buildChartUpdateRandomly(nbrDataset=random.randrange(1, 3), colorTabIndataset=True)
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='half_doughnut_chart', tile_id=TILE_ID, isTest=isTest)
    end(title=f'sensors17 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
