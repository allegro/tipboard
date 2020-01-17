/**
 * Update bigvalue tiles the values & config
 * @param tileId
 * @param data
 * @param config
 * @param tileType
 */
function updateTileBigValue(tileId, data, config, tileType) {
    if (!("title" in data)) {
        data.title = "montitre";
    }
    let description = document.getElementById(tileId + "-description");
    if (!("description" in data) || data.description.length === 0) {
        data.description = "0x42";
        Tipboard.Dashboard.setDataByKeys(tileId, data, "all");
        description.style.color = "#00414141";
        description.className = "text";
    } else {
        Tipboard.Dashboard.setDataByKeys(tileId, data, "all");
        description.className = "text-white";
    }
    Tipboard.Palette.applyFading(document.getElementById("body-" + tileId),
        config.big_value_color, config.fading_background);
}

Tipboard.Dashboard.registerUpdateFunction("big_value", updateTileBigValue);

