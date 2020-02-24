import time, random
from src.sensors.utils import end, sendUpdateByApi, COLOR_TAB


def sonde18(tester=None, tile_id='gauge_ex'):
    start_time = time.time()
    data = {
        'title': {'display': True, 'text': 'Gauge Demo'},
        'datasets': [
            {
                'backgroundColor': [COLOR_TAB[1], COLOR_TAB[4], COLOR_TAB[5]],
                'borderWidth': 0,
                'gaugeData': {
                    'value': random.randrange(5, 100),
                    'valueColor': COLOR_TAB[5]
                },
                'gaugeLimits': [0, 25, 50, 100]
            }
        ]
    }
    meta = {'labelFormat': '$'}
    tipboardAnswer = sendUpdateByApi(data=data, tileTemplate='gauge_chart', tileId=tile_id, tester=tester, meta=meta)
    end(title=f'sensors gauge_chart -> {tile_id}', startTime=start_time, tipboardAnswer=tipboardAnswer, tileId=tile_id)
