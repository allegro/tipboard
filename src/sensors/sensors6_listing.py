import time, random
from src.sensors.utils import end, sendUpdateByApi


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


def sonde6(tester=False, tile_id='listing_ex'):
    start_time = time.time()
    data = executeScriptToGetData()
    tipboardAnswer = sendUpdateByApi(data=data, tileTemplate='listing', tileId=tile_id, tester=tester)
    end(title=f'sensors6 -> {tile_id}', startTime=start_time, tipboardAnswer=tipboardAnswer, tileId=tile_id)
