from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from src.tipboard.app.parser import parseXmlLayout, getConfigNames, getFlipboardTitles
from src.tipboard.app.properties import TIPBOARD_CSS_STYLES, FLIPBOARD_INTERVAL, LOG, TIPBOARD_JAVASCRIPT_FILES
from src.tipboard.app.utils import getTimeStr
from src.sensors.sensors_main import scheduleYourSensors, stopTheSensors
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


def renderFlipboardHtml(request):
    """ Render the home page(Html flipboard), and start the javascript tipboard mecanism """
    return render(request, 'flipboard.html',
                  dict(page_title='Tipboard',
                       flipboard_interval=FLIPBOARD_INTERVAL,
                       tipboard_css=TIPBOARD_CSS_STYLES,
                       tipboard_js=TIPBOARD_JAVASCRIPT_FILES))


def renderDashboardHtmlUniqueDashboard(request, layout_name='default_config', isFlipboard=False):
    """
        Render Html page for all the tiles needed in layout_name(dashboard .yml)
        with CSS/JS dependency if isFlipboard is false
    """
    config = parseXmlLayout(layout_name)
    if config is not None:  # file is present
        title = layout_name
        color_mode = "black"
        if 'details' in config:
            title = config['details']['page_title'] if 'page_title' in config['details'] else title
            color_mode = config['details']['color_mode'] if 'color_mode' in config['details'] else color_mode
        # TODO: handle when layout is not present inside the .yml (will throw error when config['layout'] not found)
        data = dict(layout=config['layout'],
                    layout_name=layout_name,
                    tipboard_css=list() if isFlipboard else TIPBOARD_CSS_STYLES,
                    tipboard_js=list() if isFlipboard else TIPBOARD_JAVASCRIPT_FILES,
                    color_mode=color_mode,
                    page_title=title)
        return render(request, 'dashboard.html' if isFlipboard else 'flipboard.html', data)
    if LOG:
        print(f'{getTimeStr()}: (+)Config file:{layout_name} not found', flush=True)
    msg = f'<br> <div style="color: red"> ' \
        f'No config file found for dashboard: {layout_name} ' \
        f'Make sure that file: "{layout_name}" exists. </div>'
    return HttpResponse(msg, status=404)


def renderDashboardHtmlForFlipboard(request, layout_name='default_config'):
    """ Render Html page with CSS/JS dependency for all the tiles needed in layout_name(dashboard .yml) """
    return renderDashboardHtmlUniqueDashboard(request, layout_name, isFlipboard=True)


def getDashboardsPaths(request):
    """
        Return the path of layout prensent in the ./tipboard/app/Config
        Used in layout.js function(getDashboardsByApi) to flip between all dashboard(*.yml) in /Config
    """
    paths = ['/' + config_name for config_name in getConfigNames()]
    names = getFlipboardTitles()
    return JsonResponse(dict(paths=paths, names=names), safe=False)


def demo_controller(request, flagSensors=None, tester=None):
    """ activate or not the sensors by api  """
    global scheduler
    if flagSensors == 'on':
        scheduleYourSensors(scheduler, tester)
    elif flagSensors == 'off':
        stopTheSensors(scheduler)
        scheduler = BackgroundScheduler()
    return HttpResponseRedirect('/')


def getAdeline(request):
    return render(request, 'tmplinear.html')
