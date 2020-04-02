import json
import os
# General Configuration
PATH_FOR_PIP = 'src.'  # Location of Tipboard sources
CONFIG_DIR = os.path.dirname(os.path.realpath(__file__)) + '/Config/'  # Path of Config directory
PROPERTIES = json.load(open(CONFIG_DIR + 'properties.json'))
DEFAULT_CONFIG = os.path.join(CONFIG_DIR, 'default_config.yaml')  # Default layout config
API_KEY = PROPERTIES['TIPBOARD_TOKEN']
SUPER_SECRET_KEY = PROPERTIES['SUPER_SECRET_KEY']
DEBUG = PROPERTIES['DEBUG']
LOG = PROPERTIES['LOG']
VERSION = PROPERTIES['VERSION']
TIPBOARD_URL = PROPERTIES['TIPBOARD_URL']
CDN_URL = PROPERTIES['CDN_URL']  # if you are in production and need a CDN for media and static file
REDIS_HOST = PROPERTIES['REDIS_HOST']
REDIS_PORT = PROPERTIES['REDIS_PORT']
REDIS_PASSWORD = PROPERTIES['REDIS_PASSWORD']
if 'REDIS_DB' in PROPERTIES:
    REDIS_DB = PROPERTIES['REDIS_DB']
else:
    REDIS_DB = 0
# Tipboard Properties
DEFAULT_LAYOUT = 'default_config.yaml'
FLIPBOARD_INTERVAL = PROPERTIES['FLIPBOARD_INTERVAL'] if 'FLIPBOARD_INTERVAL' in PROPERTIES else 10
if 'default_config' in PROPERTIES:
    DEFAULT_CONFIG = os.path.join(CONFIG_DIR, PROPERTIES['default_config'])
else:
    DEFAULT_CONFIG = os.path.join(CONFIG_DIR, DEFAULT_LAYOUT)
TIPBOARD_CSS_STYLES = ['css/layout.css']
TIPBOARD_JAVASCRIPT_FILES = ['js/websocket.js', 'js/tipboard.js', 'tiles/chartjs.js', 'tiles/text_value.js']
ALLOWED_TILES = ['text', 'simple_percentage', 'listing', 'big_value', 'just_value',  # Homemade
                 'norm_chart', 'line_chart', 'cumulative_flow',  # ChartJS
                 'bar_chart', 'vbar_chart', 'gauge_chart', 'radial_gauge_chart', 'linear_gauge_chart',  # ChartJS
                 'vlinear_gauge_chart', 'doughnut_chart', 'half_doughnut_chart',  # ChartJS
                 'pie_chart', 'polararea_chart', 'radar_chart',  # ChartJS
                 'iframe', 'stream', 'custom']  # misc
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
BACKGROUND_TAB = ['#4caf50', '#ff6d00', '#d50000']

if 'COLOR_TAB' in PROPERTIES:  # TODO: documentation if properties present in json override default color
    rcx = 0
    for color in PROPERTIES['COLOR_TAB']:
        COLOR_TAB[rcx] = PROPERTIES['COLOR_TAB'][rcx]

if LOG:
    print(f"Tipboard start in DEBUG MODE:{DEBUG} & LOG:{LOG}")
