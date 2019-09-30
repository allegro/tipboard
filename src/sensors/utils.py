# -*- coding: utf-8 -*-
import datetime, json, requests, time
from src.tipboard.app.properties import TIPBOARD_URL, DEBUG


def end(title, start_time):
    """ Eazy way to get in str, the time of an action :) """
    duration = time.time() - start_time
    m = str(duration / 60)[:str(duration / 60).index(".")]
    s = str(duration % 60)[:str(duration % 60).index(".")]
    if m == 0:  # pragma: no cover
        print(f"{getTimeStr()}-{title}: executed script in {s} seconds", flush=True)
    else:
        print(f"{getTimeStr()}-{title}: executed script in {m}:{s}", flush=True)


def getTimeStr():
    """ Eazy way to get in str, time for log """
    return datetime.datetime.now().strftime("%Hh%M")


def sendBVColor(color, tile, fading=False):  # pragma: no cover
    """ Modify meta of tile: update the color and/or fading of a specific tile """
    var = {"value": json.dumps({"big_value_color": color, "fading_background": fading})}
    res = requests.post(TIPBOARD_URL + "/tileconfig/" + tile, data=var, verify=False)
    if DEBUG:
        print(f"{res}: color -> {tile}", flush=True)