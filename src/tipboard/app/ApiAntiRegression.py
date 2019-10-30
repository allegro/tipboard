import json
from src.tipboard.app.utils import getTimeStr


def updateDatav1tov2_linechart(data):
    success = True
    try:
        data = None
    except Exception:
        print(f"{getTimeStr()} (-) Error in updateDatav1tov2_piechart")
        success = False
    return data, success


def updateDatav1tov2_cumul(data):
    success = True
    try:
        data = None
    except Exception:
        print(f"{getTimeStr()} (-) Error in updateDatav1tov2_piechart")
        success = False
    return data, success


def updateDatav1tov2_percentage(data):
    success = True
    try:
        data = None
    except Exception:
        print(f"{getTimeStr()} (-) Error in updateDatav1tov2_piechart")
        success = False
    return data, success


def updateDatav1tov2_listing(data):
    success = True
    try:
        data = None
    except Exception:
        print(f"{getTimeStr()} (-) Error in updateDatav1tov2_piechart")
        success = False
    return data, success


def updateDatav1tov2_bigvalue(data):
    success = True
    try:
        data = None
    except Exception:
        print(f"{getTimeStr()} (-) Error in updateDatav1tov2_piechart")
        success = False
    return data, success


def updateDatav1tov2_justvalue(data):
    success = True
    try:
        data = None
    except Exception:
        print(f"{getTimeStr()} (-) Error in updateDatav1tov2_piechart")
        success = False
    return data, success


def updateDatav1tov2_normchart(data):
    success = True
    try:
        data = None
    except Exception:
        print(f"{getTimeStr()} (-) Error in updateDatav1tov2_piechart")
        success = False
    return data, success


def updateDatav1tov2_barchart(data):
    success = True
    try:
        data['labels'] = data.pop('ticks')
        data['datasets'] = list()
        for serie_list in data['series_list']:
            dataset = dict()
            dataset['data'] = serie_list
            data['datasets'].append(dataset)
        del data['series_list']
    except FutureWarning:
        print(f"{getTimeStr()} (-) Error in updateDatav1tov2_piechart")
        success = False
    print(f"{getTimeStr()} (+) AntiRegression now : {data}")
    return json.dumps(data), success


def updateDatav1tov2_piechart(data):
    success = True
#    try:
    print(f"data was {data['pie_data']}")
    data['pie_data_value'] = list()
    data['labels'] = list()
    data['pie_data_tag'] = list()
    for elem_pie_data in data['pie_data']:
        data['labels'].append(elem_pie_data[0])
        data['pie_data_value'].append(elem_pie_data[1])
        data['pie_data_tag'].append(elem_pie_data[0])
    del data['pie_data']
    # except FutureWarning as e:
    #     print(f"{getTimeStr()} (-) Error in updateDatav1tov2_piechart:")
    #     success = False
    print(f"data is now {data}")
    return json.dumps(data), success


def updateDatav1tov2(tileType, tileData):
    tileData = json.loads(tileData)
    print(f"{getTimeStr()} (+) AntiRegression type({tileType}): {tileData}")
    if 'pie_chart' in tileType:
        return updateDatav1tov2_piechart(tileData)
    elif 'bar_chart' in tileType:
        return updateDatav1tov2_barchart(tileData)
    elif 'line_chart' in tileType:
        return updateDatav1tov2_linechart(tileData)
    elif 'norm_chart' in tileType:
        return updateDatav1tov2_normchart(tileData)
    elif 'cumulative_flow' in tileType:
        return updateDatav1tov2_cumul(tileData)
    elif 'big_value' in tileType:
        return updateDatav1tov2_bigvalue(tileData)
    elif 'listing' in tileType:
        return updateDatav1tov2_listing(tileData)
    elif 'simple_percentage' in tileType:
        return updateDatav1tov2_percentage(tileData)
    elif 'just_value' in tileType:
        return updateDatav1tov2_justvalue(tileData)
    return "Error type unknow", False
