import json, os
from tipboard.utils import getTimeStr

dir_path = os.path.dirname(os.path.realpath(__file__))
conf = json.load(open(dir_path + '/Config/properties.json'))

FORMAT_SIMPLE_DATE = '%Y-%m-%d'
API_VERSION = conf['API_VERSION']
API_KEY = conf['TIPBOARD_TOKEN']
PROJECT_NAME = conf['PROJECT_NAME']
SUPER_SECRET_KEY = conf["SUPER_SECRET_KEY"]
debug = conf['DEBUG']
VERSION = conf["VERSION"]
SITE_ENV = conf["SITE_ENV"]
LOCAL = conf['LOCAL']
CDN_URL = conf['CDN_URL']

REDIS_HOST = conf['REDIS_HOST']
REDIS_PORT = conf['REDIS_PORT']
REDIS_PASSWORD = conf['REDIS_PASSWORD']
REDIS_DB = conf['REDIS_DB']

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

# We are using Sentry for catching/aggregating errors
SENTRY_DSN = ''

##############################################################################
# Settings below should not be changed directly by user

# Load local settings (.tipboard/local_settings.py)

try:
    exec (compile(open(os.path.join('tipboard/Config', 'settings-local.py'), "rb").read(),
                  os.path.join('tipboard/Config', 'settings-local.py'), "exec"))
except IOError:
    print(f"{getTimeStr()} (-) Error settings-local.py not found", flush=True)

# Determine which layout config should be used
user_config_dir = 'tipboard/Config'
_user_layout_config = os.path.join(user_config_dir, 'layout_config.yaml')
# Location of Tipboard sources
TIPBOARD_PATH = os.path.dirname(__file__)

# Tiles' paths which should be examined in given order (i.e. user's --> app's)
TILES_PATHS = [
    os.path.join('.tipboard', '.tipboard/custom_tiles'),
    os.path.join(TIPBOARD_PATH, 'tiles'),
]
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

_fallback_layout_config = os.path.join(
    TIPBOARD_PATH, 'defaults/Config/layout_config.yaml'
)
if not os.path.exists(_user_layout_config):
    LAYOUT_CONFIG = _fallback_layout_config
else:
    LAYOUT_CONFIG = _user_layout_config

