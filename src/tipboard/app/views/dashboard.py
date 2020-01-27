from django.http import JsonResponse, HttpResponse, Http404, HttpResponseRedirect
from django.contrib.staticfiles import finders
from django.shortcuts import render
from src.tipboard.app.parser import parseXmlLayout, getFlipboardTitle, getConfigNames, getFlipboardTitles
from src.tipboard.app.properties import TIPBOARD_CSS_STYLES, FLIPBOARD_INTERVAL, LOG, TIPBOARD_JAVASCRIPTS
from src.tipboard.app.utils import getTimeStr
from src.sensors.sensors_main import scheduleYourSensors, stopTheSensors
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


def renderFlipboardHtml(request):  # pragma: no cover
    """ Render the Html Flipboard, wich start the js tipboard mecanism """
    return render(request, 'flipboard.html',
                  dict(page_title=getFlipboardTitle(),
                       flipboard_interval=FLIPBOARD_INTERVAL,
                       tipboard_css=TIPBOARD_CSS_STYLES,
                       tipboard_js=['js/flipboard.js']))


def getDashboardsPaths(request):  # pragma: no cover
    """ Return the path of layout prensent in the ./tipboard/app/Config """
    paths = ['/' + config_name for config_name in getConfigNames()]
    names = getFlipboardTitles()
    return JsonResponse(dict(paths=paths, names=names), safe=False)


def replaceNameTiles(tiles_name):
    """ Replace name_tile when it's the same JS tile :), duplicate code is bad """
    listOfTiles = list()
    transformTileNameTab = {
        'big_value': 'text_value',
        'simple_percentage': 'text_value',
        'just_value': 'text_value',
        'listing': 'text_value'
    }
    for name_tile in tiles_name:
        if not listOfTiles.__contains__(name_tile):
            if name_tile in transformTileNameTab:
                name_tile = transformTileNameTab[name_tile]
            else:
                name_tile = "chartjs"
            if name_tile not in listOfTiles:
                listOfTiles.append(name_tile)
    return listOfTiles


def getTilesDependency(layout_name):
    """ Build CSS / JS tiles dependency from the tile referenced in layout.yaml """
    config = parseXmlLayout(layout_name)
    tiles_template = replaceNameTiles(config['tiles_names'])
    data = dict(details=config['details'],
                layout=config['layout'],
                tipboard_css=TIPBOARD_CSS_STYLES,
                tipboard_js=TIPBOARD_JAVASCRIPTS,
                tiles_css=['tiles/' + '.'.join((name, 'css')) for name in tiles_template],
                tiles_js=['tiles/' + '.'.join((name, 'js')) for name in tiles_template])
    tiles_css = list()  # TODO i think this need to be deleted, no css anymore for specific tile
    for tile_css in data['tiles_css']:
        if finders.find(tile_css):
            tiles_css.append(tile_css)
    data['tiles_css'] = tiles_css
    return data


def renderHtmlForTiles(request, layout_name='layout_config'):  # pragma: no cover
    """ Render Htlm page with CSS/JS dependency for all the tiles needed in layout.yaml(dashboard) """
    try:
        data = getTilesDependency(layout_name)
        return render(request, 'layout.html', data)
    except FileNotFoundError as e:
        if LOG:
            print(f'{getTimeStr()}: (+)Config file:{layout_name} not found', flush=True)
        msg = f"<br> <div style='color: red'> " \
            f'No config file found for dashboard: {layout_name} ' \
            f"Make sure that file: '{e.filename}' exists. </div>"
        return HttpResponse(msg, status=404)


def demo_controller(request, flagSensors):
    """ activate or not the sensors by api  """
    if request.method == 'GET':
        if flagSensors == "on":
            scheduleYourSensors(scheduler)
        elif flagSensors == "off":
            stopTheSensors(scheduler)
        return HttpResponseRedirect('/')
    raise Http404
