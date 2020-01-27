/**
 * Update text tile, font, color & value
 * @param tileId
 * @param data
 * @param meta
 */
function updateTileText(tileId, data) {
    let parser = new DOMParser();
    let body = document.getElementById(tileId + "-body");
    let parsed = parser.parseFromString(data.text, "text/html");
    let tags = parsed.getElementsByTagName("body");
    body.innerHTML = "";
    for (const tag of tags) {
         body.innerText = tag.innerText;
    }
}

/**
 * Add html li for every item text
 * @param container
 * @param itemText
 */
function appendListingItem(container, itemText) {
    let htmlLabel = [
        "<li class=\"list-group-item text-white\" style=\"background: #212121\">",
        itemText,
        "</li>"
    ].join("\n");
    $(container).append(htmlLabel);
}

/**
 * Update listing tile
 * @param id
 * @param data
 * @param meta
 * @param tileType
 */
function updateTileListing(id, data) {
    let MAX_ITEMS = 7;
    let tile = $("#" + id)[0];
    let container = $(tile).find(".list-group")[0];
    $(container).children().remove();
    for (let idx in data.items) {
        if ({}.hasOwnProperty.call(data.items, idx)) {
            if (idx > MAX_ITEMS) {
                break;
            }
            appendListingItem(container, data.items[parseInt(idx, 10)]);
        }
    }
}

/**
 * Update bigvalue tiles the values & config
 * @param tileId
 * @param data
 * @param config
 * @param tileType
 */
function updateTileBigValue(tileId, data, config) {
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
        description.className = "text-white";
    }
}

/**
 * Control all text_tile update fucntion
 * @param tileId
 * @param data
 * @param config
 * @param tileType
 */
function updateTileTextValue(tileId, data, config, tileType) {
    if (tileType === "listing") {
        updateTileListing(tileId, data);
        return;
    }
    if (tileType === "text") {
        updateTileText(tileId, data);
        return;
    }
    if (tileType === "big_value") {
        updateTileBigValue(tileId, data, config);
    }
    Tipboard.Dashboard.setDataByKeys(tileId, data, "all");
    let body = document.getElementById("body-" + tileId);
    Tipboard.Dashboard.applyFading(body, config.big_value_color, config.fading_background);
}

Tipboard.Dashboard.registerUpdateFunction("just_value", updateTileTextValue);
Tipboard.Dashboard.registerUpdateFunction("simple_percentage", updateTileTextValue);
Tipboard.Dashboard.registerUpdateFunction("big_value", updateTileTextValue);
Tipboard.Dashboard.registerUpdateFunction("listing", updateTileTextValue);
Tipboard.Dashboard.registerUpdateFunction("text", updateTileTextValue);
