import json
from src.tipboard.app.applicationconfig import getRedisPrefix
from src.tipboard.app.DefaultData.defaultTilesText import getDefaultText, getDefaultListing, getDefaultJustValue
from src.tipboard.app.DefaultData.defaultTilesText import getDefaultSimplePercentg, getDefaultBigValue
from src.tipboard.app.DefaultData.defaultTilesText import getDefaultCustomTile
from src.tipboard.app.DefaultData.defaultTileChartJs import getDefaultPieChart, getDefaultBarChart, getDefaultVbarChart
from src.tipboard.app.DefaultData.defaultTileChartJs import getDefaultPolarareaChart, getDefaultRadarChart
from src.tipboard.app.DefaultData.defaultTileChartJs import getDefaultHalfDoughnutChart, getDefaultDoughnutChart
from src.tipboard.app.DefaultData.defaultTileChartJs import getDefaultLineChart
from src.tipboard.app.DefaultData.defaultTileChartJs import getDefaultNormChart, getDefaultCumulFlow
from src.tipboard.app.DefaultData.defaultTileChartJs import getDefaultTsGaugeChart, getDefaultRadialGaugeChart
from src.tipboard.app.DefaultData.defaultTileChartJs import getDefaultLinearGaugeChart, getDefaultVLinearGaugeChart


def getDefaultStreamTile(tile_id, template_name):
    return {
        'id': tile_id, 'tile_template': template_name,
        'data': dict(url='https://video-auth1.iol.pt/beachcam/pourville/playlist.m3u8'),
        'meta': {}
    }


def getDefaultIframeTile(tile_id, template_name):
    return {
        'id': tile_id, 'tile_template': template_name,
        'data': dict(url='https://demo.matomo.org/index.php?'
                         'module=Widgetize&action=iframe&disableLink=0&widget=1&'
                         'moduleToWidgetize=Live&actionToWidgetize=getSimpleLastVisitCount&'
                         'idSite=62&period=day&date=yesterday&disableLink=1&widget=1'),
        'meta': {}
    }

# url = https://demo.matomo.org/index.php?module=Widgetize&action=iframe&disableLink=0&widget=1&
# moduleToWidgetize=UserCountryMap&actionToWidgetize=realtimeMap&idSite=62&period=day&
# date=yesterday&disableLink=1&widget=1


# url = https://demo.matomo.org/index.php?module=Widgetize&action=iframe&disableLink=0&widget=1&
# moduleToWidgetize=Live&actionToWidgetize=getSimpleLastVisitCount&idSite=62&period=day&
# date=yesterday&disableLink=1&widget=1


def buildSwicthPythonFfso_o():
    return dict(pie_chart=getDefaultPieChart,
                line_chart=getDefaultLineChart,
                cumulative_flow=getDefaultCumulFlow,
                bar_chart=getDefaultBarChart,
                vbar_chart=getDefaultVbarChart,
                norm_chart=getDefaultNormChart,
                half_doughnut_chart=getDefaultHalfDoughnutChart,
                doughnut_chart=getDefaultDoughnutChart,
                polararea_chart=getDefaultPolarareaChart,
                gauge_chart=getDefaultTsGaugeChart,
                radial_gauge_chart=getDefaultRadialGaugeChart,
                radar_chart=getDefaultRadarChart,
                linear_gauge_chart=getDefaultLinearGaugeChart,
                vlinear_gauge_chart=getDefaultVLinearGaugeChart,
                big_value=getDefaultBigValue,
                simple_percentage=getDefaultSimplePercentg,
                just_value=getDefaultJustValue,
                text=getDefaultText,
                listing=getDefaultListing,
                iframe=getDefaultIframeTile,
                stream=getDefaultStreamTile,
                custom=getDefaultCustomTile)


def buildFakeDataFromTemplate(tile_id, template_name, cache):  # TODO: handle when tile is unknow
    data = dict()
    ptrToFake = buildSwicthPythonFfso_o()
    if template_name in ptrToFake:
        data = ptrToFake[template_name](tile_id, template_name)
    if cache is not None:
        cache.redis.set(name=getRedisPrefix(tile_id), value=json.dumps(data))
    return data
