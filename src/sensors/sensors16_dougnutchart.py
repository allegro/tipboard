import time, random
from src.sensors.utils import end, sendDataToTipboard, getTimeStr, buildChartUpdateRandomly


def sonde16(isTest=False):
    TILE_ID = 'doughnut_ex'
    print(f'{getTimeStr()} (+) Starting sensors 16', flush=True)
    start_time = time.time()
    data = buildChartUpdateRandomly(nbrDataset=random.randrange(1, 3), colorTabIndataset=True)
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='doughnut_chart', tile_id=TILE_ID, isTest=isTest)
    end(title=f'sensors3 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
