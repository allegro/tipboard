from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from src.tipboard.app.applicationconfig import getRedisPrefix
from src.tipboard.app.properties import BASIC_CONFIG, REDIS_DB, DEBUG, ALLOWED_TILES
from src.tipboard.app.cache import MyCache, save_tile
from src.tipboard.app.utils import checkAccessToken
from src.tipboard.app.parser import getConfigNames


def project_info(request):
    """ Return info of server tipboard """
    cache = MyCache()
    return JsonResponse(dict(is_redis_connected=cache.isRedisConnected,
                             last_update=cache.getLastUpdateTime(),
                             first_start=cache.getFirstTimeStarter(),
                             project_default_config=BASIC_CONFIG,
                             dashboard_list=getConfigNames(),
                             redis_db=REDIS_DB))


def get_tile(request, tile_key):
    """ Return Json from redis for tile_key """
    if not checkAccessToken(method='GET', request=request, unsecured=True):
        return HttpResponse('API KEY incorrect', status=401)
    redis = MyCache().redis
    if redis.exists(getRedisPrefix(tile_key)):
        return HttpResponse(redis.get(tile_key))
    return HttpResponseBadRequest(f'{tile_key} key does not exist.')


def delete_tile(request, tile_key):
    """ Delete in redis """
    if not checkAccessToken(method='DELETE', request=request, unsecured=True):
        return HttpResponse('API KEY incorrect', status=401)
    redis = MyCache().redis
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
    cache = MyCache()
    tilePrefix = getRedisPrefix(HttpData.get('tile_id', None))
    if not cache.redis.exists(tilePrefix) and not DEBUG:
        return False, HttpResponseBadRequest(f'tile_id: {tilePrefix} is unknow')
    return True, HttpData


def push_api(request, unsecured=False):
    """ Update the content of a tile (widget) """
    if request.method == 'POST':
        state, HttpData = sanity_push_api(request, unsecured)
        if state:
            tile_id = HttpData.get('tile_id', None)
            tile_template = HttpData.get('tile_template', None)
            tile_data = HttpData.get('data', None)
            tile_meta = HttpData.get('meta', None)
            if save_tile(tile_id=tile_id, template=tile_template, data=tile_data, meta=tile_meta):
                return HttpResponse(f'{tile_id} data updated successfully.')
            HttpData = HttpResponse(f'Error while saving tile with tile_id: {tile_id}')
        return HttpData
