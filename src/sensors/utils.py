import datetime, json, requests, time, random
from src.tipboard.app.properties import TIPBOARD_URL, DEBUG, COLOR_TAB


def printEndOfTipboardCall(tipboardAnswer, TILE_ID):
    if tipboardAnswer is not None:
        print(f'POST tile:{TILE_ID} tipboard/push => ({str(tipboardAnswer.status_code)}): ', flush=True)
    else:
        print(f'POST tile:{TILE_ID} tipboard/push => (FAILED HTTP CONNECT): ', flush=True)


def end(title=None, start_time=None, tipboardAnswer=None, TILE_ID=None):
    """ Eazy way to end sensors, print the action time & http answer of tipboard """
    printEndOfTipboardCall(tipboardAnswer, TILE_ID)
    duration = time.time() - start_time
    m = str(duration / 60)[:str(duration / 60).index('.')]
    s = str(duration % 60)[:str(duration % 60).index('.')]
    if m == '0':
        print(f'{getTimeStr()}-{title}: executed script in {s} seconds', flush=True)
    else:
        print(f'{getTimeStr()}-{title}: executed script in {m}:{s}', flush=True)
    print(f'----------------------------------------------------------------------------------------------', flush=True)


def getTimeStr():
    """ Eazy way to get in str, time for log """
    return datetime.datetime.now().strftime('%Hh%M')


def sendBVColor(color, tile_id, fading=False, isTest=False):  # pragma: no cover
    """ Modify meta of tile: update the color and/or fading of a specific tile """
    var = dict(value=json.dumps({'big_value_color': color, 'fading_background': fading}))
    if not isTest:
        res = requests.post(TIPBOARD_URL + '/tileconfig/' + tile_id, data=var)
        if DEBUG:
            print(f'{res}: color -> {tile_id}', flush=True)


def testTipboardUpdate(checker, fake_client, TILE_ID, data):
    configTile = dict(tile_id=TILE_ID, tile_template='pie_chart', data=json.dumps(data))
    tipboardAnswer = fake_client.post(TIPBOARD_URL + '/push', configTile)
    checker.assertTrue(tipboardAnswer.status_code == 200)


def sendDataToTipboard(tile_id=None, data=None, tile_template=None, isTest=False, meta=None):
    configTile = dict(tile_id=tile_id, tile_template=tile_template, data=json.dumps(data))
    if meta is not None:
        configTile['meta'] = json.dumps(meta)
    print(f"{configTile}")
    if not isTest:
        return requests.post(TIPBOARD_URL + '/push', data=configTile)


def buildChartUpdateRandomly(nbrDataset=None, nbrLabel=None, colorTabIndataset=False, data=None):
    nbrDataset = random.randrange(1, 5) if nbrDataset is None else nbrDataset
    nbrLabel = random.randrange(2, 13) if nbrLabel is None else nbrLabel
    tileData = dict()
    tileData['title'] = dict(text=f'{nbrDataset} dataset & {nbrLabel - 1} labels',
                             color='#FFFFFF',
                             display=random.choice([True, False]))
    tileData['legend'] = dict(display=False if nbrDataset > 6 else random.choice([True, False]))
    tileData['labels'] = [f'{i}' for i in range(nbrLabel)]
    tileData['datasets'] = list()
    for index in range(nbrDataset):
        tileData['datasets'].append(
            dict(label=f'Serie {index + 1}',
                 data=[random.randrange(100, 1000) for _ in range(nbrLabel)] if data is None else data,
                 backgroundColor=COLOR_TAB[index] if colorTabIndataset is False else COLOR_TAB,
                 borderColor=COLOR_TAB[index] if colorTabIndataset is False else '#525252'))
    return tileData
