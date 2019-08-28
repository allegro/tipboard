import json
from src.tipboard.app.applicationconfig import getRedisPrefix, getIsoTime

def getFakeText(tile_id, template_name):
    pass


def getFakePieChart(tile_id, template_name):
    return {
          "id": tile_id,
          "tile_template": template_name,
          "data": {
            "title": tile_id,
            "label": "Label",
            "pie_data_tag": ["Pie 1", "Pie 2", "Pie 3"],
            "pie_data_value": [50, 25, 25]
          },
          "meta": {
              'backgroundColor': ["#3e95cd", "#72bf44", "#8e5ea2"]
          },
          "modified": getIsoTime()
        }


def getFakeLineChart(tile_id, template_name):
    return {
          "id": tile_id,
          "tile_template": template_name,
          "data": {
            "labels": ["23.09", "24.09", "25.09", "26.09", "27.09", "28.09", "29.09"],
            "datasets": [{
                'data': [8326, 260630, 240933, 229639, 190240, 125272, 3685],
                'label': "label1",
                'borderColor': "#3e95cd",
                'trendlineLinear': {
                    'style': "#3e95cd",
                    'lineStyle': "dotted",
                    'width': 2
                }
            }, {
                'data': [3685, 125272, 190240, 229639, 240933, 260630, 108326],
                'label': "label2",
                'borderColor': "#72bf44",
                'trendlineLinear': {
                    'style': "#3e95cd",
                    'lineStyle': "#72bf44",
                    'width': 2
                }
            }]
          },
          "meta": {
            'backgroundColor': ["#3e95cd", "#8e5ea2"],
            'options': {
                'responsive': True,
                'elements': {
                    'line': {
                        'tension': 0
                    }
                },
                'title': {
                    'display': True,
                    'text': 'LineChart Demo'
                }
            }
          },
          "modified": getIsoTime()
    }


def getFakeCumulFlow(tile_id, template_name):
    return {
          "id": tile_id,
          "tile_template": template_name,
          "data": {
            "labels": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            "datasets": [{
                'data': [0, 2, 0, 1, 1, 1, 2, 2, 1, 1],
                'label': "label1",
                'borderColor': "#3e95cd",
                'fill': True,
                'backgroundColor': "#3e95cd"
            }, {
                'data': [0, 5, 0, 0, 1, 0, 0, 3, 0, 0],
                'label': "label2",
                'borderColor': "#72bf44",
                'fill': True,
                'backgroundColor': "#72bf44"
            }]
          },
          "meta": {
            'backgroundColor': ["#3e95cd", "#8e5ea2", "#3cba9f"],
            'options': {
                'elements': {
                    'line': {
                        'tension': 0
                    }
                },
                'title': {
                    'display': True,
                    'text': 'Cumulative Flow Demo'
                }
            }
          },
          "modified": getIsoTime()
    }


def getFakeSimplePercentg(tile_id, template_name):
    pass


def getFakeListing(tile_id, template_name):
    pass


def getFakeBarChart(tile_id, template_name):
    return {
          "id": tile_id,
          "tile_template": template_name,
          "data": {
            "labels": ["label1", "label2", "label3", "label4", "label5"],
            "label": "# Velocity of squad",
            "data": [12, 19, 3]
          },
          "meta": {
            'backgroundColor': ["#3e95cd", "#8e5ea2", "#3cba9f"],
            'options': {
               'legend': {'display': False },
               'title': {
                   'display': True,
                   'text': 'Predicted world population (millions) in 2050'
                },
                'scales': {
                    'yAxes': [{
                        'ticks': {
                            'beginAtZero': True
                        }
                    }]
                }
            }
          },
          "modified": getIsoTime()
        }


def getFakeFancyListing(tile_id, template_name):
    pass


def getFakeBigValue(tile_id, template_name):
    return {
          "tile_template": template_name,
          "meta": {
            "big_value_color": "#4CAF50",
            "fading_background": False
          },
          "data": {
            "title": "title",
            "description": "description",
            "big-value": 42,
            "upper-left-label": "up-left-label",
            "upper-left-value": 4,
            "lower-left-label": "low-left-label",
            "lower-left-value": 2,
            "upper-right-label": "up-right-label",
            "upper-right-value": 24,
            "lower-right-label": "low-right-label",
            "lower-right-value": 4242
          },
          "modified": getIsoTime(),
          "id": tile_id
        }


def getFakeJustValue(tile_id, template_name):
    pass


def getFakeAdvancedPlot(tile_id, template_name):
    pass


def getFakeNormChart(tile_id, template_name):
    return {
          "id": tile_id,
          "tile_template": template_name,
          "data": {
            "labels": [1500, 1600, 1700, 1750, 1800, 1850, 1900, 1950, 1999, 2050],
            "datasets": [{
                'data': [86, 114, 106, 106, 107, 111, 133, 221, 783, 2478],
                'label': "Africa",
                'borderColor': "#3e95cd",
                'fill': False
            }, {
                'data': [282, 350, 411, 502, 635, 809, 947, 1402, 3700, 5267],
                'label': "Asia",
                'borderColor': "#8e5ea2",
                'fill': False
            }]
          },
          "meta": {
            'backgroundColor': ["#3e95cd", "#8e5ea2", "#3cba9f"],
            'options': {
                'title': {
                    'display': True,
                    'text': 'World population per region (in millions)'
                }
            }
          },
          "modified": getIsoTime()
    }


def buildFakeDataFromTemplate(tile_id, template_name, cache):
    print(f"Building fake data for {tile_id} as template: {template_name}")
    data = dict()
    if template_name == "text":
       data = getFakeText(tile_id, template_name)
    elif template_name == "pie_chart" or template_name == "pie_chartjs":
       data = getFakePieChart(tile_id, template_name)
    elif template_name == "line_chart" or template_name == "line_chartjs":
        data = getFakeLineChart(tile_id, template_name)
    elif template_name == "cumulative_flow" or template_name == "cumulative_flowjs":
        data = getFakeCumulFlow(tile_id, template_name)
    elif template_name == "simple_percentage":
        data = getFakeSimplePercentg(tile_id, template_name)
    elif template_name == "listing":
        data = getFakeListing(tile_id, template_name)
    elif template_name == "bar_chart" or template_name == "bar_chartjs":
        data = getFakeBarChart(tile_id, template_name)
    elif template_name == "norm_chart" or template_name == "norm_chartjs":
        data = getFakeNormChart(tile_id, template_name)
    elif template_name == "fancy_listing":
        data = getFakeFancyListing(tile_id, template_name)
    elif template_name == "big_value":
        data = getFakeBigValue(tile_id, template_name)
    elif template_name == "just_value":
        data = getFakeJustValue(tile_id, template_name)
    elif template_name == "advanced_plot":
        data = getFakeAdvancedPlot(tile_id, template_name)
    elif template_name == "empty":
        pass
    else:
        print(f"ERROR WITH FAKE DATA ON {tile_id}")
    cache.redis.set(name=getRedisPrefix(tile_id), value=json.dumps(data))
    return data