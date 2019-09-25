import json
from src.tipboard.app.applicationconfig import getRedisPrefix, getIsoTime


def getFakeText(tile_id, template_name):
    return dict()


def getFakePieChart(tile_id, template_name):
    return {
        "id": tile_id,
        "tile_template": template_name,
        "data": {
            "title": tile_id,
            "label": "Label",
            "pie_data_tag": ["Approved", "Pending", "Denied"],
            "pie_data_value": [55, 12, 33]
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
            "labels": ["00h", "01h", "02h", "03h", "04h", "05h", "06h", "07h", "08h", "09h", "10h", "11h", "12h", "13h",
                       "14h", "15h", "16h", "17h", "18h", "19h", "20h", "21h", "22h", "23h", "24h"],
            "datasets": [{
                'data': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
                'label': "Hier",
                'borderColor': "#3e95cd",
                'trendlineLinear': {
                    'style': "#3e95cd",
                    'lineStyle': "dotted",
                    'width': 2
                }
            }, {
                'data': [5, 6, 4, 1, 3, 9, 10, 11, 12, 19, 30, 31, 32, 34, 33, 32, 31, 20, 19, 18, 17, 16, 15, 14],
                'label': "Live",
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
                    'text': 'LineChart Demo',
                    'color': '#FFFFFF'
                },
                'scales': {
                    'xAxes': [{
                        'display': True,
                        "gridLines": {
                            "color": "#52525252",
                        }
                    }],
                    'yAxes': [{
                        'display': True,
                        'ticks': {
                            'beginAtZero': True,
                            'max': 40
                        },
                        "gridLines": {
                            "color": "#52525252",
                        }
                    }]
                },
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
                'data': [0, 2, 0.5, 1, 1, 1, 2, 2, 1, 1],
                'label': "label1",
                'borderColor': "#3e95cd",
                'fill': True,
                'backgroundColor': "rgba(62, 149, 205, 0.8)"
            }, {
                'data': [0, 4, 0, 0, 1, 0, 0, 3, 0, 0],
                'label': "label2",
                'borderColor': "#72bf44",
                'fill': True,
                'backgroundColor': "rgba(114, 191, 68, 0.8)"
            }]
        },
        "meta": {
            'options': {
                'elements': {
                    'line': {
                        'tension': 0
                    }
                },
                'title': {
                    'display': True,
                    'text': 'Cumulative Flow Demo'
                },
                "scales": {
                    "xAxes": [{
                        "gridLines": {
                            "color": "#52525252",
                        }
                    }],
                    "yAxes": [{
                        "gridLines": {
                            "color": "#52525252",
                        }
                    }]
                }
            }
        },
        "modified": getIsoTime()
    }


def getFakeSimplePercentg(tile_id, template_name):
    return {
        "tile_template": template_name,
        "meta": {
            "big_value_color": "#4CAF50",
            "fading_background": False
        },
        "data": {
            "title": "title",
            "description": "description",
        },
        "modified": getIsoTime(),
        "id": tile_id
    }


def getFakeListing(tile_id, template_name):
    return {
        "tile_template": template_name,
        "meta": {
            "fading_background": False
        },
        "data": {
            "items": [
              "Leader: 42",
              "Product Owner: 1",
              "Scrum Master: 1",
              "Developer: 1",
              "U.X: 1"
            ]
          },
        "modified": getIsoTime(),
        "id": tile_id
    }


