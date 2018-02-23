#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

##############################################################################
# Stuff that can be / should be overridden in local settings

# Redis server configuration
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_DB = 4

DEBUG = False
API_KEY = 'default api key'
HOST = 'localhost'
PORT = 7272
PROJECT_NAME = 'example'

# Javascript log level ('1' for 'standard', '2' for 'debug')
JS_LOG_LEVEL = 1

# Our default color palette
COLORS = {
    'black':            '#000000',
    'white':            '#FFFFFF',
    'tile_background':  '#25282d',
    'red':              '#DC5945',
    'yellow':           '#FF9618',
    'green':            '#94C140',
    'blue':             '#12B0C5',
    'violet':           '#9C4274',
    'orange':           '#EC663C',
    'naval':            '#54C5C0',
}

# how many seconds dashboard is displayed before is flipped
FLIPBOARD_INTERVAL = 0
# file name(s) of EXISTING layouts without extension, eg. ['layout_config']
FLIPBOARD_SEQUENCE = []

# We are using Sentry for catching/aggregating errors
SENTRY_DSN = ''

##############################################################################
# Settings below should not be changed directly by user

# Load local settings (~/.tipboard/local_settings.py)
try:
    execfile(
        os.path.join(os.path.expanduser("~"), '.tipboard/settings-local.py')
    )
except IOError:
    pass

# Redis config that should be processed after local settings
REDIS = dict(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=REDIS_DB,
)
REDIS_ASYNC = dict(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    selected_db=REDIS_DB,
)
REDIS_SYNC = dict(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=REDIS_DB,
)

# Location of Tipboard sources
TIPBOARD_PATH = os.path.dirname(__file__)

# Tiles' paths which should be examined in given order (i.e. user's --> app's)
TILES_PATHS = [
    os.path.join(os.path.expanduser("~"), '.tipboard/custom_tiles'),
    os.path.join(TIPBOARD_PATH, 'tiles'),
]

# Determine which layout config should be used
_user_config_dir = os.path.join(os.path.expanduser("~"), '.tipboard')
_user_layout_config = os.path.join(_user_config_dir, 'layout_config.yaml')
_fallback_layout_config = os.path.join(
    TIPBOARD_PATH, 'defaults/layout_config.yaml'
)
if not os.path.exists(_user_layout_config):
    LAYOUT_CONFIG = _fallback_layout_config
else:
    LAYOUT_CONFIG = _user_layout_config

# CSS/JS files required by Tipboard
# TODO: do we really need to put this stuff in settings..??
TIPBOARD_CSS_STYLES = [
    'css/reset.css',
    'css/jquery.jqplot.css',
    'css/layout.css',
]
TIPBOARD_JAVASCRIPTS = [
    'js/lib/jquery.js',
    'js/lib/simplify.js',
    'js/lib/jquery.fullscreen.js',
    'js/lib/jqplot/jquery.jqplot.js',
    'js/lib/jqplot/plugins/jqplot.trendline.js',
    'js/lib/jqplot/plugins/jqplot.canvasAxisTickRenderer.js',
    'js/lib/jqplot/plugins/jqplot.canvasTextRenderer.js',
    'js/lib/jqplot/plugins/jqplot.categoryAxisRenderer.js',
    'js/lib/jqplot/plugins/jqplot.barRenderer.js',
    'js/lib/jqplot/plugins/jqplot.pointLabels.js',
    'js/lib/jqplot/plugins/jqplot.highlighter.js',
    'js/lib/jqplot/plugins/jqplot.dateAxisRenderer.js',
    'js/lib/jqplot/plugins/jqplot.pieRenderer.js',
    # XXX: importing ..
    #'js/lib/jqplot/plugins/jqplot.BezierCurveRenderer.js',
    # .. spoils rendering. Try: first plot from:
    # http://www.jqplot.com/deploy/dist/examples/pieTest4.html
    'js/lib/jqplot/plugins/jqplot.blockRenderer.js',
    'js/lib/jqplot/plugins/jqplot.bubbleRenderer.js',
    'js/lib/jqplot/plugins/jqplot.canvasAxisLabelRenderer.js',
    'js/lib/jqplot/plugins/jqplot.canvasOverlay.js',
    'js/lib/jqplot/plugins/jqplot.ciParser.js',
    'js/lib/jqplot/plugins/jqplot.cursor.js',
    'js/lib/jqplot/plugins/jqplot.donutRenderer.js',
    'js/lib/jqplot/plugins/jqplot.dragable.js',
    'js/lib/jqplot/plugins/jqplot.enhancedLegendRenderer.js',
    'js/lib/jqplot/plugins/jqplot.funnelRenderer.js',
    'js/lib/jqplot/plugins/jqplot.json2.js',
    'js/lib/jqplot/plugins/jqplot.logAxisRenderer.js',
    'js/lib/jqplot/plugins/jqplot.mekkoAxisRenderer.js',
    'js/lib/jqplot/plugins/jqplot.mekkoRenderer.js',
    'js/lib/jqplot/plugins/jqplot.meterGaugeRenderer.js',
    'js/lib/jqplot/plugins/jqplot.mobile.js',
    'js/lib/jqplot/plugins/jqplot.ohlcRenderer.js',
    'js/lib/jqplot/plugins/jqplot.pyramidAxisRenderer.js',
    'js/lib/jqplot/plugins/jqplot.pyramidGridRenderer.js',
    'js/lib/jqplot/plugins/jqplot.pyramidRenderer.js',
    'js/tipboard.js',
]
