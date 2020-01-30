import time, random
from src.sensors.utils import end
from src.sensors.utils import sendUpdateByApi, getTimeStr, updateChartJS
from src.tipboard.app.properties import LOG


def sonde2(tester=None, tile_id='pie_chartjs_ex'):
    if LOG:
        print(f'{getTimeStr()} (+) Starting sensors 2', flush=True)
    start_time = time.time()
    data = updateChartJS(nbrDataset=random.randrange(1, 3), colorTabIndataset=True)
    tipboardAnswer = sendUpdateByApi(data=data, tileTemplate='pie_chart', tileId=tile_id, tester=tester)
    end(title=f'sensors2 -> {tile_id}', startTime=start_time, tipboardAnswer=tipboardAnswer, tileId=tile_id)
