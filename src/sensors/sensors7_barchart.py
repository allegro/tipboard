import time, random
from src.sensors.utils import end, sendUpdateByApi, updateChartJS, COLOR_TAB


def buildTicks():
    return {'min': 0,
            'stepSize': 1,
            'fontColor': "#000",
            'fontSize': 14
            }


def buildGridline(isRandom):
    return {'color': random.choice(COLOR_TAB),
            'offsetGridLines': random.choice([False, True]) if isRandom else True,
            'display': random.choice([False, True]) if isRandom else True,
            'lineWidth': 2,
            'zeroLineColor': '#000',
            'zeroLineWidth': 2
            }


def updateMeta(isRandom=False):
    meta = {
        'legend': {'display': True, 'position': random.choice(['top', 'bottom', 'right', 'left'])},
        'scales': {
            'xAxes': [{'ticks': buildTicks()}, {'gridLines': buildGridline(isRandom), 'stacked': True}],
            'yAxes': [{'ticks': buildTicks()}, {'gridLines': buildGridline(isRandom), 'stacked': True}]
        }
    }
    return meta


def sonde7(tester=None, tile_id='barjs_ex', isHorizontal=False):
    TILE_TEMPLATE = 'bar_chart' if isHorizontal else 'vbar_chart'
    start_time = time.time()
    data = updateChartJS(nbrDataset=random.randrange(5, 9), nbrLabel=random.randrange(4, 6), colorTabIndataset=False)
    meta = updateMeta()
    tipboardAnswer = sendUpdateByApi(data=data, tileTemplate=TILE_TEMPLATE, tileId=tile_id, tester=tester, meta=meta)
    end(title=f'sensors7 -> {tile_id}', startTime=start_time, tipboardAnswer=tipboardAnswer, tileId=tile_id)
