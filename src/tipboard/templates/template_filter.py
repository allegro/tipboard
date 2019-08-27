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
    #print(f"Template filter: returning: template for {tile_data['tile_template']}")

    if type(tile_data) is dict and tile_data['tile_template'] in ALLOWED_TILES:
        template_generated = render_to_string(f"tiles/{tile_data['tile_template']}.html",
                                              {'tile_id': tile_id, "title": tile_data['title']})
    else:
        template_generated = render_to_string(f"tiles/notfound_tiles.html",
                                              {'tile_id': tile_id, "template": tile_data['tile_template']})
    return template_generated
