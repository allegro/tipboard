from django import template
from django.template.loader import render_to_string
from src.tipboard.app.properties import ALLOWED_TILES
register = template.Library()

# Tu test la tile bar_chartjs

@register.filter(name ="template_tile")
def template_tile(tile_id, tile_data):
    """
    return a String, this is the render of the tile template
    :param tile_id:
    :param tile_data:
    :return:
    """
    # print(f"Template filter: returning: template for {tile_data['tile_template']}")
    data = {'tile_id': tile_id, "title": tile_data['title'], 'tile_template': tile_data['tile_template']}
    if type(tile_data) is dict and tile_data['tile_template'] in ALLOWED_TILES:
        try:
            return render_to_string(f"tiles/{tile_data['tile_template']}.html", data)
        except Exception as e:
            data['error'] = f'{e}'
            return render_to_string(f"tiles/error_buildingtiles.html", data)
    return render_to_string(f"tiles/notfound_tiles.html", data)
#Tu dois faire le template error_generating a base de not found