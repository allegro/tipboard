function updateTileJustValue(tileId, data, config, tileType) {
    // let tile = Tipboard.Dashboard.id2node(tileId);
    JustValue.setDataByKeys(tileId, data, "all");
    // let highlighterNode = $("#" + tileId + "-just-value").parent();
    // Tipboard.DisplayUtils.applyHighlighterConfig(
    //     highlighterNode, config["just-value-color"], config.fading_background
    // );
}

Tipboard.Dashboard.registerUpdateFunction("just_value", updateTileJustValue);

JustValue = {
    setDataByKeys: function(tileId, data, keys) {
        Tipboard.Dashboard.setDataByKeys(tileId, data, keys);
    }
};
