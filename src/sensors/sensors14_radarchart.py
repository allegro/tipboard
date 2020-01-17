import time, random
from src.sensors.utils import end, sendDataToTipboard, getTimeStr, buildChartUpdateRandomly
from src.tipboard.app.properties import COLOR_TAB


def sonde14(isTest=False):
    TILE_ID = 'radar_ex'
    print(f'{getTimeStr()} (+) Starting sensors 14', flush=True)
    start_time = time.time()
    data = buildChartUpdateRandomly(nbrLabel=5, data=None)

    index = 0
    for dataset in data['datasets']:  # TODO: ADD THIS TO .JS not in sensors... for simplicity
        dataset['pointBorderColor'] = COLOR_TAB[index]
        dataset['pointBackgroundColor'] = 'rgba(255, 255, 255, 0.5)'
        dataset['fill'] = True
        index = index + 1
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='radar_chart', tile_id=TILE_ID, isTest=isTest)
    end(title=f'sensors14 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
# il faut add ces valeur(pointBorderColor) dans les fake buildGenericChart
# dans radar il n'y a plus que la serie 1 qui est affiché, meme lorsqu'il y en a plus
# il faut régler la pie_chart aussi
