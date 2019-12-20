from django.http import HttpResponseBadRequest, Http404
from src.tipboard.app.ApiAntiRegression import updateDatav1tov2
from src.tipboard.app.properties import DEBUG
from src.tipboard.app.utils import getTimeStr
from src.tipboard.app.views.api import tile, push_tile, meta, update

# Unsecured part, don't look here ! :D
# This allow previous user to use their old script without migration in a insecure way :)


def tile_unsecured(request, tile_key):  # pragma: no cover
    print(f"{getTimeStr()} (~) Using unsecured tile url")
    if not DEBUG:
        raise Http404
    else:
        return tile(request=request, tile_key=tile_key, unsecured=True)


def push_unsecured(request):  # pragma: no cover
    print(f"{getTimeStr()} (~) Using unsecured push url")
    if not DEBUG:
        raise Http404
    postVariable = request.POST
    if not postVariable.get("key", None) or not postVariable.get("data", None) or not postVariable.get("tile", None):
        return HttpResponseBadRequest(f"Missing data")
    tileType = postVariable.get("tile", None)
    # TODO: check the token for 'security' xD
    try:
        data = updateDatav1tov2(tileType, postVariable.get("data", None))
        print(f"{getTimeStr()} (+) DATA MIGRATED ({tileType}): {data}")
        return push_tile(tile_id=postVariable.get("key", None), data=data, tile_template=tileType, meta=None)
    except Exception:
        return HttpResponseBadRequest('Error in request')


def meta_unsecured(request, tile_key):  # pragma: no cover
    print(f"{getTimeStr()} (~) Using unsecured meta url")
    if not DEBUG:
        raise Http404
    else:
        return meta(request=request, tile_key=tile_key, unsecured=True)


def update_unsecured(request):  # pragma: no cover
    print(f"{getTimeStr()} (~) Using unsecured update url")
    if not DEBUG:
        raise Http404
    else:
        return update(request=request, unsecured=True)
