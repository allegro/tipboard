import os

# Redis serwer configuration
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 4

DEBUG = True
#API_KEY = 'default api key'
API_KEY = 'xxx'
HOST = 'localhost'
PORT = 7272
#PROJECT_NAME = 'example'
PROJECT_NAME = 'polymer'

# We are using Sentry for catching/aggregating errors
SENTRY_DSN = ''

#TODO:: handle this
## Load local settings (~/.tipboard/local_settings.py)
#try:
#    execfile(
#        os.path.join(os.path.expanduser("~"), '.tipboard/settings-local.py')
#    )
#except IOError:
#    pass

# Redis config that should be processed after local settings
REDIS = dict(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
)
REDIS_ASYNC = dict(
    host=REDIS_HOST,
    port=REDIS_PORT,
    selected_db=REDIS_DB,
)
REDIS_SYNC = dict(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
)

# Location of Tipboard sources
TIPBOARD_PATH = os.path.dirname(__file__)

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
