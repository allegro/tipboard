#!/usr/bin/env python
import json

import requests

PUSH_URL = "http://localhost:7272/api/2/xxx/push"

tiles_data = []

tiles_data.append({
    'tile-id': 'chart-tile1',
    'tile-data': {
        "header": "Line chart!!",
        "chartType": "Line",
        "chartData": {
            "labels": [
                "January", "February", "March", "April", "May", "June", "July"
            ],
            "datasets": [{
                "label": "My First dataset",
                "fillColor": "rgba(220,220,220,0.2)",
                "strokeColor": "rgba(220,220,220,1)",
                "pointColor": "rgba(220,220,220,1)",
                "pointStrokeColor": "#fff",
                "pointHighlightFill": "#fff",
                "pointHighlightStroke": "rgba(220,220,220,1)",
                "data": [65, 59, 80, 81, 56, 55, 40]
            }, {
                "label": "My Second dataset",
                "fillColor": "rgba(151,187,205,0.2)",
                "strokeColor": "rgba(151,187,205,1)",
                "pointColor": "rgba(151,187,205,1)",
                "pointStrokeColor": "#fff",
                "pointHighlightFill": "#fff",
                "pointHighlightStroke": "rgba(151,187,205,1)",
                "data": [28, 48, 40, 19, 86, 27, 90]
            }]
        }
    }
})

tiles_data.append({
    'tile-id': 'chart-tile2',
    'tile-data': {
        "header": "Bar chart!!",
        "chartType": "Bar",
        "chartData": {
            "labels": ["January", "February", "March", "April", "May", "June", "July"],
            "datasets": [{
                "label": "My First dataset",
                "fillColor": "rgba(220,220,220,0.5)",
                "strokeColor": "rgba(220,220,220,0.8)",
                "highlightFill": "rgba(220,220,220,0.75)",
                "highlightStroke": "rgba(220,220,220,1)",
                "data": [65, 59, 80, 81, 56, 55, 40]
            }, {
                "label": "My Second dataset",
                "fillColor": "rgba(151,187,205,0.5)",
                "strokeColor": "rgba(151,187,205,0.8)",
                "highlightFill": "rgba(151,187,205,0.75)",
                "highlightStroke": "rgba(151,187,205,1)",
                "data": [28, 48, 40, 19, 86, 27, 90]
            }]
        }
    }
})

tiles_data.append({
    'tile-id': 'chart-tile3',
    'tile-data': {
        "header": "Pie chart!!",
        "chartType": "Pie",
        "chartData": [{
            "value": 300,
            "color":"#F7464A",
            "highlight": "#FF5A5E",
            "label": "Red"
        }, {
            "value": 50,
            "color": "#46BFBD",
            "highlight": "#5AD3D1",
            "label": "Green"
        }, {
            "value": 100,
            "color": "#FDB45C",
            "highlight": "#FFC870",
            "label": "Yellow"
        }]
    }
})

tiles_data.append({
    "tile-id": "chart-tile4",
    "tile-data": {
        "header": "Radar tile!!",
        "chartType": "Radar",
        'chartData': {
            "labels": [
                "Eating", "Drinking", "Sleeping", "Designing", "Coding",
                "Cycling", "Running"
            ],
            "datasets": [{
                "label": "My First dataset",
                "fillColor": "rgba(220,220,220,0.2)",
                "strokeColor": "rgba(220,220,220,1)",
                "pointColor": "rgba(220,220,220,1)",
                "pointStrokeColor": "#fff",
                "pointHighlightFill": "#fff",
                "pointHighlightStroke": "rgba(220,220,220,1)",
                "data": [65, 59, 90, 81, 56, 55, 40],
            }, {
                "label": "My Second dataset",
                "fillColor": "rgba(151,187,205,0.2)",
                "strokeColor": "rgba(151,187,205,1)",
                "pointColor": "rgba(151,187,205,1)",
                "pointStrokeColor": "#fff",
                "pointHighlightFill": "#fff",
                "pointHighlightStroke": "rgba(151,187,205,1)",
                "data": [28, 48, 40, 19, 96, 27, 100],
            }],
        },
    },
})

tiles_data.append({
    "tile-id": "tile-image1",
    "tile-data": {
        "header": "Retarded cat",
        "imageSrc": "http://media.giphy.com/media/m7LAdkIlt2G9a/giphy.gif",
    },
})
tiles_data.append({
    'tile-id': 'rotated1',
    'tile-data': {
        "header": "awesome image 1",
        "imageSrc": "http://media.giphy.com/media/nduJE1Q4pZela/giphy.gif"
    }
})
tiles_data.append({
    'tile-id': 'rotated2',
    'tile-data': {
        "header": "awesome image 2",
        "imageSrc": "http://media.giphy.com/media/JKa34ak34FCEw/giphy.gif"
    }
})

for data in tiles_data:
    jsoned_data = json.dumps(data)
    response = requests.post(PUSH_URL, jsoned_data)
    print(data['tile-id'], response.status_code, response.content)
