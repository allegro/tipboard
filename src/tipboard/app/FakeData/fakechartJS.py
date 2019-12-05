from src.tipboard.app.applicationconfig import getIsoTime
from src.tipboard.app.utils import buildBasicDataset
from src.tipboard.app.properties import COLOR_TAB


def getFakeLineChart(tile_id, template_name):
    return {
        'id': tile_id, 'tile_template': template_name, 'modified': getIsoTime(),
        'data': {
            'title': {'text': 'LineChart Demo', 'color': '#FFFFFF'},
            'labels': ['00h', '01h', '02h', '03h', '04h', '05h', '06h', '07h', '08h', '09h', '10h', '11h', '12h', '13h',
                       '14h', '15h', '16h', '17h', '18h', '19h', '20h', '21h', '22h', '23h', '24h'],
            'datasets': [
                buildBasicDataset(data=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
                                        14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24], seriesNumber=1),
                buildBasicDataset(data=[5, 6, 4, 1, 3, 9, 10, 11, 12, 19, 30, 31, 32,
                                        34, 33, 32, 31, 20, 19, 18, 17, 16, 15, 14], seriesNumber=2)]
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
                            'max': 40
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
                buildBasicDataset(data=[0, 2, 0.5, 1, 1, 1, 2, 2, 1, 1], seriesNumber=1),
                buildBasicDataset(data=[0, 4, 0, 0, 1, 0, 0, 3, 0, 0], seriesNumber=2)]
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


def getFakeBarChart(tile_id, template_name):
    return {
        'id': tile_id, 'tile_template': template_name, 'modified': getIsoTime(),
        'data': {
            'title': {'display': True, 'text': 'Bar Chart Demo'},
            'labels': ['Last (n)', 'n-1', 'n-2'],
            'datasets': [
                buildBasicDataset(data=[49, 50, 35], seriesNumber=1),
                buildBasicDataset(data=[13, 45, 9], seriesNumber=2)]
        },
        'meta': {
            'options': {
                # 'responsive': True,
                # 'maintainAspectRatio': False,
                'legend': {'display': False},
                'scales': {
                    'xAxes': [{'gridLines': {'color': '#525252'}}],
                    'yAxes': [{'gridLines': {'color': '#525252'}, 'ticks': {'beginAtZero': True}}]
                }
            }
        }
    }


def getFakeVbarChart(tile_id, template_name):
    return getFakeBarChart(tile_id, template_name)


def getFakeNormChart(tile_id, template_name):
    return {
        'id': tile_id, 'tile_template': template_name, 'modified': getIsoTime(),
        'data': {
            'title': {'display': True, 'text': 'Curve Comparaison'},
            'labels': [1, 3, 5, 7, 9, 11],
            'datasets': [{
                'data': [2, 20, 13, 33, 85, 100],
                'label': 'Series 2',
                'borderColor': '#3e95cd',
                'fill': False
            }, {
                'data': [2, 8, 10, 15, 80, 120],
                'label': 'Series 1',
                'borderColor': '#8e5ea2',
                'fill': False
            }]
        },
        'meta': {
            'backgroundColor': ['#3e95cd', '#8e5ea2'],
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


def getFakePieChart(tile_id, template_name):
    return {
        'id': tile_id, 'tile_template': template_name, 'modified': getIsoTime(),
        'data': {
            'title': tile_id,
            'labels': ['Label 1', 'Label 2', 'label 3'],
            'pie_data_value': [55, 12, 33],
            'borderColor': 'rgba(255, 255, 255, 0.72)',
            'borderWidth': 1.0
        },
        'meta': {
            'backgroundColor': ['#303F9F', '#8BC34A', '#0288D1', '#E040FB', '#FF5722'],
            'elements': {'arc': {}}
        }
    }


def getFakeDoughnutChart(tile_id, template_name):
    return {
        'id': tile_id, 'tile_template': template_name, 'modified': getIsoTime(),
        'data': {
            'title': {'display': True, 'text': 'Doughnut Demo'},
            'labels': ['Label 1', 'Label 2', 'Label 3'],
            'datasets': [
                {
                    'backgroundColor': ['#3e95cd', '#72bf44', '#8e5ea2'],
                    'data': [2478, 5267, 734],
                }
            ]
        },
        'meta': {
            'options': {
                'responsive': True,
                'maintainAspectRatio': False,
                'elements': {'arc': {'borderWidth': 1.0, 'borderColor': 'rgba(255, 255, 255, 0.82)'}}
            }
        }
    }


def getFakeRadarChart(tile_id, template_name):
    return {
        'id': tile_id, 'tile_template': template_name, 'modified': getIsoTime(),
        'data': {
            'title': {'text': 'Radar Demo', 'borderColor': 'rgba(255, 255, 255, 1)'},
            'labels': ['Label 1', 'Label 2', 'Label 3', 'Label 4', 'Label 5'],
            'datasets': [
                {
                    'label': 'Series 1',
                    'fill': True,
                    'backgroundColor': COLOR_TAB[1],
                    'borderColor': COLOR_TAB[1],
                    'pointBorderColor': 'rgba(114, 191, 68, 0.95)',
                    'pointBackgroundColor': 'rgba(255, 255, 255, 0.5)',
                    'data': [8.77, 55.61, 21.69, 6.62, 6.82]
                }, {
                    'label': 'Series 2',
                    'fill': True,
                    'backgroundColor': COLOR_TAB[0],
                    'borderColor': COLOR_TAB[0],
                    'pointBorderColor': 'rgba(62, 149, 205, 0.95)',
                    'pointBackgroundColor': 'rgba(255, 255, 255, 0.5)',
                    'data': [18, 10, 36, 36, 40]
                }
            ]
        },
        'meta': {
            'options': {
                'scale': {
                    'gridLines': {
                        'color': ['#525252', '#525252', '#525252', '#525252', '#525252', '#525252', '#525252']
                    },
                    'angleLines': {'color': '#525252'},
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
            'labels': ['Series 1', 'Series 2', 'Series 3'],
            'datasets': [
                {
                    'label': 'Series',
                    'backgroundColor': ['#3e95cd', '#8e5ea2', '#3cba9f', '#e8c3b9', '#c45850'],
                    'data': [10, 29, 40],
                }
            ]
        },
        'meta': {
            'options': {
                'responsive': True,
                'maintainAspectRatio': False,
                'elements': {'arc': {'borderColor': '#525252', 'borderWidth': 2}},
                'scale': {
                    'gridLines': {
                        'color': ['#525252', '#525252', '#525252', '#525252', '#525252', '#525252', '#525252']
                    },
                    'angleLines': {'color': '#525252'},
                    'ticks': {'display': False}
                }
            }
        }
    }
