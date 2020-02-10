/**
 * Update the html of tile regarding the key to update
 * @param tileId id of tile in redis
 * @param dataToPut data to update
 * @param keysToUse list of key in tile, to update with dataToPut
 */
function setDataByKeys(tileId, dataToPut, keysToUse, dashboardname) {
    if (keysToUse === "all") { // keysToUse*: list of keys, or string 'all', if 'all' then all keys used from *dataToPut*
        keysToUse = [];
        for (let data in dataToPut) {
            if ({}.hasOwnProperty.call(dataToPut, data)) {
                keysToUse.push(data);
            }
        }
    }
    $.each(keysToUse, function (idx, key) {
        let value = dataToPut[key.toString()];
        if (typeof (value) !== "undefined") {
            console.log("$('#" + tileId + "').find('#" + tileId + "-" + key + "')");
            let dst = $($("#" + tileId)[0]).find("#" + tileId + "-" + key)[0];
            if (typeof dst !== "undefined") {
                $(dst).text(value);
            }
        }
    });
}

/**
 * Add fading class to the tile
 * @param node
 * @param color
 * @param fading
 */
function applyFading(node, color, fading) {
    node.style.backgroundColor = color;
    if (fading === true) {
        node.classList.add("fading-background-color");
    } else {
        node.classList.remove("fading-background-color");
    }
}

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
 * @param tileType
 */
function updateTileBigValue(tileId, data, dashboardname) {
    if (!("title" in data)) {
        data.title = "montitre";
    }
    let description = document.getElementById(tileId + "-description");
    if (!("description" in data) || data.description.length === 0) {
        data.description = "0x42";
        setDataByKeys(tileId, data, "all", dashboardname);
        description.style.color = "#00414141";
        description.className = "text";
    } else {
        description.className = "text-white";
    }
}

/**
 * Control all text_tile update fucntion
 * @param tileData
 * @param dashboardname
 */
function updateTileTextValue(tileData, dashboardname) {
    let id = `${dashboardname}-${tileData['id']}`;
    console.log('Start text tile:' +  id);
    if (tileData.tile_template === "listing") {
        updateTileListing(id, tileData.data);
        return;
    }
    if (tileData.tile_template === "text") {
        updateTileText(id, tileData.data);
        return;
    }
    if (tileData.tile_template === "big_value") {
        updateTileBigValue(id, tileData.data, dashboardname);
    }
    setDataByKeys(id, tileData.data, "all", dashboardname);
    console.log('End text tile:' +  id);
    let body = document.getElementById("body-" + id);
    applyFading(body, tileData.meta.big_value_color, tileData.meta.fading_background);
}
