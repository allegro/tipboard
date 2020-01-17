from src.tipboard.app.utils import getTimeStr
from src.tipboard.app.properties import FLIPBOARD_SEQUENCE
from src.tipboard.app.parser import get_config_files_names, parse_xml_layout


def get_config_names():
    config_names = FLIPBOARD_SEQUENCE
    if not any(config_names):
        config_names = get_config_files_names()
        if not any(config_names):

            raise Exception('No config (.yaml) file found in ./tipboard/app/Config/layout_config.yaml')
    return config_names


def get_flipboard_title():
    """ Returns title to display as a html title. """
    title = ''
    config_names = get_config_names()
    try:
        if len(config_names) == 1:
            config = parse_xml_layout(config_names[0])
            title = config['details']['page_title']
        else:
            # TODO: put here more suitable title?
            title = 'Flipboard Mode'
    except KeyError:
        print(f"{getTimeStr()} (+) config {config_names[0]} has no key: details/page_title'", flush=True)
    return title


class Flipboard(object):

    def __init__(self):
        self.last_found_configs_number = -1
        self.paths = list()

    def get_paths(self):
        """ Returns url paths to dashboards (created from .yaml config from userspace). """
        config_names = get_config_names()
        if len(config_names) != self.last_found_configs_number:
            self.paths = list()
            for name in config_names:
                self.paths.append('/' + name)
            self.last_found_configs_number = len(config_names)
        return self.paths
