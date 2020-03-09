import time, random
from src.sensors.utils import end, sendUpdateByApi


def executeScriptToGetData(tile_id='stream_ex'):
    """ Simulate some actions for text tile exemple """
    webcamArray = [
        # # # America
        # "https://videos-3.earthcam.com/fecnetwork/16730.flv/chunklist_w1958387849.m3u8"
        # # Espagna
        # "https://video-auth1.iol.pt/beachcam/palavasrivegauche/chunks.m3u8",
        # "https://video-auth1.iol.pt/beachcam/carcavelos/chunks.m3u8",
        # "https://video-auth1.iol.pt/beachcam/bcmafraribeira/chunks.m3u8",
        # "https://video-auth1.iol.pt/beachcam/praiaguinchosul/chunks.m3u8",
        # "https://video-auth1.iol.pt/beachcam/costacaparicacds/chunks.m3u8",
        # "https://video-auth1.iol.pt/beachcam/lagide/chunks.m3u8",
        # # France
        "https://video-auth1.iol.pt/beachcam/pourville/chunks.m3u8",
        "https://video-auth1.iol.pt/beachcam/lehavre/chunks.m3u8",
        "https://video-auth1.iol.pt/beachcam/siouvilles/chunks.m3u8",
        "https://video-auth1.iol.pt/beachcam/saintbrevin/chunks.m3u8",
        "https://video-auth1.iol.pt/beachcam/sablesolonne/chunks.m3u8",
        "https://video-auth1.iol.pt/beachcam/cotesauvage/chunks.m3u8",
        "https://video-auth1.iol.pt/beachcam/ronce/chunks.m3u8",
        "https://video-auth1.iol.pt/beachcam/montalivet/chunks.m3u8",
        "https://video-auth1.iol.pt/beachcam/latestedubuch/chunks.m3u8",
        "https://video-auth1.iol.pt/beachcam/biscarosse/chunks.m3u8",
        "https://video-auth1.iol.pt/beachcam/vieuxboucau01/chunks.m3u8",
        "https://video-auth1.iol.pt/beachcam/seignosse/chunks.m3u8",
        "https://video-auth1.iol.pt/beachcam/seignossebourdaines/chunks.m3u8",
        "https://video-auth1.iol.pt/beachcam/capbreton/chunks.m3u8",
        "https://video-auth1.iol.pt/beachcam/capbreton2/chunks.m3u8",
        "https://video-auth1.iol.pt/beachcam/bidart/chunks.m3u8",
        "https://video-auth1.iol.pt/beachcam/cavaliers/chunks.m3u8",
    ]
    c1 = random.choice(webcamArray)
    c2 = random.choice(webcamArray)
    return {
        'url': random.choice([c1, c2])
    }


def sonde21(tester=None, tile_id='stream_ex'):
    start_time = time.time()
    data = executeScriptToGetData()
    print(f"updated:{data}")

    answer = sendUpdateByApi(tileId=tile_id, data=data, tileTemplate='stream', tester=tester)
    end(title=f'sensor21 -> -> {tile_id}', startTime=start_time, tipboardAnswer=answer, tileId=tile_id)
