"use strict";

function updateTileSimplePercentage(tileId, data, config, tileType) {
    //update the tile value
    windows.Tipboard.Dashboard.setDataByKeys(tileId, data, 'all');
    //update background color regarding the config['fading_value'] if conf['fading_'] is true
//    var highlighterNode = $('#' + tileId + '-big_value').parent();
    //var tile = Tipboard.Dashboard.id2node(tileId);
}

Tipboard.Dashboard.registerUpdateFunction('simple_percentage', updateTileSimplePercentage);
