import time
from src.sensors.utils import end, sendUpdateByApi, updateChartJS
from src.tipboard.app.properties import COLOR_TAB


def sonde14(tester=None, tile_id='radar_ex'):
    start_time = time.time()
    data = updateChartJS(nbrLabel=5, data=None)
    index = 0
    for dataset in data['datasets']:  # TODO: ADD THIS TO .JS not in sensors... for simplicity
        dataset['pointBorderColor'] = COLOR_TAB[index]
        dataset['pointBackgroundColor'] = 'rgba(255, 255, 255, 0.5)'
        dataset['fill'] = True
        index = index + 1
    tipboardAnswer = sendUpdateByApi(data=data, tileTemplate='radar_chart', tileId=tile_id, tester=tester)
    end(title=f'sensors14 -> {tile_id}', startTime=start_time, tipboardAnswer=tipboardAnswer, tileId=tile_id)
