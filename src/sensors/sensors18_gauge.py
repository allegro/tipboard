import time
from src.sensors.utils import end, sendUpdateByApi, COLOR_TAB


def sonde18(tester=None, tile_id='gauge_ex'):
    start_time = time.time()
    data = {
        'title': {'display': True, 'text': 'Gauge Demo'},
        'datasets': [
            {
                'borderWidth': 0,
                'gaugeData': {
                    'value': 36,
                    'valueColor': COLOR_TAB[5]
                },
                'gaugeLimits': [-10, 0, 8, 26, 31, 55],
                'backgroundColor': [COLOR_TAB[0], COLOR_TAB[8], COLOR_TAB[1], COLOR_TAB[4], COLOR_TAB[5]],
            }
        ]
    }
    meta = {'labelFormat': '°'}
    tipboardAnswer = sendUpdateByApi(data=data, tileTemplate='gauge_chart', tileId=tile_id, tester=tester, meta=meta)
    end(title=f'sensors gauge_chart -> {tile_id}', startTime=start_time, tipboardAnswer=tipboardAnswer, tileId=tile_id)
