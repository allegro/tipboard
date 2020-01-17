import time, random
from src.sensors.utils import end, sendDataToTipboard, getTimeStr


def getItemExemple(index):
    if index % 2 == 0:
        return {
            'items':
                [f'Leader: {random.randrange(1, 5)}',
                 f'Product Owner: {random.randrange(1, 2)}',
                 f'Scrum Master: {random.randrange(1, 2)}',
                 f'Developer: {random.randrange(1, 5)}'
                 ]
        }
    return {
        'items':
            [f'Major incident: {random.randrange(1, 5)}',
             f'N2 incident: {random.randrange(2, 50)}',
             f'+3month incident: {random.randrange(10, 59)}',
             f'Resolved incident: {random.randrange(1, 50)}'
             ]
    }


def executeScriptToGetData():
    """ Simulate some actions for text tile exemple"""
    return getItemExemple(random.randrange(0, 3))


def sonde6(isTest=False):
    TILE_ID = 'listing_ex'
    print(f'{getTimeStr()} (+) Starting sensors 6', flush=True)
    start_time = time.time()
    data = executeScriptToGetData()
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='listing', tile_id=TILE_ID, isTest=isTest)
    end(title=f'sensors6 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
