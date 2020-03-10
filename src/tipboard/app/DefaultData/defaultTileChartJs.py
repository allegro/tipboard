from src.tipboard.app.DefaultData.chartJsDatasetBuilder import buildDatasetBar, buildDatasetCumulFlow, \
    buildDatasetDoughnut
from src.tipboard.app.DefaultData.chartJsDatasetBuilder import buildDatasetLine, buildDatasetNorm, buildDatasetPolararea
from src.tipboard.app.DefaultData.chartJsDatasetBuilder import buildDatasetRadar, buildDatasetPie
from src.tipboard.app.properties import COLOR_TAB


def getDefaultLineChart():
    return {
        'data': {
            'title': {'text': 'LineChart Demo', 'color': '#FFFFFF'},
            'labels': [f'{i if i > 10 else f"0{i}"}h' for i in range(25)],
            'datasets': [
                buildDatasetLine(index=0, randomData=True, labelLenght=25),
                buildDatasetLine(index=1, randomData=True, labelLenght=25)
            ]
        },
        'meta': {
            'options': {
                'responsive': True, 'maintainAspectRatio': False, 'elements': {'line': {'tension': 0}},
                'scales': {
                    'xAxes': [{'display': True, 'gridLines': {'color': '#626262'}}],
                    'yAxes': [{'display': True, 'ticks': {'beginAtZero': True}, 'gridLines': {'color': '#626262'}}]
                },
            }
        }
    }


def getDefaultCumulFlow():
    return {
        'data': {
            'title': {'display': True, 'text': 'Cumulative Flow Demo'},
            'labels': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            'datasets': [
                buildDatasetCumulFlow(index=0, randomData=True, labelLenght=10),
                buildDatasetCumulFlow(index=1, randomData=True, labelLenght=10)
            ]
        },
        'meta': {
            'options': {
                'responsive': True,
                'maintainAspectRatio': False,
                'elements': {'line': {'tension': 0}},
                'scales': {
                    'xAxes': [{'gridLines': {'color': '#626262'}}],
                    'yAxes': [{'gridLines': {'color': '#626262'}}]
                }
            }
        }
    }


def getDefaultNormChart():
    return {
        'data': {
            'title': {'display': True, 'text': 'Curve Comparaison'}, 'labels': [1, 3, 5, 7, 9, 11],
            'datasets': [
                buildDatasetNorm(index=0, randomData=True, labelLenght=6),
                buildDatasetNorm(index=1, randomData=True, labelLenght=6)
            ]
        },
        'meta': {
            'backgroundColor': COLOR_TAB,
            'options': {
                'responsive': True, 'maintainAspectRatio': False,
                'scales': {
                    'xAxes': [{'gridLines': {'color': '#626262'}}],
                    'yAxes': [{'gridLines': {'color': '#626262'}}]
                }
            }
        }
    }


def getDefaultBarChart():
    return {
        'data': {
            'title': {'display': True, 'text': 'Bar Chart Demo'},
            'labels': ['Last (n)', 'n-1', 'n-2'],
            'datasets': [
                buildDatasetBar(index=0, randomData=True, labelLenght=3),
                buildDatasetBar(index=1, randomData=True, labelLenght=3)
            ]
        },
        'meta': {
            'options': {
                'responsive': True, 'maintainAspectRatio': False, 'legend': {'display': False},
                'scales': {
                    'xAxes': [{'gridLines': {'color': '#626262', 'display': False}}],
                    'yAxes': [{'gridLines': {'color': '#626262'}}]
                }
            }
        }
    }


def getDefaultPieChart():
    return {
        'data': {
            'title': {'display': True, 'text': 'PieChart Demo'}, 'labels': [f'Label {i + 1}' for i in range(5)],
            'borderColor': '#626262', 'datasets': [buildDatasetPie(randomData=True, labelLenght=5)]
        },
        'meta': {
            'responsive': True, 'maintainAspectRatio': False, 'backgroundColor': COLOR_TAB,
            'labels': {'fontColor': 'rgba(255, 255, 255, 0.80)'}, 'tooltips': {'enabled': False},
            'elements': {'arc': {}}
        }
    }


