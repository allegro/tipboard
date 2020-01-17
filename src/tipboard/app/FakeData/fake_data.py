import json
from src.tipboard.app.applicationconfig import getRedisPrefix
from src.tipboard.app.FakeData.fakeTilesText import getFakeText, getFakeFancyListing, getFakeJustValue
from src.tipboard.app.FakeData.fakeTilesText import getFakeListing, getFakeSimplePercentg, getFakeBigValue
from src.tipboard.app.FakeData.fakechartJS import getFakePieChart, getFakeBarChart, getFakeVbarChart
from src.tipboard.app.FakeData.fakechartJS import getFakeNormChart, getFakeCumulFlow, getFakeLineChart
from src.tipboard.app.FakeData.fakechartJS import getFakeDoughnutChart, getFakePolarareaChart, getFakeRadarChart


def buildSwicthPythonFfso_o():
    return dict(pie_chart=getFakePieChart,
                line_chart=getFakeLineChart,
                cumulative_flow=getFakeCumulFlow,
                bar_chart=getFakeBarChart,
                norm_chart=getFakeNormChart,
                doughnut_chart=getFakeDoughnutChart,
                radar_chart=getFakeRadarChart,
                polararea_chart=getFakePolarareaChart,
                vbar_chart=getFakeVbarChart,
                big_value=getFakeBigValue,
                just_value=getFakeJustValue,
                simple_percentage=getFakeSimplePercentg,
                text=getFakeText,
                listing=getFakeListing,
                fancy_listing=getFakeFancyListing)


def buildFakeDataFromTemplate(tile_id, template_name, cache):
    print(f'Building fake data for {tile_id} as template: {template_name}')
    data = dict()
    ptrToFake = buildSwicthPythonFfso_o()
    if template_name in ptrToFake:
        if template_name in ptrToFake:
            data = ptrToFake[template_name](tile_id, template_name)
        if cache is not None:
            cache.redis.set(name=getRedisPrefix(tile_id), value=json.dumps(data))
    return data


def buildFakeData(tile_id, template_name):
    data = dict()
    ptrToFake = buildSwicthPythonFfso_o()
    if template_name in ptrToFake:
        if template_name in ptrToFake:
            data = ptrToFake[template_name](tile_id, template_name)
    # le but cest de généré un max de dataset pour répondre au besoin lorsqu'on update une chart
    # il faudra mettre un nombre max de dataset du coup
    # dans fakeChartJS il faudra update les methode de creation de chart pour modifier le nombre de dataset
    return
