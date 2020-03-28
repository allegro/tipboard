import time
from src.sensors.utils import end, sendUpdateByApi


def returnHttPageExemple():
    """ Basic Html exemple with css """
    return '''
    <div class="contener" id="mycontener">
         <div class="card">
<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcS0MrhIzjan2GfDeqNVqyIDjBXqP7J7GwDJxd_OKwp91Lj4JS4t">
             <div class="container">
                  <h4><b>Mister cat</b></h4>
                  <p>Look in my eyes darling</p>
             </div>
        </div> 
    </div>
    <style>
    #mycontener {
        display: flex;
        justify-content: center;     
    }
    </style>
    '''


def sonde22(tester=None, tile_id='custom_ex'):
    start_time = time.time()
    data = {
        'text': returnHttPageExemple()
    }
    tipboardAnswer = sendUpdateByApi(data=data, tileTemplate='custom', tileId=tile_id, tester=tester)
    end(title=f'sensors custom tile -> {tile_id}', startTime=start_time, tipboardAnswer=tipboardAnswer, tileId=tile_id)