def getDefaultDoughnutChart():
    return {
        'data': {
            'title': {'display': True, 'text': 'Doughnut Demo'},
            'labels': [f'Label {i + 1}' for i in range(8)],
            'datasets': [buildDatasetDoughnut(randomData=False, labelLenght=8)]
        },
        'meta': {
            'options': {
                'responsive': True, 'maintainAspectRatio': False,
                'elements': {'arc': {'borderWidth': 1.0, 'borderColor': '#626262'}}
            }
        }
    }


def getDefaultRadialGaugeChart():
    return {
        'data': {
            'title': {'display': True, 'text': 'Radial Gauge Demo'}, 'labels': [f'Label 1'],
            'datasets': [{'data': [42], 'label': 'Label'}]
        },
        'meta': {
            'options': {
                'responsive': True, 'maintainAspectRatio': False, 'events': list(), 'showMarkers': True,
                'animation': {'animateRotate': True, 'animateScale': True},
                #    'rotation': -Math.PI / 2,
                'centerPercentage': 80, 'trackColor': 'rgb(204, 221, 238)', 'domain': [0, 50], 'roundedCorners': True,
                'centerArea': {
                    'displayText': True, 'fontFamily': None, 'fontColor': None, 'fontSize': None, 'padding': 4,
                    'backgroundImage': None, 'backgroundColor': None, 'text': None
                }
            }
        }
    }


def getDefaultLinearGaugeChart():
    return {
        'data': {
            'title': {'display': True, 'text': 'Linear Gauge Demo'}, 'labels': ['data 1', 'data 2', 'data 3'],
            'datasets': [
                {'label': 'data 1', 'data': [370], 'backgroundColor': COLOR_TAB[0], 'offset': 10, 'width': 10},
                {'label': 'data 2', 'data': [170], 'backgroundColor': COLOR_TAB[1], 'offset': 21, 'width': 10},
                {'label': 'data 3', 'data': [270], 'backgroundColor': COLOR_TAB[2], 'offset': 32, 'width': 10}
            ]
        },
        'meta': {
            'options': {'responsive': True, 'maintainAspectRatio': False, 'scale': {'horizontal': True}}
        }
    }


def getDefaultVLinearGaugeChart():
    data = getDefaultLinearGaugeChart()
    data['meta']['options']['scale']['horizontal'] = False
    return data


def getDefaultTsGaugeChart():
    return {
        'data': {
            'title': {'display': True, 'text': 'Gauge Demo'},
            'datasets': [
                {
                    'backgroundColor': ['#0fdc63', '#fd9704', '#ff7143'], 'borderWidth': 0,
                    'gaugeData': {'value': 7777, 'valueColor': '#ff7143'}, 'gaugeLimits': [0, 3000, 7000, 10000]
                }
            ]
        },
        'meta': {'options': {'responsive': True, 'maintainAspectRatio': False, 'events': list(), 'showMarkers': True}}
    }


def getDefaultRadarChart():
    return {
        'data': {
            'title': {'text': 'Radar Demo', 'borderColor': 'rgba(255, 255, 255, 1)'},
            'labels': [f'Label {i + 1}' for i in range(5)],
            'datasets': [
                buildDatasetRadar(index=0, randomData=True, labelLenght=5),
                buildDatasetRadar(index=1, randomData=True, labelLenght=5)
            ]
        },
        'meta': {
            'options': {
                'scale': {
                    'gridLines': {'color': ['#626262' for _ in range(8)]},
                    'angleLines': {'color': '#626262'}, 'ticks': {'display': False}
                },
                'responsive': True, 'maintainAspectRatio': False,
            }
        }
    }


def getDefaultPolarareaChart():
    return {
        'data': {
            'title': {'display': True, 'text': 'Polar area Demo'},
            'labels': [f'Serie {i + 1}' for i in range(4)],
            'datasets': [buildDatasetPolararea(randomData=True, labelLenght=4)]
        },
        'meta': {
            'options': {
                'responsive': True, 'maintainAspectRatio': False,
                'elements': {'arc': {'borderColor': '#626262', 'borderWidth': 2}},
                'scale': {
                    'gridLines': {'color': ['#626262' for _ in range(8)]},
                    'angleLines': {'color': '#626262'},
                    'ticks': {'display': False}
                }
            }
        }
    }
