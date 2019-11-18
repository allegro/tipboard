function updateTileBigValue(tileId, data, config, tileType) {
    // let tile = Tipboard.Dashboard.id2node(tileId);
    console.log('updateTileSimplePercentage START');
    console.log(data);
    if (!("title" in data)) {
        data["title"] = "montitre";
    }

    if (!("description" in data) || data["description"].length === 0) {
        data["description"] = "Hifgdded";
        BigValueTile.setDataByKeys(tileId, data, "all");
        document.getElementById(tileId + "-description").style.color = "#00414141";
        document.getElementById(tileId + "-description").className = 'text';
    } else {
        console.log('updateTileSimplePercentage ALTERED');
        console.log(data);
        BigValueTile.setDataByKeys(tileId, data, "all");
    }
    // let highlighterNode = $("#" + tileId + "-big-value").parent();
    // Tipboard.DisplayUtils.applyHighlighterConfig(
    //     highlighterNode, config.big_value_color, config.fading_background
    // );
    // Tipboard.TileDisplayDecorator.runAllDecorators(tile);
}

Tipboard.Dashboard.registerUpdateFunction("big_value", updateTileBigValue);

BigValueTile = {
    setDataByKeys: function(tileId, data, keys) {
        Tipboard.Dashboard.setDataByKeys(tileId, data, keys);
    },
    setBigValueColor: function(tileId, meta) {
        // DEPRECATED function, Tipboard.DisplayUtils.applyHighlighterConfig
        let color = meta["big_value_color"];
        if (typeof(color) !== "undefined") {
            // color = Tipboard.DisplayUtils.replaceFromPalette(color);
            // let tile = Tipboard.Dashboard.id2node(tileId);
            // let bigValue = $(tile).find("#" + tileId + "-big-value")[0];
            // let dst = $(bigValue).parent();
            // $(dst).css("background-color", color);
        }
    }
};