def getFakeBarChart(tile_id, template_name):
    return {
        "id": tile_id,
        "tile_template": template_name,
        "data": {
            "labels": ["Last(n)", "n-1", "n-2", ],
            "data": [12, 19, 3]
        },
        "meta": {
            'backgroundColor': ["#3e95cd", "#8e5ea2", "#3cba9f"],
            'options': {
                'legend': {'display': False},
                'title': {
                    'display': True,
                    'text': '# Velocity of squad'
                },
                "scales": {
                    "xAxes": [{
                        "gridLines": {
                            "color": "#52525252",
                        }
                    }],
                    "yAxes": [{
                        "gridLines": {
                            "color": "#52525252",
                        },
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
    return {
        "tile_template": template_name,
        "meta": {
            "big_value_color": "#4CAF50",
            "fading_background": False
        },
        "data": {
            "title": "title",
            "description": "description",
        },
        "modified": getIsoTime(),
        "id": tile_id
    }


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
        },
        "modified": getIsoTime(),
        "id": tile_id
    }


def getFakeJustValue(tile_id, template_name):
    return {
        "tile_template": template_name,
        "meta": {
            "big_value_color": "#4CAF50",
            "fading_background": False
        },
        "data": {
            "title": "title",
            "description": "description",
        },
        "modified": getIsoTime(),
        "id": tile_id
    }


def getFakeAdvancedPlot(tile_id, template_name):
    return {
        "tile_template": template_name,
        "meta": {
            "big_value_color": "#4CAF50",
            "fading_background": False
        },
        "data": {
            "title": "title",
            "description": "description",
        },
        "modified": getIsoTime(),
        "id": tile_id
    }


def getFakeNormChart(tile_id, template_name):
    return {
        "id": tile_id,
        "tile_template": template_name,
        "data": {
            "labels": [1, 3, 5, 7, 9, 11],
            "datasets": [{
                'data': [2, 20, 13, 33, 85, 100],
                'label': "SERIES 2",
                'borderColor': "#3e95cd",
                'fill': False
            }, {
                'data': [2, 8, 10, 15, 80, 120],
                'label': "SERIES 1",
                'borderColor': "#8e5ea2",
                'fill': False
            }]
        },
        "meta": {
            'backgroundColor': ["#3e95cd", "#8e5ea2", ],
            'options': {
                'title': {
                    'display': True,
                    'text': 'Curve Comparaison'
                },
            "scales": {
                "xAxes": [{
                    "gridLines": {
                    "color": "#52525252",
                    }
                }],
                "yAxes": [{
                    "gridLines": {
                    "color": "#52525252",
                    }
                }]
            }
            }
        },
        "modified": getIsoTime()
    }


def getFakeDoughnutChart(tile_id, template_name):
    return {
        "id": tile_id,
        "tile_template": template_name,
        "data": {
            'labels': ["Africa", "Asia", "Europe", "Latin America", "North America"],
            'datasets': [
                {
                    'label': "Population (millions)",
                    'backgroundColor': ["#7b1fa2", "#1976d2", "#8e5ea2", "#ffa000", "#ffeb3b"],
                    'data': [2478, 5267, 734, 784, 433]
                }
            ]
        },
        "meta": {
            'title': {
                'display': True,
                'text': 'Predicted world population (millions) in 2050'
            }
        },
        "modified": getIsoTime()
    }


def getFakeRadarChart(tile_id, template_name):
    return {
        "id": tile_id,
        "tile_template": template_name,
        "data": {
            'labels': ["Label 1", "Label 2", "Label 3", "Label 4", "Label 5"],
            'datasets': [
                {
                    'label': "Series 1",
                    'fill': True,

                    'backgroundColor': "rgba(114, 191, 68, 0.8)",
                    'borderColor': "rgba(114, 191, 68, 0.8)",

                    'pointBorderColor': "rgba(114, 191, 68, 0.95)",
                    'pointBackgroundColor': "rgba(255, 255, 255, 0.5)",
                    'data': [8.77, 55.61, 21.69, 6.62, 6.82]
                }, {
                    'label': "Series 2",
                    'fill': True,

                    'backgroundColor': "rgba(62, 149, 205, 0.8)",
                    'borderColor': "rgba(62, 149, 205, 0.8)",

                    'pointBorderColor': "rgba(62, 149, 205, 0.95)",
                    'pointBackgroundColor': "rgba(255, 255, 255, 0.5)",
                    'data': [18, 10, 36, 36, 40]
                }
            ]
        },
        "meta": {
            'title': {
                'display': True,
                'text': 'Radar Demo',
                'borderColor': 'rgba(255, 255, 255, 1)'
            },
            'scale': {
                'gridLines': {
                    'color': ['#525252', '#525252', '#525252', '#525252', '#525252', '#525252', '#525252']
                },
                'angleLines': {'color': '#525252'},
                'ticks': {
                    'display': False
                }
            }

        },
        "modified": getIsoTime()
    }


def getFakePolarareaChart(tile_id, template_name):
    return {
        "id": tile_id,
        "tile_template": template_name,
        "data": {
            'labels': ["Africa", "Asia", "Europe", "Latin America", "North America"],
            'datasets': [
                {
                    'label': "Population (millions)",
                    'backgroundColor': ["#3e95cd", "#8e5ea2", "#3cba9f", "#e8c3b9", "#c45850"],
                    'data': [2478, 5267, 734, 784, 433],
                }
            ]
        },
        "meta": {
            "options": {
                'title': {
                    'display': True,
                    'text': 'Predicted world population (millions) in 2050'
                },
                'elements': {
                  'arc': {
                    'borderColor': "#52525252",
                    'borderWidth': 2
                  }
                }
            }
        },
        "modified": getIsoTime()
    }


def getFakeVbarChart(tile_id, template_name):
    return getFakeBarChart(tile_id, template_name)


def buildFakeDataForChartJS(tile_id, template_name):
    if template_name == "pie_chart":
        return getFakePieChart(tile_id, template_name)
    elif template_name == "line_chart":
        return getFakeLineChart(tile_id, template_name)
    elif template_name == "cumulative_flow":
        return getFakeCumulFlow(tile_id, template_name)
    elif template_name == "bar_chart":
        return getFakeBarChart(tile_id, template_name)
    elif template_name == "norm_chart":
        return getFakeNormChart(tile_id, template_name)

    elif template_name == "doughnut_chart":
        return getFakeDoughnutChart(tile_id, template_name)
    elif template_name == "radar_chart":
        return getFakeRadarChart(tile_id, template_name)
    elif template_name == "polararea_chart":
        return getFakePolarareaChart(tile_id, template_name)
    elif template_name == "vbar_chart":
        return getFakeVbarChart(tile_id, template_name)
    else:
        print(f"ERROR WITH FAKE DATA ON {tile_id}", flush=True)
        return None


def buildFakeDataFromTemplate(tile_id, template_name, cache):
    print(f"Building fake data for {tile_id} as template: {template_name}")
    data = dict()
    if template_name == "text":
        data = getFakeText(tile_id, template_name)
    elif template_name == "simple_percentage":
        data = getFakeSimplePercentg(tile_id, template_name)
    elif template_name == "listing":
        data = getFakeListing(tile_id, template_name)
    elif template_name == "fancy_listing":
        data = getFakeFancyListing(tile_id, template_name)
    elif template_name == "big_value":
        data = getFakeBigValue(tile_id, template_name)
    elif template_name == "just_value":
        data = getFakeJustValue(tile_id, template_name)
    elif template_name == "empty":
        pass
    else:
        data = buildFakeDataForChartJS(tile_id, template_name)
    if cache is not None:
        cache.redis.set(name=getRedisPrefix(tile_id), value=json.dumps(data))
    return data
