from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.staticfiles import finders
from django.shortcuts import render
from src.tipboard.app.parser import parseXmlLayout, getDashboardName, getConfigNames, getFlipboardTitles
from src.tipboard.app.properties import TIPBOARD_CSS_STYLES, FLIPBOARD_INTERVAL, LOG, TIPBOARD_JAVASCRIPTS
from src.tipboard.app.utils import getTimeStr
from src.sensors.sensors_main import scheduleYourSensors, stopTheSensors
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


def renderFlipboardHtml(request):
    """ Render the home page(Html flipboard), and start the javascript tipboard mecanism """
    return render(request, 'flipboard.html',
                  dict(page_title=getDashboardName(),
                       flipboard_interval=FLIPBOARD_INTERVAL,
                       tipboard_css=TIPBOARD_CSS_STYLES,
                       tipboard_js=['js/flipboard.js'] + TIPBOARD_JAVASCRIPTS))


def renderDashboardHtmlUniqueDashboard(request, layout_name='layout_config', isFlipboard=False):
    """
        Render Html page for all the tiles needed in layout_name(dashboard .yml)
        with CSS/JS dependency if isFlipboard is false
    """
    try:
        config = parseXmlLayout(layout_name)
        title = layout_name
        color_mode = "black"
        if 'details' in config:
            title = config['details']['page_title'] if 'page_title' in config['details'] else title
            color_mode = config['details']['color_mode'] if 'color_mode' in config['details'] else color_mode
        # TODO: handle when layout is not present inside the .yml (will throw error when config['layout'] not found)
        # layout_name will be used to make the diff between same tileId on multiple char
        data = dict(layout=config['layout'],
                    layout_name=layout_name,
                    tipboard_css=list() if isFlipboard else TIPBOARD_CSS_STYLES,
                    tipboard_js=list() if isFlipboard else TIPBOARD_JAVASCRIPTS,
                    color_mode=color_mode,
                    page_title=title)
        return render(request, 'dashboard.html' if isFlipboard else 'flipboard.html', data)
    except FileNotFoundError as e:
        if LOG:
            print(f'{getTimeStr()}: (+)Config file:{layout_name} not found', flush=True)
        msg = f'<br> <div style="color: red"> ' \
            f'No config file found for dashboard: {layout_name} ' \
            f'Make sure that file: "{e.filename}" exists. </div>'
        return HttpResponse(msg, status=404)


def renderDashboardHtmlForFlipboard(request, layout_name='layout_config'):
    """ Render Html page with CSS/JS dependency for all the tiles needed in layout_name(dashboard .yml) """
    return renderDashboardHtmlUniqueDashboard(request, layout_name, isFlipboard=True)


def getDashboardsPaths(request):
    """
        Return the path of layout prensent in the ./tipboard/app/Config
        Used in layout.js with flipboard.js function(getDashboardsByApi) to flip between all dashboard(*.yml) in /Config
    """
    paths = ['/' + config_name for config_name in getConfigNames()]
    names = getFlipboardTitles()
    return JsonResponse(dict(paths=paths, names=names), safe=False)


def demo_controller(request, flagSensors=None, tester=None):
    """ activate or not the sensors by api  """
    if flagSensors == 'on':
        scheduleYourSensors(scheduler, tester)
    elif flagSensors == 'off':
        stopTheSensors(scheduler)
    return HttpResponseRedirect('/')
