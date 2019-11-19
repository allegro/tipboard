import json
from src.tipboard.app.applicationconfig import getRedisPrefix
from src.tipboard.app.FakeData.fakeTilesText import getFakeText, getFakeFancyListing, getFakeJustValue
from src.tipboard.app.FakeData.fakeTilesText import getFakeListing, getFakeSimplePercentg, getFakeBigValue
from src.tipboard.app.FakeData.fakechartJS import getFakePieChart, getFakeBarChart, getFakeVbarChart
from src.tipboard.app.FakeData.fakechartJS import getFakeNormChart, getFakeCumulFlow, getFakeLineChart
from src.tipboard.app.FakeData.fakechartJS import getFakeDoughnutChart, getFakePolarareaChart, getFakeRadarChart


def buildFakeDataForChartJS(tile_id, template_name):
    data = None
    if template_name == 'pie_chart':
        data = getFakePieChart(tile_id, template_name)
    elif template_name == 'line_chart':
        data = getFakeLineChart(tile_id, template_name)
    elif template_name == 'cumulative_flow':
        data = getFakeCumulFlow(tile_id, template_name)
    elif template_name == 'bar_chart':
        data = getFakeBarChart(tile_id, template_name)
    elif template_name == 'norm_chart':
        data = getFakeNormChart(tile_id, template_name)

    elif template_name == 'doughnut_chart':
        data = getFakeDoughnutChart(tile_id, template_name)
    elif template_name == 'radar_chart':
        data = getFakeRadarChart(tile_id, template_name)
    elif template_name == 'polararea_chart':
        data = getFakePolarareaChart(tile_id, template_name)
    elif template_name == 'vbar_chart':
        data = getFakeVbarChart(tile_id, template_name)
    else:
        print(f'ERROR WITH FAKE DATA ON {tile_id}', flush=True)
    return data


def buildDataFromValueTemplate(tile_id, template_name):
    if template_name == 'big_value':
        return getFakeBigValue(tile_id, template_name)
    elif template_name == 'just_value':
        return getFakeJustValue(tile_id, template_name)
    elif template_name == 'simple_percentage':
        return getFakeSimplePercentg(tile_id, template_name)
    else:
        return None


def buildFakeDataFromTemplate(tile_id, template_name, cache):
    print(f'Building fake data for {tile_id} as template: {template_name}')
    data = dict()
    if template_name == 'text':
        data = getFakeText(tile_id, template_name)
    elif template_name == 'listing':
        data = getFakeListing(tile_id, template_name)
    elif template_name == 'fancy_listing':
        data = getFakeFancyListing(tile_id, template_name)
    elif 'value' in template_name or 'percentage' in template_name:
        data = buildDataFromValueTemplate(tile_id, template_name)
    elif template_name != 'empty':
        data = buildFakeDataForChartJS(tile_id, template_name)
    if cache is not None:
        cache.redis.set(name=getRedisPrefix(tile_id), value=json.dumps(data))
    return data
