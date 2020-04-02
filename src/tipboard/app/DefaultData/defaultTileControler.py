import json
from src.tipboard.app.applicationconfig import getRedisPrefix
from src.tipboard.app.DefaultData.defaultTileChartJs import getDefaultPieChart, getDefaultBarChart
from src.tipboard.app.DefaultData.defaultTileChartJs import getDefaultPolarareaChart, getDefaultRadarChart
from src.tipboard.app.DefaultData.defaultTileChartJs import getDefaultDoughnutChart, getDefaultLineChart
from src.tipboard.app.DefaultData.defaultTileChartJs import getDefaultNormChart, getDefaultCumulFlow
from src.tipboard.app.DefaultData.defaultTileChartJs import getDefaultTsGaugeChart, getDefaultRadialGaugeChart
from src.tipboard.app.DefaultData.defaultTileChartJs import getDefaultLinearGaugeChart, getDefaultVLinearGaugeChart
from src.tipboard.app.DefaultData.defaultTilesText import getDefaultText, getDefaultListing, getDefaultJustValue
from src.tipboard.app.DefaultData.defaultTilesText import getDefaultSimplePercentg, getDefaultBigValue
from src.tipboard.app.DefaultData.defaultTilesText import getDefaultCustomTile


def getDefaultStreamTile():
    return {
        'data': dict(url='https://video-auth1.iol.pt/beachcam/pourville/playlist.m3u8'),
        'meta': {}
    }


def getDefaultIframeTile():
    return {
        'data': dict(url='https://demo.matomo.org/index.php?'
                         'module=Widgetize&action=iframe&disableLink=0&widget=1&'
                         'moduleToWidgetize=Live&actionToWidgetize=getSimpleLastVisitCount&'
                         'idSite=62&period=day&date=yesterday&disableLink=1&widget=1')
    }


def add_template_and_id(little_dict, tile_id, template_name):
    if little_dict is not None:
        little_dict['id'] = tile_id
        little_dict['tile_template'] = template_name
    return little_dict


def buildSwicthPythonFfso_o():
    return dict(pie_chart=getDefaultPieChart,
                line_chart=getDefaultLineChart,
                cumulative_flow=getDefaultCumulFlow,
                bar_chart=getDefaultBarChart,
                vbar_chart=getDefaultBarChart,
                norm_chart=getDefaultNormChart,
                half_doughnut_chart=getDefaultDoughnutChart,
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
    ptrToFuncUpdateTile = buildSwicthPythonFfso_o()
    if template_name in ptrToFuncUpdateTile:
        functionTileUpdate = ptrToFuncUpdateTile[template_name]
        tileData = add_template_and_id(functionTileUpdate(), tile_id, template_name)
        if cache is not None:
            tileData = json.dumps(tileData)
            cache.redis.set(name=getRedisPrefix(tile_id), value=tileData)
            return tileData
        print(f'(-) Error with tile:{template_name}')
    else:
        print(f'(-) Error no update function for tile: {template_name}')
    return None
