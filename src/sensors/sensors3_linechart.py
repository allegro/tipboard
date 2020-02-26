import time
from src.sensors.utils import end, sendUpdateByApi, updateChartJS


def sonde3(tester=None, tile_id='line_chartjs_ex'):
    TILE_TEMPLATE = 'line_chart'
    start_time = time.time()
    data = updateChartJS()
    tipboardAnswer = sendUpdateByApi(data=data, tileTemplate=TILE_TEMPLATE, tileId=tile_id, tester=tester)
    end(title=f'sensors3 -> {tile_id}', startTime=start_time, tipboardAnswer=tipboardAnswer, tileId=tile_id)
