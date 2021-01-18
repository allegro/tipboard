/**
 * Update the html of tile regarding the key to update
 * @param tileId id of tile in redis
 * @param tileData data to update
 */
function setDataByKeys(tileId, tileData) {
    let fieldsToUpdate = [];
    for (let data in tileData) {
        if ({}.hasOwnProperty.call(tileData, data)) {
            fieldsToUpdate.push(data);
        }
    }
    $.each(fieldsToUpdate, function (idx, key) {
        let value = tileData[key.toString()];
        let dst = $($("#" + tileId)[0]).find("#" + tileId + "-" + key)[0];
        $(dst).text(value);
        if ($(dst).hidden) {
            $(dst).show();
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
    return true;
}

/**
 * Update Custom Tile
 * @param tileId
 * @param data
 */
function updateTileCustomTile(tileId, data) {
    let tile = document.getElementById(tileId);
    tile.innerHTML = data.text;
    return true;
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
    return true;
}

/**
 * Build Tile stream with Hls and save it in Tipboard.chartJsTile object
 * @param tileId
 */
function buildTileStream(tileId) {
    Tipboard.chartJsTile[tileId] = { // first creation of the tile
        hls: new Hls(),
        container: document.getElementById(tileId + "-stream"),
        video: document.createElement("video")
    };
    let stream_tile = Tipboard.chartJsTile[tileId];
    stream_tile.container.appendChild(stream_tile.video);
    stream_tile.video.setAttribute("width", stream_tile.video.parentElement.clientWidth);
    stream_tile.video.setAttribute("height", stream_tile.video.parentElement.clientHeight);
    stream_tile.video.muted = "muted";
}

/**
 * Update or create tile stream by by loading Source in Hls
 * @param tileId
 * @param data
 */
function updateTileStream(tileId, data) {
    if (!(tileId in Tipboard.chartJsTile)) {
        buildTileStream(tileId);
    } else { // update the tile to kill the actual media in order to replace it
        Tipboard.chartJsTile[tileId].hls.detachMedia();
        Tipboard.chartJsTile[tileId].hls.destroy();
        Tipboard.chartJsTile[tileId].hls = new Hls();
    }
    Tipboard.chartJsTile[tileId].hls.loadSource(data.url); // start the media
    Tipboard.chartJsTile[tileId].hls.attachMedia(Tipboard.chartJsTile[tileId].video);
    Tipboard.chartJsTile[tileId].hls.on(Hls.Events.MEDIA_ATTACHED, function () {
        Tipboard.chartJsTile[tileId].video.play();
    });
    return true;
}

/**
 * Hide elemen in tiles with no value, to not let previous value stay
 * @param tileId
 * @param tileData
 */
function hideElementNotPresent(tileId, tileData) {
    if (!("title" in tileData)) {
        $("#" + tileId + "-title").hide();
    }
    if (!("description" in tileData)) {
        $("#" + tileId + "-subtitle").hide();
    }
}

/**
 * Update misc tile if it's one
 * @param tileData
 * @param tileId
 * @returns {boolean}
 */
function isMiscTile(tileData, tileId) {
    let isMiscTile = false;
    switch (tileData["tile_template"]) {
        case "iframe":
            document.getElementById(tileId + "-iframe").src = tileData.data.url;
            isMiscTile = true;
            break;
        case "stream":
            isMiscTile = updateTileStream(tileId, tileData.data);
            break;
        case "listing":
            isMiscTile = updateTileListing(tileId, tileData.data);
            break;
        case "text":
            isMiscTile = updateTileText(tileId, tileData.data);
            break;
        case "custom":
            isMiscTile = updateTileCustomTile(tileId, tileData.data);
            break;
    }
    return isMiscTile;
}

/**
 * Control all text_tile update function
 * @param tileData
 * @param dashboard_name
 */
function updateTileTextValue(tileData, dashboard_name) {
    let id = `${dashboard_name}-${tileData["id"]}`;
    if (isMiscTile(tileData, id) === false) {
        console.log(id + " was updated");
        hideElementNotPresent(id, tileData.data);
        setDataByKeys(id, tileData.data);
        let body = document.getElementById("body-" + id);
        applyFading(body, tileData.meta["big_value_color"], tileData.meta["fading_background"]);
    }
}
