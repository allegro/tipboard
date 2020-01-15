import time, random
from src.sensors.utils import end, sendDataToTipboard, getTimeStr, buildChartUpdateRandomly
from src.tipboard.app.properties import COLOR_TAB


def sonde14(isTest=False):
    TILE_ID = 'radar_ex'
    print(f'{getTimeStr()} (+) Starting sensors 14', flush=True)
    start_time = time.time()
    nbrLabel = random.randrange(2, 4)
    data = [random.randrange(4, 11) for _ in range(nbrLabel)]
    data = buildChartUpdateRandomly(nbrDataset=random.randrange(2, 4), nbrLabel=nbrLabel, data=data)
    index = 0
    for dataset in data['datasets']:  # TODO: ADD THIS TO .JS not in sensors... for simplicity
        dataset['pointBorderColor'] = COLOR_TAB[index]
        dataset['pointBackgroundColor'] = 'rgba(255, 255, 255, 0.5)'
        dataset['fill'] = True
        index = index + 1
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='radar_chart', tile_id=TILE_ID, isTest=isTest)
    end(title=f'sensors14 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
