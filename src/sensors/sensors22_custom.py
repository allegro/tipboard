import time
from src.sensors.utils import end, sendUpdateByApi


def returnHttPage():
    return '''
    <link property rel="stylesheet" href="http://snippi.com/raw/j5v0t66" media="screen" type="text/html"/>
    <div class="grid">
        <img src="https://dummyimage.com/824x600/1FD0C0/fff&text=%20" class="l" id="coco" alt="app">
        <img src="https://dummyimage.com/400x600/FF5046/fff&text=%20" class="m" id="cocote" alt="affiche">
        <img src="https://dummyimage.com/400x288/FFDE13/fff&text=%20" class="s" alt="site">
        <img src="https://dummyimage.com/824x600/1FD0C0/fff&text=%20" class="l" alt="app">
        <img src="https://dummyimage.com/400x600/FF5046/fff&text=%20" class="m" alt="affiche">
        <img src="https://dummyimage.com/400x288/FFDE13/fff&text=%20" class="s" alt="site">
        <img src="https://dummyimage.com/824x600/1FD0C0/fff&text=%20" class="l" alt="app">
        <img src="https://dummyimage.com/400x600/FF5046/fff&text=%20" class="m" alt="affiche">
        <img src="https://dummyimage.com/400x288/FFDE13/fff&text=%20" class="s" alt="site">
    </div>
    '''


def sonde22(tester=None, tile_id='custom_ex'):
    start_time = time.time()
    data = {
        'text': returnHttPage()
    }
    tipboardAnswer = sendUpdateByApi(data=data, tileTemplate='custom', tileId=tile_id, tester=tester)
    end(title=f'sensors custom tile -> {tile_id}', startTime=start_time, tipboardAnswer=tipboardAnswer, tileId=tile_id)
