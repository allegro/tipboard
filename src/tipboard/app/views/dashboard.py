# -*- coding: utf-8 -*-
from django.http import JsonResponse, HttpResponse
from django.contrib.staticfiles import finders
from django.shortcuts import render

from src.tipboard.app.cache import getCache
from src.tipboard.app.flipboard import Flipboard
from src.tipboard.app.parser import parse_xml_layout
from src.tipboard.app.properties import TIPBOARD_CSS_STYLES, FLIPBOARD_INTERVAL, LOG, TIPBOARD_JAVASCRIPTS
from src.tipboard.app.utils import getTimeStr

cache = getCache()


def flipboardHandler(request):
    data = {
        "page_title": Flipboard().get_flipboard_title(),
        "tipboard_css": TIPBOARD_CSS_STYLES,
        "tipboard_js": ['js/flipboard.js'],
        "flipboard_interval": FLIPBOARD_INTERVAL,
    }
    print(f"{getTimeStr()} (+) flipboardHandler/ -> CSS: {data['tipboard_css']}", flush=True)
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
        config = parse_xml_layout(layout_name)

        data = {
            "details": config['details'],
            "layout": config['layout'],
            "tipboard_css": TIPBOARD_CSS_STYLES,
            "tipboard_js": TIPBOARD_JAVASCRIPTS,
            "tiles_css": ["tiles/" + '.'.join((name, 'css')) for name in config['tiles_names']],
            "tiles_js": ["tiles/" + '.'.join((name, 'js')) for name in config['tiles_names']],
        }
    except FileNotFoundError as e:
        if LOG:
            print(f"{getTimeStr()}: (+)Config file:{layout_name} not found", flush=True)
        msg = f'<br> <div style="color: red"> ' \
            f'No config file found for dashboard: {layout_name} ' \
            f'Make sure that file: "{e.filename}" exists. </div>'
        return HttpResponse(msg, status=404)
    tiles_css = list()
    for tile_css in data['tiles_css']:
        if finders.find(tile_css):
            tiles_css.append(tile_css)
    data['tiles_css'] = tiles_css
    return render(request, 'layout.html', data)
