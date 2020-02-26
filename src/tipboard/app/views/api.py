import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from src.tipboard.app.applicationconfig import getRedisPrefix
from src.tipboard.app.properties import PROJECT_NAME, LAYOUT_CONFIG, REDIS_DB, DEBUG, ALLOWED_TILES
from src.tipboard.app.cache import getCache, save_tile_ToRedis, update_tile_data_from_redis
from src.tipboard.app.utils import checkAccessToken


def project_info(request):
    """ Return info of server tipboard """
    if request.method == 'GET':
        response = dict(tipboard_version='v0.1',
                        project_name=PROJECT_NAME,
                        project_layout_config=LAYOUT_CONFIG,
                        redis_db=REDIS_DB)
        return JsonResponse(response)


def get_tile(request, tile_key):
    """ Return Json from redis for tile_key """
    if not checkAccessToken(method='GET', request=request, unsecured=True):
        return HttpResponse('API KEY incorrect', status=401)
    redis = getCache().redis
    if redis.exists(getRedisPrefix(tile_key)):
        return HttpResponse(redis.get(tile_key))
    return HttpResponseBadRequest(f'{tile_key} key does not exist.')


def delete_tile(request, tile_key):
    """ Delete in redis """
    if not checkAccessToken(method='DELETE', request=request, unsecured=True):
        return HttpResponse('API KEY incorrect', status=401)
    redis = getCache().redis
    if redis.exists(getRedisPrefix(tile_key)):
        redis.delete(tile_key)
        return HttpResponse('Tile\'s data deleted.')
    return HttpResponseBadRequest(f'{tile_key} key does not exist.')


def tile_rest(request, tile_key):
    """ Handles reading and deleting of tile's data """
    if request.method == 'DELETE':
        return delete_tile(request, tile_key)
    if request.method == 'GET':
        return get_tile(request, tile_key)


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
        tile_data = HttpData.get('data', None)
        tile_id = HttpData.get('tile_id', None)
        tile_template = HttpData.get('tile_template', None)
        res = save_tile_ToRedis(tile_id=tile_id, tile_template=tile_template, tile_data=tile_data)
        is_meta_present_in_request(HttpData.get('meta', None), tile_id)
        if res:  # TODO: handle when there is error in save_tile_redis
            return HttpResponse(f'{tile_id} data updated successfully.')


def is_meta_present_in_request(meta, tile_id):
    """ Update the meta(config) of a tile(widget) """
    if meta is not None:
        tilePrefix = getRedisPrefix(tile_id)
        cachedTile = json.loads(getCache().redis.get(tilePrefix))
        metaTile = cachedTile['meta']['options'] if 'options' in cachedTile['meta'] else cachedTile['meta']
        update_tile_data_from_redis(metaTile, json.loads(meta), None)
        getCache().set(tilePrefix, json.dumps(cachedTile), sendToWS=False)
