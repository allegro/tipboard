import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse, Http404
from src.tipboard.app.applicationconfig import getRedisPrefix, getIsoTime
from src.tipboard.app.properties import PROJECT_NAME, LAYOUT_CONFIG, REDIS_DB, LOG, DEBUG
from src.tipboard.app.cache import getCache
from src.tipboard.app.utils import getTimeStr, checkAccessToken
from src.tipboard.app.FakeData.fake_data import buildFakeDataFromTemplate


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


def update_tile_meta(request, tilePrefix, tile_key):  # pragma: no cover
    cachedTile = json.loads(getCache().redis.get(tilePrefix))
    options = json.loads(request.POST.get('value', None))
    try:
        for metaItem in options.keys():
            cachedTile['meta'][metaItem] = options[metaItem]
    except Exception as e:
        return HttpResponseBadRequest(f'Invalid Json data: {e}')
    getCache().set(tilePrefix, json.dumps(cachedTile))
    return HttpResponse(f'{tile_key} data updated successfully.')


def meta_api(request, tile_key, unsecured=False):  # pragma: no cover
    """ Update the meta(config) of a tile(widget) """
    if request.method == 'POST':
        if not checkAccessToken(method='POST', request=request, unsecured=unsecured):
            return HttpResponse('API KEY incorrect', status=401)
        tilePrefix = getRedisPrefix(tile_key)
        if not getCache().redis.exists(tilePrefix):
            return HttpResponseBadRequest(f'{tile_key} is not present in cache')
        return update_tile_meta(request, tilePrefix, tile_key)
    raise Http404


def update_tile_data_from_redis(previousData, newData):
    """ update value of tile with new data """
    if isinstance(newData, str):
        previousData['text'] = newData
        return previousData
    for key, value in newData.items():
        if isinstance(value, dict) and key != 'data' and key in previousData and key != 'datasets':
            update_tile_data_from_redis(previousData[key], value)
        else:
            previousData[key] = value
    return previousData


def save_tile_ToRedis(tile_id, tile_template, data, meta):  # pragma: no cover
    cache = getCache()
    tilePrefix = getRedisPrefix(tile_id)
    if not cache.redis.exists(tilePrefix) and DEBUG:  # if tile don't exist, create it with template, DEBUG mode only
        buildFakeDataFromTemplate(tile_id, tile_template, cache)
    cachedTile = json.loads(cache.redis.get(tilePrefix))
    cachedTile['data'] = update_tile_data_from_redis(cachedTile['data'], json.loads(data))
    cachedTile['modified'] = getIsoTime()
    cachedTile['tile_template'] = tile_template
    cache.set(tilePrefix, json.dumps(cachedTile))
    return HttpResponse(f'{tile_id} data updated successfully.')


def push_api(request, unsecured=False):  # pragma: no cover
    """ Update the content of a tile (widget) """
    if request.method == 'POST':
        if not checkAccessToken(method='POST', request=request, unsecured=unsecured):
            return HttpResponse('API KEY incorrect', status=401)
        HttpData = request.POST
        if not HttpData.get('tile_id', None) or not HttpData.get('tile_template', None) or \
                not HttpData.get('data', None):
            return HttpResponseBadRequest('Missing data')
        data = HttpData.get('data', None)
        if 'data' in json.loads(data):
            data = json.dumps(json.loads(data)['data'])
        return save_tile_ToRedis(tile_id=HttpData.get('tile_id', None),
                                 tile_template=HttpData.get('tile_template', None),
                                 data=data,
                                 meta=HttpData.get('meta', None))
    raise Http404


def is_meta_present_in_request(request, tile_id):  # pragma: no cover
    """ Check in the request if there is new meta value for /update """
    try:
        request.POST.get('value', None)
        httpResponse = meta_api(request, tile_id)
        if httpResponse.status_code != 200:
            return httpResponse
    except Exception as e:
        if LOG:
            print(f'{getTimeStr()} (-) No meta value for update tile {tile_id}: {e}', flush=True)
        return HttpResponseBadRequest(f'{tile_id} meta was not update (meta is missing)')
    return HttpResponse(f'{tile_id} data updated successfully.')


def update_api(request, unsecured=False):  # TODO: "it's better to ask forgiveness than permission" ;)
    """ Update the meta(config) AND the content of a tile(widget) """
    if request.method == 'POST':
        if not checkAccessToken(method='POST', request=request, unsecured=unsecured):
            return HttpResponse('API KEY incorrect', status=401)
        tile_id = request.POST.get('tile_id', None)
        data = request.POST.get('data', None)  # Test if var is present
        if data is None:
            print('No data')
        httpResponse = push_api(request)
        return httpResponse if httpResponse.status_code != 200 else is_meta_present_in_request(request, tile_id)
    raise Http404

# if meta is not None:  # TODO: Test the update meta
#     if meta.get('options') is not None:
#         cachedTile['meta']['options'].update_api(meta['options'])
#     elif meta.get('backgroundColor') is not None:
#         cachedTile['meta']['backgroundColor'].update_api(meta['backgroundColor'])
