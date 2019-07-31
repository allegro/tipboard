/*jslint browser: true, devel: true*/
/*global WebSocket: false, Tipboard: false*/

function updateTileText(id, data, meta, tipboard) {
    var tile = $("#" + id)[0];
    var textSelector = 'span.text-container';
    containers = $(tile).find(textSelector);
    if (containers.length != 1) {
        console.log('tile ' + tile + 'does not include ONE: ' + textSelector);
    }
    var nodeWithText = containers[0];
    $(nodeWithText).html(data['text']);

    var textSelector = '#' + id + ' .text-container';
    if (meta.font_size) {
        $(textSelector).css("font-size", meta.font_size);
    }
    if (meta.font_color) {
        $(textSelector).css(
            "color", Tipboard.DisplayUtils.replaceFromPalette(meta.font_color)
        );
    }
    if (meta.font_weight) {
        $('.text-container').css("font-weight", meta.font_weight);
    }
    Tipboard.TileDisplayDecorator.runAllDecorators(tile);
}
Tipboard.Dashboard.updateFunctions['text'] = updateTileText;

