import time
from src.sensors.utils import end, sendUpdateByApi, updateChartJS


def sonde15(tester=None, tile_id='polararea_ex'):
    start_time = time.time()
    data = updateChartJS(nbrDataset=1, colorTabIndataset=True)
    meta = {
        "scale": {
            "ticks": {
                "display": False
            }
        }
    }
    answer = sendUpdateByApi(data=data, tileTemplate='polararea_chart', tileId=tile_id, meta=meta, tester=tester)
    end(title=f'sensor15 -> -> {tile_id}', startTime=start_time, tipboardAnswer=answer, tileId=tile_id)
