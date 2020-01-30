import time, random
from src.sensors.utils import end, sendUpdateByApi, updateChartJS


def sonde7(tester=None, tile_id='barjs_ex', isHorizontal=False):
    TILE_TEMPLATE = 'bar_chart' if isHorizontal else 'vbar_chart'
    start_time = time.time()
    data = updateChartJS(nbrDataset=random.randrange(2, 7), nbrLabel=random.randrange(1, 4), colorTabIndataset=False)
    tipboardAnswer = sendUpdateByApi(data=data, tileTemplate=TILE_TEMPLATE, tileId=tile_id, tester=tester)
    end(title=f'sensors7 -> {tile_id}', startTime=start_time, tipboardAnswer=tipboardAnswer, tileId=tile_id)
