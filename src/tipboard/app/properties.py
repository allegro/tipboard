import json, os

dir_path = os.path.dirname(os.path.realpath(__file__))

# Location of Tipboard sources
TIPBOARD_PATH = os.path.dirname(__file__)

FROM_PIP = 'src.'

# Path of Config directory
user_config_dir = dir_path + '/Config/'

# Determine which layout config should be used by default
LAYOUT_CONFIG = os.path.join(user_config_dir, 'tmp/layout_config.yaml')

conf = json.load(open(dir_path + '/Config/properties.json'))

API_VERSION = conf['API_VERSION']
API_KEY = conf['TIPBOARD_TOKEN']
PROJECT_NAME = conf['PROJECT_NAME']
SUPER_SECRET_KEY = conf['SUPER_SECRET_KEY']

DEBUG = conf['DEBUG']
LOG = conf['LOG']
VERSION = conf['VERSION']
SITE_ENV = conf['SITE_ENV']
LOCAL = conf['LOCAL']
TIPBOARD_URL = conf['TIPBOARD_URL']
CDN_URL = conf['CDN_URL']  # if you are in production and need a CDN for media and static file
REDIS_HOST = conf['REDIS_HOST']
REDIS_PORT = conf['REDIS_PORT']
REDIS_PASSWORD = conf['REDIS_PASSWORD']
REDIS_DB = conf['REDIS_DB']

ALLOWED_TILES = ['text', 'simple_percentage', 'listing', 'big_value', 'just_value',  # Homemade
                 'norm_chart', 'line_chart', 'cumulative_flow', 'bar_chart', 'vbar_chart',  # ChartJS
                 'half_doughnut_chart', 'doughnut_chart', 'pie_chart', 'radar_chart', 'polararea_chart',  # ChartJS
                 'empty', 'iframe']  # misc

COLOR_TAB = [  # material color
    'rgba(66, 165, 245, 0.8)',      # blue #42a5f5
    'rgba(114, 191, 68, 0.8)',      # green #72bf44
    'rgba(0, 150, 136, 0.8)',       # teal #009688
    'rgba(255, 234, 0, 0.8)',       # yellow #ffea00
    'rgba(255, 152, 0, 0.8)',       # orange #ff9800
    'rgba(213, 0, 0, 0.8)',         # red #d50000
    'rgb(240, 98, 146)',            # pink #f06292
    'rgba(224, 224, 224, 0.8)',     # Grey #e0e0e0
    'rgb(177, 208, 225)',           # Light Blue #b1d0e1
    'rgba(121, 85, 72, 0.8)',       # Marron #795548
    'rgba(149, 117, 205, 0.8)',     # purple #9575cd
    'rgb(224, 64, 251)',            # Light Purple #e040fb
    'rgb(48, 79, 254)',             # Indigo #304ffe
    'rgb(33, 33, 33)'               # Black #212121
]

if 'COLOR_TAB' in conf:
    rcx = 0
    for color in conf['COLOR_TAB']:
        COLOR_TAB[rcx] = conf['COLOR_TAB'][rcx]

BACKGROUND_TAB = ['#4caf50', '#ff6d00', '#d50000']

TIPBOARD_CSS_STYLES = ['css/layout.css']
TIPBOARD_JAVASCRIPTS = ['js/websocket.js', 'js/tipboard.js',
                        'tiles/chartjs.js', 'tiles/text_value.js']

# how many seconds dashboard is displayed before is flipped, if 0 than NO FLIPBOARD
FLIPBOARD_INTERVAL = 10

if LOG:
    print(f"Tipboard start in DEBUG MODE:{DEBUG} & LOG:{LOG}")
