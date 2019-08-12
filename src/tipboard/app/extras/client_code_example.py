# -*- coding: utf-8 -*-

# This is an example 'client_code' script which demonstrates how to 'glue'
# together a tile (or collection of tiles) with an external script fetching
# json'ed data from data source.
#
# Script like this one is meant to be launched periodically from crontab.
#
# The main idea here is as follows: you're querying the data source(s) you want,
# transform resulting data according to your needs, and finally you're pushing
# it to your tile, along with optional config data. Really simple, isn't it?

import json
import requests

from subprocess import check_output

# Get your API_KEY from your settings file ('~/.tipboard/settings-local.py').
API_KEY = ''
# Change '127.0.0.1:7272' to the address of your Tipboard instance.
API_URL = 'http://127.0.0.1:7272/api/v0.1/{}'.format(API_KEY)
API_URL_PUSH = '/'.join((API_URL, 'push'))
API_URL_TILECONFIG = '/'.join((API_URL, 'tileconfig'))


#### Helper functions for data transformations (data sources --> tiles).

# We have only one tile here, hence 'prepare_for_pie_chart' is all we need,
# but in real-life scenario you may want some additional functions like
# 'prepare_for_line_chart', 'prepare_for_velocity_chart' and so on.

def prepare_for_pie_chart(data):
    # Pie chart needs data as a list of lists (whose elements are pairs
    # component-percentage), so we have to prepare it.
    data_prepared = []
    for k, v in data.items():
        data_prepared.append([k, v[0]])
    data_prepared = {'title': 'my title', 'pie_data': data_prepared}
    return data_prepared


#### Putting it all together.

def main():
    # Tile 'pie001' (pie chart)
    # (let's say we want to show issues count for project 'Tipboard' grouped by
    # issue status i.e. 'Resolved', 'In Progress', 'Open', 'Closed' etc.)
    TILE_NAME = 'pie_chart'
    TILE_KEY = 'pie001'
    # Now we are launching our script asking data source for the stuff we want:
    # (see its documentation for available options/switches)
    ds_output = check_output(["python", "jira-ds.py", "--project=Tipboard",
                              "--issues-counts"])
    data = json.loads(ds_output)
    data_selected = data.get('status_summary')
    data_prepared = prepare_for_pie_chart(data_selected)
    data_jsoned = json.dumps(data_prepared)
    data_to_push = {
        'tile': TILE_NAME,
        'key': TILE_KEY,
        'data': data_jsoned,
    }
    resp = requests.post(API_URL_PUSH, data=data_to_push)
    if resp.status_code != 200:
        print(resp.text)
        return

    # (optional) config for our pie chart, which is pushed in a separate request
    tile_config = {
        'legend': {
            'show': True,
            'location': 's',
        }
    }
    tile_config_jsoned = json.dumps(tile_config)
    data_to_push = {
        'value': tile_config_jsoned,
    }
    resp = requests.post(
        '/'.join((API_URL_TILECONFIG, TILE_KEY)),
        data=data_to_push,
    )
    if resp.status_code != 200:
        print(resp.text)
        return


    # Tile 'pie002'
    # TILE_NAME = 'pie_chart'
    # TILE_KEY = 'pie002'
    # output = check_output(...
    # ...and the rest in the same manner as in above example, i.e.:
    #  - query the data source for data
    #  - select what you want from that data
    #  - transform selected data according to tile's specs (if needed)
    #  - push transformed data to API_URL_PUSH
    #  - push config data for your tile to API_URL_CONFIG (let's say you want
    #    to override default behavior and show pie chart's legend at
    #    the bottom of the tile, or change some colors etc.)
    # That's all!


if __name__ == '__main__':
    main()
