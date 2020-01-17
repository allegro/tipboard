import time, random
from src.sensors.utils import end
from src.sensors.utils import sendDataToTipboard, getTimeStr, buildChartUpdateRandomly


def sonde2(isTest=False):
    TILE_ID = 'pie_chartjs_ex'
    print(f'{getTimeStr()} (+) Starting sensors 2', flush=True)
    start_time = time.time()
    data = buildChartUpdateRandomly(nbrDataset=random.randrange(1, 3), colorTabIndataset=True)
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='pie_chart', tile_id=TILE_ID, isTest=isTest)
    end(title=f'sensors2 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
