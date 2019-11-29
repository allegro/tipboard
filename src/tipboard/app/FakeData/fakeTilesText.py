from src.tipboard.app.applicationconfig import getIsoTime


def getFakeSimplePercentg(tile_id, template_name):
    return {
        'tile_template': template_name,
        'meta': {
            'big_value_color': '#4CAF50',
            'fading_background': True
        },
        'data': {
            'title': 'Title',
            'big_value': '24',
            'subtitle': 'Subtitle',
            'right_value': 'right_value',
            'right_label': 'right_label',
            'left_label': 'left_label',
            'left_value': 'left_value'
        },
        'modified': getIsoTime(),
        'id': tile_id
    }


def getFakeListing(tile_id, template_name):
    return {
        'tile_template': template_name,
        'meta': {
            'fading_background': False
        },
        'data': {
            'items': [
                'Leader: 42',
                'Product Owner: 1',
                'Scrum Master: 1',
                'Developer: 1',
                'U.X: 1'
            ]
        },
        'modified': getIsoTime(),
        'id': tile_id
    }


def getFakeText(tile_id, template_name):
    return {
        'tile_template': template_name,
        'meta': {
            'fading_background': False
        },
        'data': {
            'text': 'Text from sensors'
        },
        'modified': getIsoTime(),
        'id': tile_id
    }


def getFakeFancyListing(tile_id, template_name):
    return {
        'tile_template': template_name,
        'meta': {
            'big_value_color': '#4CAF50',
            'fading_background': False
        },
        'data': {
            'title': 'title',
            'description': 'description',
        },
        'modified': getIsoTime(),
        'id': tile_id
    }


def getFakeBigValue(tile_id, template_name):
    return {
        'tile_template': template_name,
        'meta': {
            'big_value_color': '#4CAF50',
            'fading_background': True
        },
        'data': {
            'title': 'Title',
            'description': 'Description',
            "big-value": "25%",
            "lower-left-label": "lower left-label",
            "upper-left-label": "upper left-label",
            "upper-right-label": "upper right-label",
            "lower-right-label": "lower right-label"
        },
        'modified': getIsoTime(),
        'id': tile_id
    }


def getFakeJustValue(tile_id, template_name):
    return {
        'tile_template': template_name,
        'meta': {
            'big_value_color': '#d50000',
            'fading_background': True
        },
        'data': {
            'title': 'Title',
            'description': 'Description',
            'just-value': '51'
        },
        'modified': getIsoTime(),
        'id': tile_id
    }
