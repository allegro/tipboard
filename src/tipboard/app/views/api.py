# -*- coding: utf-8 -*-
import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse, HttpResponseServerError, Http404
from src.tipboard.app.properties import PROJECT_NAME, LAYOUT_CONFIG, REDIS_DB, LOG
from src.tipboard.app.cache import getCache
from src.tipboard.app.utils import getRedisPrefix, getTimeStr, getIsoTime

cache = getCache()
redis = cache.redis


# TODO: "it's better to ask forgiveness than permission" ;)
def getTile(request, tile_key):
    """Handles reading and deleting of tile's data."""
    if redis.exists(tile_key):
        return HttpResponse(redis.get(tile_key))
    else:
        return HttpResponseBadRequest(f"{tile_key} key does not exist.")


def deleteTile(request, tile_key):
    if redis.exists(tile_key):
        redis.delete(tile_key)
        return HttpResponse("Tile's data deleted.")
    else:
        return HttpResponseBadRequest(f"{tile_key} key does not exist.")


def tile(request, tile_key):
    if request.method == "GET":
        return getTile(request, getRedisPrefix(tile_key))
    elif request.method == "DELETE":
        return deleteTile(request, getRedisPrefix(tile_key))
    raise Http404


def createTile(tile_id, value, tile_template):
    dumped_value = json.dumps(dict(
        id=tile_id,
        tile_template=tile_template,
        data=json.loads(value),
        meta={},
        modified=getIsoTime(),
    ))
    cache.set(getRedisPrefix(tile_id), dumped_value)
    return HttpResponse(f"{tile_id} data created successfully.")


def push(request):
    if request.method == "POST":
        try:
            tile_id = request.POST.get("key", None)
            data = request.POST.get("data", None)
            tile_template = request.POST.get("tile", None)
            if not tile_id or not data or not tile_template:
                return HttpResponseBadRequest(f"Missing data")
            tilePrefix = getRedisPrefix(tile_id)
            if not redis.exists(tilePrefix):
                if LOG:
                    print(f"{getTimeStr()}: (+) {tile_id} not found in cache, creating tile {tile_template}", flush=True)
                return createTile(tile_id=tile_id, value=data, tile_template=tile_template)
            cachedTile = json.loads(redis.get(tilePrefix))
            cachedTile['data'] = json.loads(data)
            cachedTile['modified'] = getIsoTime()
            cachedTile['tile_template'] = tile_template
            cache.set(tilePrefix, json.dumps(cachedTile))
            return HttpResponse(f"{tile_id} data updated successfully.")
        except IOError as e:
            return HttpResponseServerError(e)
    raise Http404


def meta(request, tile_key):
    if request.method == "POST":
        try:
            value = request.POST.get("value", None)
            if value is None:
                return HttpResponseBadRequest("Missing data")
            try:
                value = json.loads(value)
            except:
                return HttpResponseBadRequest("Invalid Json data")
            if "big_value_color" not in value or "fading_background" not in value:
                return HttpResponseBadRequest("Bad data")
            tilePrefix = getRedisPrefix(tile_key)
            if not redis.exists(tilePrefix):
                if LOG:
                    print(f"{getTimeStr()}: (+) {tile_key} is not present in cache", flush=True)
                return HttpResponseBadRequest(f"{tile_key} is not present in cache")
            cachedTile = json.loads(redis.get(tilePrefix))
            cachedTile['meta']['big_value_color'] = value['big_value_color']
            cachedTile['meta']['fading_background'] = value['fading_background']
            cache.set(tilePrefix, json.dumps(cachedTile))
            return HttpResponse(f"{tile_key} data updated successfully.")
        except Exception as e:
            return HttpResponseServerError(e)
    raise Http404


# TODO: "it's better to ask forgiveness than permission" ;)
def update(request):
    if request.method == "POST":
        try:
            tile_id = request.POST.get("key", None)
            data = request.POST.get("data", None)
            httpResponse = push(request)
            if httpResponse.status_code != 200:
                return httpResponse
            try:
                request.POST.get("value", None)
                httpResponse = meta(request, tile_id)
                if httpResponse.status_code != 200:
                    return httpResponse
            except Exception as e:
                if LOG:
                    print(f"{getTimeStr()} (-) No meta value for update tile {tile_id}: {e}", flush=True)
                return HttpResponseBadRequest(f"{tile_id} data updated successfully.")
            return HttpResponse(f"{tile_id} data updated successfully.")
        except Exception as e:
            if LOG:
                print(f"{getTimeStr()} (-) Update error: {e}", flush=True)
            return push(request)

def projectInfo(request):
    if request.method == "GET":
        response = {
            'tipboard_version': "v0.1",
            'project_name': PROJECT_NAME,
            'project_layout_config': LAYOUT_CONFIG,
            'redis_db': REDIS_DB,
        }
        return JsonResponse(response)
    raise Http404
