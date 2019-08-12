# -*- coding: utf-8 -*-
from src.tipboard.app.utils import getTimeStr
from src.tipboard.app.properties import *
from src.tipboard.app.parser import get_config_files_names, process_layout_config

class Flipboard(object):

    def __init__(self):
        self.last_found_configs_number = -1
        self.paths = []

    def get_paths(self):
        """
        Returns url paths to dashboards (created from .yaml config from
        userspace).
        """
        config_names = self._get_config_names()
        if len(config_names) != self.last_found_configs_number:
            self.paths = self._config_names2paths(config_names)
            self.last_found_configs_number = len(config_names)
        return self.paths

    def get_flipboard_title(self):
        """
        Returns title to display as a html title.
        """
        title = ''
        config_names = self._get_config_names()
        if len(config_names) == 1:
            config = process_layout_config(config_names[0])
            try:
                title = config['details']['page_title']
            except KeyError:
                msg = 'config {} has no key: details/page_title'.format(
                    config_names[0]
                )
                if LOG:
                    print(f"{getTimeStr()} (+) {msg}", flush=True)
        elif len(config_names) > 1:
            # TODO: put here more suitable title?
            title = 'Flipboard Mode'
        return title

    def _get_config_names(self):
        config_names = FLIPBOARD_SEQUENCE
#        print("settings.FLIPBOARD_SEQUENCE: " + str(FLIPBOARD_SEQUENCE))
        if not any(config_names):
            config_names = get_config_files_names()
            if not any(config_names):

                raise Exception('No config (.yaml) file found in ./tipboard/app/Config/layout_config.yaml')
        return config_names

    def _config_names2paths(self, config_names):
        paths = []
        for name in config_names:
            path = '/' + name
            paths.append(path)
        return paths