/*jslint browser: true, devel: true*/
/*global $, WebSocket: false, Tipboard: false*/

"use strict";

function updateTileSimplePercentage(tileId, data, config, tileType) {
    Tipboard.Dashboard.setDataByKeys(tileId, data, 'all');
    var highlighterNode = $('#' + tileId + '-big_value').parent();
    var tile = Tipboard.Dashboard.id2node(tileId);
}

Tipboard.Dashboard.registerUpdateFunction('simple_percentage', updateTileSimplePercentage);
