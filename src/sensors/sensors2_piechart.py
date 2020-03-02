import time, random
from src.sensors.utils import end
from src.sensors.utils import sendUpdateByApi, updateChartJS


def sonde2(tester=None, tile_id='pie_chartjs_ex'):
    start_time = time.time()
    data = updateChartJS(nbrDataset=1, colorTabIndataset=True)
    tipboardAnswer = sendUpdateByApi(data=data, tileTemplate='pie_chart', tileId=tile_id, tester=tester)
    end(title=f'sensors2 -> {tile_id}', startTime=start_time, tipboardAnswer=tipboardAnswer, tileId=tile_id)
