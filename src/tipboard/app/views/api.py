import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse, Http404
from src.tipboard.app.applicationconfig import getRedisPrefix, getIsoTime
from src.tipboard.app.properties import PROJECT_NAME, LAYOUT_CONFIG, REDIS_DB, LOG
from src.tipboard.app.cache import getCache
from src.tipboard.app.utils import getTimeStr, checkAccessToken
from src.tipboard.app.FakeData.fake_data import buildFakeDataFromTemplate


def projectInfo(request):  # pragma: no cover
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
    else:
        return HttpResponseBadRequest(f'{tile_key} key does not exist.')


def delete_tile(request, tile_key, unsecured=False):  # pragma: no cover
    """ Delete in redis """
    if not checkAccessToken(method='DELETE', request=request, unsecured=unsecured):
        return HttpResponse('API KEY incorrect', status=401)
    redis = getCache().redis
    if redis.exists(tile_key):
        redis.delete(tile_key)
        return HttpResponse('Tile\'s data deleted.')
    else:
        return HttpResponseBadRequest(f'{tile_key} key does not exist.')


def tile(request, tile_key, unsecured=False):  # TODO: "it's better to ask forgiveness than permission" ;)
    """ Handles reading and deleting of tile's data """
    if request.method == 'GET':
        return get_tile(request, tile_key, unsecured)
    elif request.method == 'DELETE':
        return delete_tile(request, tile_key, unsecured)
    raise Http404


def update_tile_meta(request, tilePrefix, tile_key):  # pragma: no cover
    cachedTile = json.loads(getCache().redis.get(tilePrefix))
    options = json.loads(request.body.decode('utf-8'))
    try:
        for metaItem in options.keys():
            cachedTile['meta'][metaItem] = options[metaItem]
    except Exception as e:
        return HttpResponseBadRequest(f'Invalid Json data: {e}')
    getCache().set(tilePrefix, json.dumps(cachedTile))
    return HttpResponse(f'{tile_key} data updated successfully.')


def meta(request, tile_key, unsecured=False):  # pragma: no cover
    """ Update the meta(config) of a tile(widget) """
    if request.method == 'POST':
        if not checkAccessToken(method='POST', request=request, unsecured=unsecured):
            return HttpResponse('API KEY incorrect', status=401)
        tilePrefix = getRedisPrefix(tile_key)
        if not getCache().redis.exists(tilePrefix):
            return HttpResponseBadRequest(f'{tile_key} is not present in cache')
        return update_tile_meta(request, tilePrefix, tile_key)
    raise Http404


def isThereMetaUpdate(request, tile_id):  # pragma: no cover
    """ Check in the request if there is new meta value """
    try:
        request.POST.get('value', None)
        httpResponse = meta(request, tile_id)
        if httpResponse.status_code != 200:
            return httpResponse
    except Exception as e:
        if LOG:
            print(f'{getTimeStr()} (-) No meta value for update tile {tile_id}: {e}', flush=True)
        return HttpResponseBadRequest(f'{tile_id} meta was not update (meta is missing)')
    return HttpResponse(f'{tile_id} data updated successfully.')


def update(request, unsecured=False):  # TODO: "it's better to ask forgiveness than permission" ;)
    """ Update the meta(config) AND the content of a tile(widget) """
    if request.method == 'POST':
        if not checkAccessToken(method='POST', request=request, unsecured=unsecured):
            return HttpResponse('API KEY incorrect', status=401)
        tile_id = request.POST.get('key', None)
        data = request.POST.get('data', None)  # Test if var is present
        if data is None:
            print('No data')
        httpResponse = push(request)
        if httpResponse.status_code != 200:
            return httpResponse
        isThereMetaUpdate(request, tile_id)
    raise Http404


def update_tile_data(previousData, newData):
    """ update value of tile with new data """
    if isinstance(newData, str):
        previousData['text'] = newData
        return previousData
    for key, value in newData.items():
        if isinstance(value, dict) and key != 'data' and key in previousData and key != 'datasets':
            update_tile_data(previousData[key], value)
        else:
            previousData[key] = value
    return previousData


def push_tile(tile_id, tile_template, data, meta):  # pragma: no cover
    cache = getCache()
    tilePrefix = getRedisPrefix(tile_id)
    if not cache.redis.exists(tilePrefix):
        buildFakeDataFromTemplate(tile_id, tile_template, cache)
    cachedTile = json.loads(cache.redis.get(tilePrefix))
    cachedTile['data'] = update_tile_data(cachedTile['data'], json.loads(data))
    cachedTile['modified'] = getIsoTime()
    cachedTile['tile_template'] = tile_template
    if meta is not None:  # TODO: Test the update meta
        if meta.get('options') is not None:
            cachedTile['meta']['options'].update(meta['options'])
        elif meta.get('backgroundColor') is not None:
            cachedTile['meta']['backgroundColor'].update(meta['backgroundColor'])
    cache.set(tilePrefix, json.dumps(cachedTile))
    return HttpResponse(f"{tile_id} data updated successfully.")


def push(request, unsecured=False):  # pragma: no cover
    """ Update the content of a tile(widget) """
    if request.method == 'POST':
        if not checkAccessToken(method='POST', request=request, unsecured=unsecured):
            return HttpResponse('API KEY incorrect', status=401)
        if not request.POST.get('key', None) or \
                not request.POST.get('data', None) or \
                not request.POST.get('tile', None):
            return HttpResponseBadRequest(f'Missing data')
        data = request.POST.get('data', None)
        if 'data' in json.loads(data):
            data = json.dumps(json.loads(data)['data'])
        return push_tile(tile_id=request.POST.get('key', None),
                         tile_template=request.POST.get('tile', None),
                         data=data,
                         meta=request.POST.get('meta', None))
    raise Http404
