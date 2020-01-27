from src.tipboard.app.applicationconfig import getIsoTime
from src.tipboard.app.FakeData.datasetbuilder import buildDatasetBar, buildDatasetCumulFlow, buildDatasetDoughnut
from src.tipboard.app.FakeData.datasetbuilder import buildDatasetLine, buildDatasetNorm, buildDatasetPolararea
from src.tipboard.app.FakeData.datasetbuilder import buildDatasetRadar, buildDatasetPie
from src.tipboard.app.properties import COLOR_TAB


def getFakeLineChart(tile_id, template_name):
    return {
        'id': tile_id, 'tile_template': template_name, 'modified': getIsoTime(),
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
                'responsive': True,
                'maintainAspectRatio': False,
                'elements': {
                    'line': {
                        'tension': 0
                    }
                },
                'scales': {
                    'xAxes': [{
                        'display': True,
                        'gridLines': {
                            'color': '#525252',
                        }
                    }],
                    'yAxes': [{
                        'display': True,
                        'ticks': {
                            'beginAtZero': True,
                        },
                        'gridLines': {
                            'color': '#525252',
                        }
                    }]
                },
            }
        }
    }


def getFakeCumulFlow(tile_id, template_name):
    return {
        'id': tile_id, 'tile_template': template_name, 'modified': getIsoTime(),
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
                'elements': {
                    'line': {
                        'tension': 0
                    }
                },
                'scales': {
                    'xAxes': [{
                        'gridLines': {
                            'color': '#525252',
                        }
                    }],
                    'yAxes': [{
                        'gridLines': {
                            'color': '#525252',
                        }
                    }]
                }
            }
        }
    }


def getFakeNormChart(tile_id, template_name):
    return {
        'id': tile_id, 'tile_template': template_name, 'modified': getIsoTime(),
        'data': {
            'title': {'display': True, 'text': 'Curve Comparaison'},
            'labels': [1, 3, 5, 7, 9, 11],
            'datasets': [
                buildDatasetNorm(index=0, randomData=True, labelLenght=6),
                buildDatasetNorm(index=1, randomData=True, labelLenght=6)
            ]
        },
        'meta': {
            'backgroundColor': COLOR_TAB,
            'options': {
                'responsive': True,
                'maintainAspectRatio': False,
                'scales': {
                    'xAxes': [{'gridLines': {'color': '#525252'}}],
                    'yAxes': [{'gridLines': {'color': '#525252'}}]
                }
            }
        }
    }


def getFakeBarChart(tile_id, template_name):
    return {
        'id': tile_id, 'tile_template': template_name, 'modified': getIsoTime(),
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
                'responsive': True,
                'maintainAspectRatio': False,
                'legend': {'display': False},
                'scales': {
                    'xAxes': [{'gridLines': {'color': '#696969', 'display': False}}],
                    'yAxes': [{'gridLines': {'color': '#696969'}}]
                }
            }
        }
    }



def getFakeVbarChart(tile_id, template_name):
    return getFakeBarChart(tile_id, template_name)


def getFakePieChart(tile_id, template_name):
    return {
        'id': tile_id, 'tile_template': template_name, 'modified': getIsoTime(),
        'data': {
            'title': {'display': True, 'text': 'PieChart Demo'},
            'labels': [f'Label {i + 1}' for i in range(5)],
            'borderColor': '#525252',
            'datasets': [
                buildDatasetPie(randomData=True, labelLenght=5)
            ]
        },
        'meta': {
            'labels': {'fontColor': 'rgba(255, 255, 255, 0.80)'},
            'tooltips': {'enabled': False},
            'backgroundColor': COLOR_TAB,
            'elements': {'arc': {}},
            'responsive': True,
            'maintainAspectRatio': False,
        }
    }


def getFakeDoughnutChart(tile_id, template_name):
    return {
        'id': tile_id, 'tile_template': template_name, 'modified': getIsoTime(),
        'data': {
            'title': {'display': True, 'text': 'Doughnut Demo'},
            'labels': [f'Label {i + 1}' for i in range(8)],
            'datasets': [
                buildDatasetDoughnut(randomData=False, labelLenght=8)
            ]
        },
        'meta': {
            'options': {
                'responsive': True,
                'maintainAspectRatio': False,
                'elements': {'arc': {'borderWidth': 1.0, 'borderColor': '#696969'}}
            }
        }
    }


def getFakeHalfDoughnutChart(tile_id, template_name):
    return getFakeDoughnutChart(tile_id, template_name)


def getFakeRadarChart(tile_id, template_name):
    return {
        'id': tile_id, 'tile_template': template_name, 'modified': getIsoTime(),
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
                    'gridLines': {
                        'color': ['#525252' for _ in range(8)]
                    },
                    'angleLines': {'color': '#696969'},
                    'ticks': {'display': False}
                },
                'responsive': True,
                'maintainAspectRatio': False,
            }
        }
    }


def getFakePolarareaChart(tile_id, template_name):
    return {
        'id': tile_id, 'tile_template': template_name, 'modified': getIsoTime(),
        'data': {
            'title': {'display': True, 'text': 'Polar area Demo'},
            'labels': [f'Serie {i + 1}' for i in range(3)],
            'datasets': [
                buildDatasetPolararea(randomData=True, labelLenght=4)
            ]
        },
        'meta': {
            'options': {
                'responsive': True,
                'maintainAspectRatio': False,
                'elements': {'arc': {'borderColor': '#696969', 'borderWidth': 2}},
                'scale': {
                    'gridLines': {
                        'color': ['#525252' for _ in range(8)]
                    },
                    'angleLines': {'color': '#696969'},
                    'ticks': {'display': False}
                }
            }
        }
    }
