import time, random
from src.sensors.utils import end, sendUpdateByApi


def executeScriptToGetData():
    """ Choose randomly a iframe widget from the beautiful matomo project """
    url1 = 'https://demo.matomo.org/index.php?module=Widgetize&action=iframe&disableLink=0&widget=1&' + \
           'moduleToWidgetize=Live&actionToWidgetize=getSimpleLastVisitCount&idSite=62&period=day&' + \
           'date=yesterday&disableLink=1&widget=1'
    url2 = 'https://demo.matomo.org/index.php?module=Widgetize&action=iframe&disableLink=0&widget=1&' + \
           'moduleToWidgetize=UserCountryMap&actionToWidgetize=realtimeMap&idSite=62&period=day&' + \
           'date=yesterday&disableLink=1&widget=1'
    url3 = 'https://demo.matomo.org/index.php?module=Widgetize&action=iframe&' \
           'containerId=VisitOverviewWithGraph&disableLink=0&widget=1&moduleToWidgetize=CoreHome&' \
           'actionToWidgetize=renderWidgetContainer&idSite=62&period=day&date=yesterday&disableLink=1&widget=1'
    url4 = 'https://demo.matomo.org/index.php?module=Widgetize&action=iframe&secondaryDimension=eventName&' \
           'disableLink=0&widget=1&moduleToWidgetize=Events&actionToWidgetize=getAction&idSite=62' \
           '&period=day&date=yesterday&disableLink=1&widget=1'
    url5 = 'https://demo.matomo.org/index.php?module=Widgetize&action=iframe&forceView=1&viewDataTable=sparklines' \
           '&disableLink=0&widget=1&moduleToWidgetize=VisitFrequency&actionToWidgetize=get&idSite=62&' \
           'period=day&date=yesterday&disableLink=1&widget=1'
    url6 = 'https://demo.matomo.org/index.php?module=Widgetize&action=iframe&disableLink=0&widget=1&moduleTo' \
           'Widgetize=Actions&actionToWidgetize=getPageUrls&idSite=62&period=day&date=yesterday&disableLink=1&widget=1'
    url7 = 'https://demo.matomo.org/index.php?module=Widgetize&action=iframe&containerId=EcommerceOverview&' \
           'disableLink=0&widget=1&moduleToWidgetize=CoreHome&actionToWidgetize=renderWidgetContainer&idSite=62&' \
           'period=day&date=yesterday&disableLink=1&widget=1'
    choiceList = [url1, url2, url3, url4, url5, url6, url7,
                  url6, url7, url1, url2, url3, url4, url5, url6, url7, url1, url2, url3, url4, url5, url6, url7]
    return {'url': random.choice(choiceList)}


def sonde21(tester=None, tile_id='iframe_ex'):
    start_time = time.time()
    data = executeScriptToGetData()
    answer = sendUpdateByApi(tileId=tile_id, data=data, tileTemplate='iframe', tester=tester)
    end(title=f'sensor21 -> -> {tile_id}', startTime=start_time, tipboardAnswer=answer, tileId=tile_id)
