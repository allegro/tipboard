
def getDefaultBigValue():
    return {
        'data': {
            'title': 'Title',
            'big-value': '25%',
            'lower-left-label': 'lower left-label',
            'upper-left-label': 'upper left-label',
            'upper-right-label': 'upper right-label',
            'lower-right-label': 'lower right-label'
        },
        'meta': dict(big_value_color='#4CAF50', fading_background=True),
    }


def getDefaultSimplePercentg():
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
        'meta': dict(big_value_color='#4CAF50', fading_background=False),
    }


def getDefaultJustValue():
    return {
        'data': {
            'title': 'Title',
            'description': 'Description',
            'just-value': '51'
        },
        'meta': dict(big_value_color='#d50000', fading_background=True),
    }


def getDefaultText():
    return {
        'data': dict(text='Text auto generated')
    }


def getDefaultListing():
    return {
        'data': {
            'items': [
                'Leader: 42',
                'Product Owner: 1',
                'Scrum Master: 1',
                'Developer: 1',
                'U.X: 1'
            ]
        }
    }


def getDefaultCustomTile():
    return {
        'data': dict(text='Text auto generated For custom tile')
    }
