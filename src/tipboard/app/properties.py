import json, os

dir_path = os.path.dirname(os.path.realpath(__file__))
conf = json.load(open(dir_path + '/Config/properties.json'))

FORMAT_SIMPLE_DATE = '%Y-%m-%d'
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
    'css/layout.css',
]
TIPBOARD_JAVASCRIPTS = [
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

