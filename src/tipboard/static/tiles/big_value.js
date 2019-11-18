// BigValueTile = {
//     setDataByKeys: function(tileId, data, keys) {
//         Tipboard.Dashboard.setDataByKeys(tileId, data, keys);
//     },
//     setBigValueColor: function(tileId, meta) {
//         // DEPRECATED function, Tipboard.DisplayUtils.applyHighlighterConfig
//         let color = meta["big_value_color"];
//         if (typeof(color) !== "undefined") {
//             // color = Tipboard.DisplayUtils.replaceFromPalette(color);
//             // let tile = Tipboard.Dashboard.id2node(tileId);
//             // let bigValue = $(tile).find("#" + tileId + "-big-value")[0];
//             // let dst = $(bigValue).parent();
//             // $(dst).css("background-color", color);
//         }
//     }
// };
//

function updateTileBigValue(tileId, data, config, tileType) {
    if (!("title" in data)) {
        data["title"] = "montitre";
    }
    let description = document.getElementById(tileId + "-description");
    if (!("description" in data) || data["description"].length === 0) {
        data["description"] = "0x42";
        Tipboard.Dashboard.setDataByKeys(tileId, data, "all");
        description.style.color = "#00414141";
        description.className = "text";
    } else {
        Tipboard.Dashboard.setDataByKeys(tileId, data, "all");
        description.className = "text-white";
    }
    // let tile = Tipboard.Dashboard.id2node(tileId);
    // let highlighterNode = $("#" + tileId + "-big-value").parent();
    // Tipboard.DisplayUtils.applyHighlighterConfig(
    //     highlighterNode, config.big_value_color, config.fading_background
    // );
    // Tipboard.TileDisplayDecorator.runAllDecorators(tile);
}

Tipboard.Dashboard.registerUpdateFunction("big_value", updateTileBigValue);

