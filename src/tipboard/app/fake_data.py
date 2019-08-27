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
              'backgroundColor': ["#3e95cd", "#8e5ea2", "#3cba9f"],
              'options': {
                  'title': {
                      'displayTitle': True,
                      'text': "Mon Titre"
                  }
              }
          },
          "modified": getIsoTime()
        }


def getFakeLineChart(tile_id, template_name):
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


def getFakeCumulFlow(tile_id, template_name):
    pass


def getFakeSimplePercentg(tile_id, template_name):
    pass


def getFakeListing(tile_id, template_name):
    pass


def getFakeBarChart(tile_id, template_name):
    pass


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
    pass


def buildFakeDataFromTemplate(tile_id, template_name, cache):
    print(f"Building fake data for {tile_id} as template: {template_name}")
    data = dict()
    if template_name == "text":
       data = getFakeText(tile_id, template_name)
    elif template_name == "pie_chart" or template_name == "pie_chartjs":
       data = getFakePieChart(tile_id, template_name)
    elif template_name == "line_chart" or template_name == "line_chartjs":
        data = getFakeLineChart(tile_id, template_name)
    elif template_name == "cumulative_flow":
        data = getFakeCumulFlow(tile_id, template_name)
    elif template_name == "simple_percentage":
        data = getFakeSimplePercentg(tile_id, template_name)
    elif template_name == "listing":
        data = getFakeListing(tile_id, template_name)
    elif template_name == "bar_chart":
        data = getFakeBarChart(tile_id, template_name)
    elif template_name == "norm_chart":
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
    else:# TODO: need to be handle for all type of tiles
        data = {
            "tile_template": template_name,
            "modified": "2019-08-01T15:17:01+02:00",
            "id": tile_id,
            "meta": {
                "big_value_color": "#4CAF50",
                "fading_background": False
            },
            "data": {
                "title": "My title",
                "text":"text"
            }
        }
    cache.redis.set(name=getRedisPrefix(tile_id), value=json.dumps(data))
    return data