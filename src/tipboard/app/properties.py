import json, os

dir_path = os.path.dirname(os.path.realpath(__file__))
conf = json.load(open(dir_path + '/Config/properties.json'))

FORMAT_SIMPLE_DATE = '%Y-%m-%d'
API_VERSION = conf['API_VERSION']
API_KEY = conf['TIPBOARD_TOKEN']
PROJECT_NAME = conf['PROJECT_NAME']
SUPER_SECRET_KEY = conf["SUPER_SECRET_KEY"]
debug = conf['DEBUG']
LOG = conf['LOG']
VERSION = conf["VERSION"]
SITE_ENV = conf["SITE_ENV"]
LOCAL = conf['LOCAL']
CDN_URL = conf['CDN_URL'] #if you are in production and need a CDN for media and static file

REDIS_HOST = conf['REDIS_HOST']
REDIS_PORT = conf['REDIS_PORT']
REDIS_PASSWORD = conf['REDIS_PASSWORD']
REDIS_DB = conf['REDIS_DB']

# Location of Tipboard sources
TIPBOARD_PATH = os.path.dirname(__file__)

# Javascript log level ('1' for 'standard', '2' for 'debug')
JS_LOG_LEVEL = 2

# Our default color palette
COLORS = {
    'black':            '#000000',
    'white':            '#FFFFFF',
    'tile_background':  '#15282d',
    'red':              '#d50000',
    'yellow':           '#ffea00',
    'green':            '#00c853',
    'blue':             '#0091ea',
    'violet':           '#aa00ff',
    'orange':           '#ff6d00',
    'naval':            '#00bfa5',
}

# how many seconds dashboard is displayed before is flipped
FLIPBOARD_INTERVAL = 0
# file name(s) of EXISTING layouts without extension, eg. ['layout_config']
FLIPBOARD_SEQUENCE = []


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

FROM_PIP = 'src.'
#FROM_PIP = ''

#Tu dois faire la diff des path quand
# * dans pip
# * dans docker
# * dans bash

# Determine which layout config should be used
user_config_dir = dir_path + '/Config/'

LAYOUT_CONFIG = os.path.join(user_config_dir, 'layout_config.yaml')

