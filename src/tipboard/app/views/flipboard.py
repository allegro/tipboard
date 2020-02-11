from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.staticfiles import finders
from django.shortcuts import render
from src.tipboard.app.parser import parseXmlLayout, getFlipboardTitle, getConfigNames, getFlipboardTitles
from src.tipboard.app.properties import TIPBOARD_CSS_STYLES, FLIPBOARD_INTERVAL, LOG, TIPBOARD_JAVASCRIPTS
from src.tipboard.app.utils import getTimeStr
from src.sensors.sensors_main import scheduleYourSensors, stopTheSensors
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


def renderFlipboardHtml(request):
    """ Render the home page(Html flipboard), and start the javascript tipboard mecanism """
    return render(request, 'flipboard.html',
                  dict(page_title=getFlipboardTitle(),
                       flipboard_interval=FLIPBOARD_INTERVAL,
                       tipboard_css=TIPBOARD_CSS_STYLES,
                       tipboard_js=['js/flipboard.js'] + TIPBOARD_JAVASCRIPTS))


def renderDashboardHtmlUniqueDashboard(request, layout_name='layout_config', isFlipboard=False):
    """ Render Html page with CSS/JS dependency for all the tiles needed in layout_name(dashboard .yml) """
    try:
        config = parseXmlLayout(layout_name)
        data = dict(details=config['details'],
                    layout=config['layout'],
                    tipboard_css=list() if isFlipboard else TIPBOARD_CSS_STYLES,
                    tipboard_js=list() if isFlipboard else TIPBOARD_JAVASCRIPTS,
                    tiles_css=list(),
                    tiles_js=list(),
                    layout_name=layout_name)
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
