import json
from src.tipboard.app.applicationconfig import getRedisPrefix
from src.tipboard.app.FakeData.fakeTilesText import getFakeText, getFakeJustValue
from src.tipboard.app.FakeData.fakeTilesText import getFakeListing, getFakeSimplePercentg, getFakeBigValue
from src.tipboard.app.FakeData.fakechartJS import getFakePieChart, getFakeBarChart, getFakeVbarChart
from src.tipboard.app.FakeData.fakechartJS import getFakeNormChart, getFakeCumulFlow, getFakeLineChart
from src.tipboard.app.FakeData.fakechartJS import getFakePolarareaChart, getFakeRadarChart
from src.tipboard.app.FakeData.fakechartJS import getFakeHalfDoughnutChart, getFakeDoughnutChart
from src.tipboard.app.FakeData.fakechartJS import getFakeTsGaugeChart, getFakeRadialGaugeChart, getFakeLinearGaugeChart
from src.tipboard.app.FakeData.fakechartJS import getFakeVLinearGaugeChart


def getStreamTile(tile_id, template_name):
    return {
        'id': tile_id, 'tile_template': template_name,
        'data': dict(url="https://video-auth1.iol.pt/beachcam/pourville/playlist.m3u8"),
        'meta': {}
    }


def getIframeTile(tile_id, template_name):
    return {
        'id': tile_id, 'tile_template': template_name,
        'data': dict(url="https://demo.matomo.org/index.php?"
                         "module=Widgetize&action=iframe&disableLink=0&widget=1&"
                         "moduleToWidgetize=Live&actionToWidgetize=getSimpleLastVisitCount&"
                         "idSite=62&period=day&date=yesterday&disableLink=1&widget=1"),
        'meta': {}
    }

# url = https://demo.matomo.org/index.php?module=Widgetize&action=iframe&disableLink=0&widget=1&
# moduleToWidgetize=UserCountryMap&actionToWidgetize=realtimeMap&idSite=62&period=day&
# date=yesterday&disableLink=1&widget=1


# url = https://demo.matomo.org/index.php?module=Widgetize&action=iframe&disableLink=0&widget=1&
# moduleToWidgetize=Live&actionToWidgetize=getSimpleLastVisitCount&idSite=62&period=day&
# date=yesterday&disableLink=1&widget=1


def buildSwicthPythonFfso_o():
    return dict(pie_chart=getFakePieChart,
                line_chart=getFakeLineChart,
                cumulative_flow=getFakeCumulFlow,
                bar_chart=getFakeBarChart,
                vbar_chart=getFakeVbarChart,
                norm_chart=getFakeNormChart,
                half_doughnut_chart=getFakeHalfDoughnutChart,
                doughnut_chart=getFakeDoughnutChart,
                gauge_chart=getFakeTsGaugeChart,
                radial_gauge_chart=getFakeRadialGaugeChart,
                radar_chart=getFakeRadarChart,
                linear_gauge_chart=getFakeLinearGaugeChart,
                vlinear_gauge_chart=getFakeVLinearGaugeChart,
                polararea_chart=getFakePolarareaChart,
                big_value=getFakeBigValue,
                just_value=getFakeJustValue,
                simple_percentage=getFakeSimplePercentg,
                text=getFakeText,
                listing=getFakeListing,
                iframe=getIframeTile,
                stream=getStreamTile)


def buildFakeDataFromTemplate(tile_id, template_name, cache):  # TODO: handle when tile is unknow
    data = dict()
    ptrToFake = buildSwicthPythonFfso_o()
    if template_name in ptrToFake:
        data = ptrToFake[template_name](tile_id, template_name)
    if cache is not None:
        cache.redis.set(name=getRedisPrefix(tile_id), value=json.dumps(data))
    return data
