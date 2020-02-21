import time, random
from src.sensors.utils import end, sendUpdateByApi, updateChartJS
from src.tipboard.app.properties import COLOR_TAB


def sonde20(tester=None, tile_id='rgauge_ex'):
    start_time = time.time()
    data = updateChartJS(nbrDataset=3, nbrLabel=3, colorTabIndataset=False)
    nbrDataset = 1
    data = dict()
    data['datasets'] = list()
    maxValue = 100
    value = random.randrange(10, 100)
    for idx in range(nbrDataset):
        data['datasets'].append(dict(data=[value], label=f'Series {idx}'))
    meta = dict(domain=[0, maxValue], trackColor=COLOR_TAB[1], centerArea=dict(text=f'{value}%', backgroundImage=''))
    answer = sendUpdateByApi(data=data, tileTemplate='radial_gauge_chart', tileId=tile_id, tester=tester, meta=meta)
    end(title=f'sensor20 -> -> {tile_id}', startTime=start_time, tipboardAnswer=answer, tileId=tile_id)
