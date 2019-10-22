import json, os

dir_path = os.path.dirname(os.path.realpath(__file__))

# Location of Tipboard sources
TIPBOARD_PATH = os.path.dirname(__file__)

FROM_PIP = 'src.'

# Path of Config directory
user_config_dir = dir_path + '/Config/'

# Determine which layout config should be used by default
LAYOUT_CONFIG = os.path.join(user_config_dir, 'layout_config.yaml')

conf = json.load(open(dir_path + '/Config/properties.json'))

API_VERSION = conf['API_VERSION']
API_KEY = conf['TIPBOARD_TOKEN']
PROJECT_NAME = conf['PROJECT_NAME']
SUPER_SECRET_KEY = conf["SUPER_SECRET_KEY"]
DEBUG = conf['DEBUG']
LOG = conf['LOG']
VERSION = conf["VERSION"]
SITE_ENV = conf["SITE_ENV"]
LOCAL = conf['LOCAL']
TIPBOARD_URL = conf['TIPBOARD_URL']
CDN_URL = conf['CDN_URL']  # if you are in production and need a CDN for media and static file

REDIS_HOST = conf['REDIS_HOST']
REDIS_PORT = conf['REDIS_PORT']
REDIS_PASSWORD = conf['REDIS_PASSWORD']
REDIS_DB = conf['REDIS_DB']

ALLOWED_TILES = ["text", "fancy_listing", "simple_percentage", "listing", "big_value", "just_value",  # Homemade
                 "norm_chart", "line_chart", "cumulative_flow", "bar_chart", "vbar_chart",  # ChartJS
                 "doughnut_chart", "pie_chart", "radar_chart", "polararea_chart",  # ChartJS
                 "empty"]  # chartjs lib


TIPBOARD_CSS_STYLES = [
    'css/layout.css',
]
TIPBOARD_JAVASCRIPTS = [
    'js/dashboard.js', 'js/tipboard.js'
]

# Javascript log level ('1' for 'standard', '2' for 'debug')
JS_LOG_LEVEL = 2

# how many seconds dashboard is displayed before is flipped
FLIPBOARD_INTERVAL = 0
# file name(s) of EXISTING layouts without extension, eg. ['layout_config']
FLIPBOARD_SEQUENCE = []

# Our default color palette
COLORS = {
    'black': '#000000',
    'white': '#FFFFFF',
    'tile_background': '#15282d',
    'red': '#d50000',
    'yellow': '#ffea00',
    'green': '#00c853',
    'blue': '#0091ea',
    'violet': '#aa00ff',
    'orange': '#ff6d00',
    'naval': '#00bfa5',
}
