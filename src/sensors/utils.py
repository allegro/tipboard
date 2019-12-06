import datetime, json, requests, time
from src.tipboard.app.properties import TIPBOARD_URL, DEBUG


def printEndOfTipboardCall(tipboardAnswer, TILE_ID):
    if tipboardAnswer is not None:
        print(f"POST tile:{TILE_ID} tipboard/push => ({tipboardAnswer.status_code}): ", flush=True)
        if tipboardAnswer.status_code == 200:
            print(f"\t\t{tipboardAnswer.text}")
    else:
        print(f"POST tile:{TILE_ID} tipboard/push => (FAILED HTTP CONNECT): ", flush=True)


def end(title=None, start_time=None, tipboardAnswer=None, TILE_ID=None):
    """ Eazy way to end sensors, print the action time & http answer of tipboard """
    printEndOfTipboardCall(tipboardAnswer, TILE_ID)
    duration = time.time() - start_time
    m = str(duration / 60)[:str(duration / 60).index(".")]
    s = str(duration % 60)[:str(duration % 60).index(".")]
    if m == '0':
        print(f"{getTimeStr()}-{title}: executed script in {s} seconds", flush=True)
    else:
        print(f"{getTimeStr()}-{title}: executed script in {m}:{s}", flush=True)
    print(f"----------------------------------------------------------------------------------------------", flush=True)


def getTimeStr():
    """ Eazy way to get in str, time for log """
    return datetime.datetime.now().strftime("%Hh%M")


def sendBVColor(color, tile, fading=False):  # pragma: no cover
    """ Modify meta of tile: update the color and/or fading of a specific tile """
    var = {"value": json.dumps({"big_value_color": color, "fading_background": fading})}
    res = requests.post(TIPBOARD_URL + "/tileconfig/" + tile, data=var)
    if DEBUG:
        print(f"{res}: color -> {tile}", flush=True)


def buildConfigTile(tile_id, tile_template, data):
    return {
        "tile": tile_template,  # tile_template name
        "key": tile_id,  # tile_template name
        "data": json.dumps(data)
    }


def sendDataToTipboard(data=None, tile_template=None, tile_id="", isTest=False):
    configTile = buildConfigTile(tile_id=tile_id, tile_template=tile_template, data=data)
    if not isTest:
        return requests.post(TIPBOARD_URL + "/push", data=configTile)
