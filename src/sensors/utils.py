import datetime, json, requests, time, random
from src.tipboard.app.properties import TIPBOARD_URL, COLOR_TAB, LOG


def printEndOfTipboardCall(tipboardAnswer, tileId):
    if tipboardAnswer is None:
        print(f'POST tile:{tileId} tipboard/push => (FAILED HTTP CONNECT): ', flush=True)


def end(title=None, startTime=None, tipboardAnswer=None, tileId=None):
    """ Eazy way to end sensors, print the action time & http answer of tipboard """
    if LOG:
        printEndOfTipboardCall(tipboardAnswer, tileId)
        duration = time.time() - startTime
        m = str(duration / 60)[:str(duration / 60).index('.')]
        s = str(duration % 60)[:str(duration % 60).index('.')]
        if m == '0':
            print(f'{getTimeStr()}-{title}: executed script in {s} seconds', flush=True)
        else:
            print(f'{getTimeStr()}-{title}: executed script in {m}:{s}', flush=True)
        print(f'-----------------------------------------------------------------------------------------', flush=True)


def getTimeStr():
    """ Eazy way to get in str, time for log """
    return datetime.datetime.now().strftime('%Hh%M')


def sendUpdateByApi(tileId=None, data=None, tileTemplate=None, tester=False, meta=None):
    """ Send data to url django /push, if it's a test, send the django.UnitTest fake client """
    configTile = dict(tile_id=tileId, tile_template=tileTemplate, data=json.dumps(data))
    if meta is not None:
        configTile['meta'] = json.dumps(meta)
    if tester is None:
        return requests.post(TIPBOARD_URL + '/push', data=configTile)
    return tester.fakeClient.post(TIPBOARD_URL + '/push', data=configTile)


def updateChartJS(nbrDataset=None, nbrLabel=None, colorTabIndataset=False, data=None):
    """
        Build a full dataset, title, legend for title with random data
        For the demo, it show the possibility to hide title/legend/label, randomly
    """
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
                 borderColor=COLOR_TAB[index] if colorTabIndataset is False else '#626262'))
    return tileData
