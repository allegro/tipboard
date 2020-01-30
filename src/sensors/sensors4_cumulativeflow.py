import time
from src.sensors.utils import end, sendUpdateByApi, updateChartJS


def sonde4(tester=None, tile_id='cfjs_ex'):
    start_time = time.time()
    data = updateChartJS()
    tipboardAnswer = sendUpdateByApi(data=data, tileTemplate='cumulative_flow', tileId=tile_id, tester=tester)
    end(title=f'sensors4 -> {tile_id}', startTime=start_time, tipboardAnswer=tipboardAnswer, tileId=tile_id)
