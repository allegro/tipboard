/*jslint browser: true, devel: true*/
/*global WebSocket: false, Tipboard: false*/

function updateTileJustValue(tileId, data, config) {
    var tile = Tipboard.Dashboard.id2node(tileId);
    JustValue.setDataByKeys(tileId, data, 'all');
    var highlighterNode = $('#' + tileId + '-just-value').parent();
    Tipboard.DisplayUtils.applyHighlighterConfig(
        highlighterNode, config['just-value-color'], config.fading_background
    );
    Tipboard.TileDisplayDecorator.runAllDecorators(tile);
}

Tipboard.Dashboard.registerUpdateFunction('just_value', updateTileJustValue);

JustValue = {
    setDataByKeys: function(tileId, data, keys) {
        Tipboard.Dashboard.setDataByKeys(tileId, data, keys);
    },
    setJustValueColor: function(tileId, meta) {
        // DEPRECATED function, Tipboard.DisplayUtils.applyHighlighterConfig
        var color = meta['just-value-color'];
        if (typeof(color) !== 'undefined') {
            color = Tipboard.DisplayUtils.replaceFromPalette(color);
            var dst = $('#' + tileId + '-just-value').parent();
            $(dst).css('background-color', color);
        }
    }
};
