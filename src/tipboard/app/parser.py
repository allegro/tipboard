import glob, os, yaml
from src.tipboard.app import properties
from src.tipboard.app.utils import getTimeStr
from src.tipboard.app.properties import DEBUG


class WrongSumOfRows(Exception):
    pass


def _get_tiles_dict(col):
    return list(col.values())[0]


def get_cols(rows):
    # TODO: validation col_1_of_4
    cols = []
    for col in list(rows.values())[0]:
        cols.append(col)
    return cols


def get_rows(layout):
    """Validates and returns number of rows."""
    rows_data = []
    rows_class = []
    for row in layout:
        rows_data.append(row)
        rows_class.append(list(row.keys()))
    rows_count = 0
    sum_of_rows = []
    for row_class in rows_class:
        splited_class = row_class[0].split('_')  # ex: row_1_of_2
        row = splited_class[1]
        of_rows = int(splited_class[3])
        if rows_count == 0:
            rows_count = int(of_rows)
            sum_of_rows.append(int(row))
        elif not rows_count == of_rows:
            raise WrongSumOfRows('The sum of the lines is incorrect.')
        else:
            sum_of_rows.append(int(row))
    if not sum(sum_of_rows) == rows_count:
        raise WrongSumOfRows('The sum of the lines is incorrect.')
    return rows_data


def get_config_files_names():
    """
    Return all configs files' names (without '.yaml' ext.) from user space
    (.tipboard/)
    """
    configs_names = []
    configs_dir = os.path.join(properties.user_config_dir, '*.yaml')
    for config_path in glob.glob(configs_dir):
        filename = os.path.basename(config_path)
        head, ext = os.path.splitext(filename)
        configs_names.append(head)
    return configs_names


def config_file_name2path(config_name):
    """
    Return file path to *config_name* (eg. 'layout_config')
    """
    path = os.path.join(
        properties.user_config_dir, ''.join([config_name])
    )
    return path


def get_tiles_configs():
    """
    Return dict with tiles keys and ids from all available configs
    """
    tiles_configs = {
        'tiles_keys': set(),
        'tiles_names': set()
    }
    configs_names = get_config_files_names()
    for config_name in configs_names:
        parsed_config = parse_xml_layout(config_name)
        tiles_configs['tiles_keys'].update(set(parsed_config['tiles_keys']))
        tiles_configs['tiles_names'].update(set(parsed_config['tiles_names']))
    return tiles_configs


def analyse_cols(tiles_id, tiles_templates, tiles_dict):
    for tile_dict in tiles_dict:
        if tile_dict['tile_id'] not in tiles_id:
            tiles_id.append(tile_dict['tile_id'])
            tiles_templates.append(tile_dict['tile_template'])


def find_tiles_names(cols_data):
    tiles_templates, tiles_id = list(), list()
    for col_dict in cols_data:
        for tiles_dict in list(col_dict.values()):
            analyse_cols(tiles_id, tiles_templates, tiles_dict)
    if DEBUG:
        print(f"{getTimeStr()} (+) Parsing Config file with {len(tiles_id)} tiles parsed "
              f"and {len(tiles_templates)} tiles templates")
    return tiles_templates, tiles_id


def parse_xml_layout(layout_name='layout_config'):
    config_path = config_file_name2path(layout_name)
    try:
        with open(config_path, 'r') as layout_config:
            config = yaml.safe_load(layout_config)
    except FileNotFoundError:
        if ".yaml" not in config_path:
            config_path += ".yaml"
        with open(config_path, 'r') as layout_config:
            config = yaml.safe_load(layout_config)
    rows = [row for row in get_rows(config['layout'])]
    cols = [col for col in [get_cols(row) for row in rows]]
    cols_data = [colsValue for colsList in cols for colsValue in colsList]
    config['tiles_names'], config['tiles_keys'] = find_tiles_names(cols_data)
    return config


def getSrcJssForTilesInLayout(tiles_name):
    listOfTiles = list()
    for name_tile in tiles_name:
        if not listOfTiles.__contains__(name_tile):
            if name_tile == "vbar_chart":
                name_tile = "bar_chart"
            elif name_tile == "cumulative_flow":
                name_tile = "line_chart"
            elif name_tile == "doughnut_chart":
                name_tile = "radar_chart"
            listOfTiles.append(name_tile)
    return listOfTiles
