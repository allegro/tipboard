# import json
# from src.tipboard.app.utils import getTimeStr, buildBasicDataset
#
#
# def getLabel(data):
#     extractLabel = data['plot_data'][0] if len(data['plot_data'][0]) > len(data['plot_data'][1]) \
#         else data['plot_data'][1]
#     return [i[0] for i in extractLabel]
#
#
# def updateDatav1tov2_norm(data):
#     data['datasets'] = list()
#     if 'plot_data' in data:
#         data['labels'] = getLabel(data)
#         data['plot_data'][0] = [i[1] for i in data['plot_data'][0]]
#         data['plot_data'][1] = [i[1] for i in data['plot_data'][1]]
#         data['datasets'].append(buildBasicDataset(data=data['plot_data'][0], seriesNumber=1, borderColor=True))
#         data['datasets'].append(buildBasicDataset(data=data['plot_data'][1], seriesNumber=2, borderColor=True))
#         del data['plot_data']
#     else:
#         data['labels'] = [x for x in range(len(data['datasets'][0]))]
#     if 'description' in data:
#         data['title'] = {'text': data['description'], 'display': True}
#         del data['description']
#     elif 'title' in data:
#         title = data['title']
#         del data['title']
#         data['title'] = {'text': title, 'display': True}
#     else:
#         data['title'] = {'text': '', 'display': False}
#     return json.dumps(data)
#
#
# def updateDatav1tov2_linechart(tileData):
#     return json.dumps(tileData)
#
#
# def updateDatav1tov2_barchart(data):
#     data['labels'] = data.pop('ticks')
#     data['datasets'] = list()
#     if 'serie_list' in data:
#         for serie_list in data['series_list']:
#             data['datasets'].append(dict(data=serie_list))
#         del data['series_list']
#     return json.dumps(data)
#
#
# def updateDatav1tov2_piechart(data):
#     print(f"data was {data['pie_data']}")
#     data['pie_data_value'] = list()
#     data['labels'] = list()
#     data['pie_data_tag'] = list()
#     if 'pie_data' in data:
#         for elem_pie_data in data['pie_data']:
#             data['labels'].append(elem_pie_data[0])
#             data['pie_data_value'].append(elem_pie_data[1])
#             data['pie_data_tag'].append(elem_pie_data[0])
#         del data['pie_data']
#     return json.dumps(data)
#
#
# def updateDatav1tov2(tileType, tileData):
#     tileData = json.loads(tileData)
#     print(f"{getTimeStr()} (+) AntiRegression type({tileType}): {tileData}")
#     print("{getTimeStr()} (+) ----- WIP")
#     if 'pie_chart' in tileType:
#         return updateDatav1tov2_piechart(tileData)
#     elif 'bar_chart' in tileType:
#         return updateDatav1tov2_barchart(tileData)
#     elif 'norm_chart' in tileType:
#         updateDatav1tov2_norm(tileData)
#     elif tileType in ['line_chart', 'norm_chart', 'cumulative_flow']:
#         return updateDatav1tov2_linechart(tileData)
#     return json.dumps(tileData)
