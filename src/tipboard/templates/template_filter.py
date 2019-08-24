from django import template

register = template.Library()

ALLOWED_TILES = ["text", "pie_chart",  "line_chart", "cumulative_flow", "simple_percentage", "listing", "bar_chart",
                 "norm_chart", "fancy_listing", "big_value", "just_value", "advanced_plot",  "empty",   #jqplot

                 "line_chartjs"]#chartjs

from django.template.loader import render_to_string

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
        #print(template_generated)
        return template_generated
    #print(f"Nothing")
    return ""