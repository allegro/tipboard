import time
from src.sensors.utils import end, sendDataToTipboard, getTimeStr, buildChartUpdateRandomly


def sonde15(isTest=False):
    print(f'{getTimeStr()} (+) Starting sensors 15', flush=True)
    start_time = time.time()
    data = buildChartUpdateRandomly(nbrDataset=1, colorTabIndataset=True)
    answer = sendDataToTipboard(data=data, tile_template='polararea_chart', tile_id='polararea_ex', isTest=isTest)
    end(title=f'sensors3 -> polararea_ex', start_time=start_time, tipboardAnswer=answer, TILE_ID='polararea_ex')
