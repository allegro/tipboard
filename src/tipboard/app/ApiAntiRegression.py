import json
from src.tipboard.app.utils import getTimeStr


def updateDatav1tov2_linechart(data):
    # try:
    #     data = None
    # except Exception:
    #     print(f"{getTimeStr()} (-) Error in updateDatav1tov2_piechart")
    return data


# def updateDatav1tov2_cumul(data):
#     success = True
#     try:
#         data = None
#     except Exception:
#         print(f"{getTimeStr()} (-) Error in updateDatav1tov2_piechart")
#         success = False
#     return data, success
#
#
# def updateDatav1tov2_normchart(data):
#     success = True
#     try:
#         data = None
#     except Exception:
#         print(f"{getTimeStr()} (-) Error in updateDatav1tov2_piechart")
#         success = False
#     return data, success


def updateDatav1tov2_barchart(data):
    data['labels'] = data.pop('ticks')
    data['datasets'] = list()
    for serie_list in data['series_list']:
        dataset = dict()
        dataset['data'] = serie_list
        data['datasets'].append(dataset)
    del data['series_list']
    print(f"{getTimeStr()} (+) AntiRegression now : {data}")
    return json.dumps(data)


def updateDatav1tov2_piechart(data):
    print(f"data was {data['pie_data']}")
    data['pie_data_value'] = list()
    data['labels'] = list()
    data['pie_data_tag'] = list()
    for elem_pie_data in data['pie_data']:
        data['labels'].append(elem_pie_data[0])
        data['pie_data_value'].append(elem_pie_data[1])
        data['pie_data_tag'].append(elem_pie_data[0])
    del data['pie_data']
    print(f"data is now {data}")
    return json.dumps(data)


def updateDatav1tov2(tileType, tileData):
    tileData = json.loads(tileData)
    print(f"{getTimeStr()} (+) AntiRegression type({tileType}): {tileData}")
    if 'pie_chart' in tileType:
        return updateDatav1tov2_piechart(tileData)
    elif 'bar_chart' in tileType:
        return updateDatav1tov2_barchart(tileData)
    elif ('line_chart' or 'norm_chart' or 'cumulative_flow') in tileType:
        return updateDatav1tov2_linechart(tileData)
    else:
        return json.dumps(tileData)
