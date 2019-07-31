/*jslint browser: true, devel: true*/
/*global $, WebSocket: false, Tipboard: false*/

"use strict";

function updateTileSimplePercentage(tileId, data, config) {
    Tipboard.Dashboard.setDataByKeys(tileId, data, 'all');
    var highlighterNode = $('#' + tileId + '-big_value').parent();
    Tipboard.DisplayUtils.applyHighlighterConfig(
        highlighterNode, config.big_value_color, config.fading_background
    );
    var tile = Tipboard.Dashboard.id2node(tileId);
    // TODO: use rescaleTile instead
    Tipboard.TileDisplayDecorator.runAllDecorators(tile);
    Tipboard.DisplayUtils.expandLastChild($(tile).find('.tile-content')[0]);
}

Tipboard.Dashboard.registerUpdateFunction('simple_percentage', updateTileSimplePercentage);
