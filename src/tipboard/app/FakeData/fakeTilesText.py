from src.tipboard.app.applicationconfig import getIsoTime


def getFakeSimplePercentg(tile_id, template_name):
    return {
        'data': {
            'title': 'Title',
            'big_value': '24',
            'subtitle': 'Subtitle',
            'right_value': 'right_value',
            'right_label': 'right_label',
            'left_label': 'left_label',
            'left_value': 'left_value'
        },
        'meta': dict(big_value_color='#4CAF50', fading_background=True),
        'tile_template': template_name,
        'modified': getIsoTime(),
        'id': tile_id
    }


def getFakeListing(tile_id, template_name):
    return {
        'data': {
            'items': [
                'Leader: 42',
                'Product Owner: 1',
                'Scrum Master: 1',
                'Developer: 1',
                'U.X: 1'
            ]
        },
        'meta': dict(big_value_color='#4CAF50', fading_background=False),
        'tile_template': template_name,
        'modified': getIsoTime(),
        'id': tile_id
    }


def getFakeText(tile_id, template_name):
    return {
        'data': dict(text='Text auto generated'),
        'meta': dict(big_value_color='#4CAF50', fading_background=False),
        'tile_template': template_name,
        'modified': getIsoTime(),
        'id': tile_id
    }


def getFakeFancyListing(tile_id, template_name):
    return {
        'data': dict(title='title', description='description'),
        'meta': dict(big_value_color='#4CAF50', fading_background=False),
        'tile_template': template_name,
        'modified': getIsoTime(),
        'id': tile_id
    }


def getFakeBigValue(tile_id, template_name):
    return {
        'data': {
            'title': 'Title',
            'description': 'Description',
            'big-value': '25%',
            'lower-left-label': 'lower left-label',
            'upper-left-label': 'upper left-label',
            'upper-right-label': 'upper right-label',
            'lower-right-label': 'lower right-label'
        },
        'meta': dict(big_value_color='#4CAF50', fading_background=True),
        'tile_template': template_name,
        'modified': getIsoTime(),
        'id': tile_id
    }


def getFakeJustValue(tile_id, template_name):
    return {
        'data': {
            'title': 'Title',
            'description': 'Description',
            'just-value': '51'
        },
        'meta': dict(big_value_color='#d50000', fading_background=True),
        'tile_template': template_name,
        'modified': getIsoTime(),
        'id': tile_id
    }
