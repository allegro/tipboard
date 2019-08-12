from django import template

register = template.Library()

ALLOWED_TILES = ["text", "simple_percentage", "pie_chart", "norm_chart", "listing", "line_chart", "just_value",
                 "fancy_listing", "empty", "cumulative_flow", "big_value", "bar_chart", "advanced_plot"]
from django.template.loader import render_to_string

@register.filter(name ="template_tile")
def template_tile(tile_id, tile_data):
    """
    return a String, this is the render of the tile template
    :param tile_id:
    :param tile_data:
    :return:
    """
    if type(tile_data) is dict and tile_data['tile_template'] in ALLOWED_TILES:
        return render_to_string(f"tiles/{tile_data['tile_template']}.html",
                                {'tile_id': tile_id, "title": tile_data['title']})
    return ""