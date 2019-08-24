# -*- coding: utf-8 -*-

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from src.tipboard.app.cache import getCache
from src.tipboard.app.flipboard import Flipboard
from src.tipboard.app.parser import process_layout_config
from src.tipboard.app.properties import *
from src.tipboard.app.utils import getTimeStr

cache = getCache()


def flipboardHandler(request):
    if LOG:
        print(f"{getTimeStr()} (+) flipboardHandler/", flush=True)
    data = {
        "page_title": Flipboard().get_flipboard_title(),
        "tipboard_css": TIPBOARD_CSS_STYLES,
        "tipboard_js": ['js/lib/jquery.js', 'js/flipboard.js', 'js/lib/require.js'],
        "flipboard_interval": FLIPBOARD_INTERVAL,
    }
#    data['tipboard_js'].remove('js/tipboard.js')
    return render(request, 'flipboard.html', data)


def getDashboardsPaths(request):
    if LOG:
        print(f"{getTimeStr()} GET /getDashboardsPaths", flush=True)
    paths = Flipboard().get_paths()
    return JsonResponse({'paths': paths}, safe=False)


def dashboardRendererHandler(request, layout_name='layout_config'):
    if LOG:
        print(f"{getTimeStr()} GET dashboardRendererHandler /{layout_name}", flush=True)
    try:
        config = process_layout_config(layout_name)
        tiles_js = ["tiles/" + '.'.join((name, 'js')) for name in config['tiles_names']]
        tiles_css = ["tiles/" + '.'.join((name, 'css')) for name in config['tiles_names']]
        #tiles_js = filter(_verify_statics, tiles_js) #TODO fix the verify_statics for js/css in utils.py
        print(f"Yaml loaded tilesjs: {tiles_js}")
        data = {
            "details": config['details'],
            "layout": config['layout'],
            "tipboard_css": TIPBOARD_CSS_STYLES,
            "tipboard_js": TIPBOARD_JAVASCRIPTS,
            "tiles_css": tiles_css,
            "tiles_js": tiles_js,
        }
    except FileNotFoundError as e:
        if LOG:
            print(f"{getTimeStr()}: (+)Config file:{layout_name} not found", flush=True)
        msg = '<br>'.join([
            '<div style="color: red">',
            f'No config file found for dashboard: {layout_name}',
            f'Make sure that file: "{e.filename}" exists.',
            '</div>',
        ])
        return HttpResponse(msg, status=404)
    return render(request, 'layout.html', data)


