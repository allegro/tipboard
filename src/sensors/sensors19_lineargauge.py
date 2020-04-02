import time, random
from src.sensors.utils import end, sendUpdateByApi, updateChartJS
from src.tipboard.app.properties import COLOR_TAB


def sonde19(tester=None, tile_id='lgauge_ex'):
    start_time = time.time()
    data = updateChartJS(nbrDataset=3, nbrLabel=3, colorTabIndataset=False)
    nbrDataset = 3
    data = dict()
    data['datasets'] = list()
    offset = 9  # offset start at the end of width of center axis
    for idx in range(nbrDataset):
        offset = offset + 11
        data['datasets'].append(dict(label=f'Serie {idx}',
                                     backgroundColor=COLOR_TAB[idx],
                                     data=[random.randrange(100, 500)],
                                     offset=offset, width=10))
    answer = sendUpdateByApi(data=data, tileTemplate='linear_gauge_chart', tileId=tile_id, tester=tester)
    end(title=f'sensor19 -> -> {tile_id}', startTime=start_time, tipboardAnswer=answer, tileId=tile_id)
