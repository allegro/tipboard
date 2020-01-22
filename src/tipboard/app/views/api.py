import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse, Http404
from src.tipboard.app.applicationconfig import getRedisPrefix, getIsoTime
from src.tipboard.app.properties import PROJECT_NAME, LAYOUT_CONFIG, REDIS_DB, LOG, DEBUG, ALLOWED_TILES
from src.tipboard.app.cache import getCache
from src.tipboard.app.utils import getTimeStr, checkAccessToken
from src.tipboard.app.FakeData.fake_data import buildFakeDataFromTemplate
from src.tipboard.app.FakeData.datasetbuilder import buildGenericDataset


def project_info(request):  # pragma: no cover
    """ Return info of server tipboard """
    if request.method == 'GET':
        response = dict(tipboard_version='v0.1',
                        project_name=PROJECT_NAME,
                        project_layout_config=LAYOUT_CONFIG,
                        redis_db=REDIS_DB)
        return JsonResponse(response)
    raise Http404


def get_tile(request, tile_key, unsecured=False):  # pragma: no cover
    """ Return Json from redis for tile_key """
    if not checkAccessToken(method='GET', request=request, unsecured=unsecured):
        return HttpResponse('API KEY incorrect', status=401)
    redis = getCache().redis
    if redis.exists(tile_key):
        return HttpResponse(redis.get(tile_key))
    return HttpResponseBadRequest(f'{tile_key} key does not exist.')


def delete_tile(request, tile_key, unsecured=False):  # pragma: no cover
    """ Delete in redis """
    if not checkAccessToken(method='DELETE', request=request, unsecured=unsecured):
        return HttpResponse('API KEY incorrect', status=401)
    redis = getCache().redis
    if redis.exists(tile_key):
        redis.delete(tile_key)
        return HttpResponse('Tile\'s data deleted.')
    return HttpResponseBadRequest(f'{tile_key} key does not exist.')


def tile_rest(request, tile_key, unsecured=False):  # TODO: "it's better to ask forgiveness than permission" ;)
    """ Handles reading and deleting of tile's data """
    if request.method == 'GET':
        return get_tile(request, tile_key, unsecured)
    if request.method == 'DELETE':
        return delete_tile(request, tile_key, unsecured)
    raise Http404


def update_dataset_from_tiles(value, previousData, key, tile_template):
    rcx = 0
    for dataset in value:
        if rcx >= len(previousData[key]):
            previousData[key].append(buildGenericDataset(tile_template=tile_template))
        update_tile_data_from_redis(previousData[key][rcx], dataset, tile_template)
        rcx = rcx + 1
    previousData[key] = previousData[key][0:len(value)]


def update_tile_data_from_redis(previousData, newData, tile_template):
    """ update value(dict) of tile with new data Recursiv & deep inside the tile """
    if isinstance(newData, str):
        previousData['text'] = newData
        return previousData
    for key, value in newData.items():
        if isinstance(value, dict) and key != 'data' and key in previousData:
            update_tile_data_from_redis(previousData[key], value, tile_template)
        elif isinstance(value, list) and key == 'datasets':
            update_dataset_from_tiles(value, previousData, key, tile_template)
        else:
            previousData[key] = value
    return previousData


def save_tile_ToRedis(tile_id, tile_template, data):  # pragma: no cover
    cache = getCache()
    tilePrefix = getRedisPrefix(tile_id)
    if not cache.redis.exists(tilePrefix) and DEBUG:  # if tile don't exist, create it with template, DEBUG mode only
        buildFakeDataFromTemplate(tile_id, tile_template, cache)
    cachedTile = json.loads(cache.redis.get(tilePrefix))
    cachedTile['data'] = update_tile_data_from_redis(cachedTile['data'], json.loads(data), tile_template)
    cachedTile['modified'] = getIsoTime()
    cachedTile['tile_template'] = tile_template
    cache.set(tilePrefix, json.dumps(cachedTile))
    return HttpResponse(f'{tile_id} data updated successfully.')


def sanity_push_api(request, unsecured):
    """ Test token, all data present, correct tile_template and tile_id present in cache """
    if not checkAccessToken(method='POST', request=request, unsecured=unsecured):
        return False, HttpResponse('API KEY incorrect', status=401)
    HttpData = request.POST
    if not HttpData.get('tile_id', None) or not HttpData.get('tile_template', None) or \
            not HttpData.get('data', None):
        return False, HttpResponseBadRequest('Missing data')
    if HttpData.get('tile_template', None) not in ALLOWED_TILES:
        tile_template = HttpData.get('tile_template', None)
        return False, HttpResponseBadRequest(f'tile_template: {tile_template} is unknow')
    cache = getCache()
    tilePrefix = getRedisPrefix(HttpData.get('tile_id', None))
    if not cache.redis.exists(tilePrefix) and not DEBUG:
        return False, HttpResponseBadRequest(f'tile_id: {tilePrefix} is unknow')
    return True, HttpData


def push_api(request, unsecured=False):
    """ Update the content of a tile (widget) """
    if request.method == 'POST':
        state, HttpData = sanity_push_api(request, unsecured)
        if state is False:
            return HttpData
        data = HttpData.get('data', None)
        tile_id = HttpData.get('tile_id', None)
        error = is_meta_present_in_request(HttpData.get('meta', None), tile_id)
        if error:  # protect against update for tile_id not present in redis
            HttpResponseBadRequest(f'{tile_id} is not present in cache')
        return save_tile_ToRedis(tile_id=tile_id,
                                 tile_template=HttpData.get('tile_template', None),
                                 data=json.dumps(json.loads(data)['data']) if 'data' in json.loads(data) else data)
    raise Http404


def is_meta_present_in_request(meta, tile_id):  # pragma: no cover
    """ Update the meta(config) of a tile(widget) """
    if meta is not None:
        tilePrefix = getRedisPrefix(tile_id)
        if getCache().redis.exists(tilePrefix) is not None:
            cachedTile = json.loads(getCache().redis.get(tilePrefix))
            update_tile_data_from_redis(cachedTile['meta']['options'], json.loads(meta), None)
            getCache().set(tilePrefix, json.dumps(cachedTile))
            print(f"(+) Meta of tile {tilePrefix} has been updated")
            return True
    print(f"(+) Meta of tile not present")
    return False
