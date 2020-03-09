/**
 * Update the html of tile regarding the key to update
 * @param tileId id of tile in redis
 * @param dataToPut data to update
 * @param keysToUse list of key in tile, to update with dataToPut
 */
function setDataByKeys(tileId, dataToPut, keysToUse) {
    if (keysToUse === "all") { // keysToUse*: if 'all' then all keys used from *dataToPut*
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
            let dst = $($("#" + tileId)[0]).find("#" + tileId + "-" + key)[0];
            if (typeof dst !== "undefined") {
                $(dst).text(value);
                if ($(dst).hidden) {
                    $(dst).show();
                }
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
 * Update Custom Tile
 * @param tileId
 * @param data
 */
function updateTileCustomTile(tileId, data) {
    let tile = document.getElementById(tileId);
    tile.innerHTML = data.text;
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
}

/**
 * Update or create tile stream by by loading Source in Hls
 * @param tileId
 * @param data
 */
function updateTileStream(tileId, data) {
    if (!(tileId in Tipboard.chartJsTile)) { // first created
        Tipboard.chartJsTile[tileId] = {
            hls: new Hls(),
            container: document.getElementById(tileId + "-stream"),
            video: document.createElement("video")
        };
        let stream_tile = Tipboard.chartJsTile[tileId];
        stream_tile.container.appendChild(stream_tile.video);
        let width = stream_tile.video.parentElement.clientWidth;
        let height = stream_tile.video.parentElement.clientHeight;
        stream_tile.video.setAttribute("width", width);
        stream_tile.video.setAttribute("height", height);
        stream_tile.video.muted = "muted";
        stream_tile.hls.loadSource(data.url);
        stream_tile.hls.attachMedia(stream_tile.video);
        stream_tile.hls.on(Hls.Events.MEDIA_ATTACHED, function () {
            stream_tile.video.play();
        });
    } else { // updated by sensors
        let stream_tile = Tipboard.chartJsTile[tileId];
        Tipboard.chartJsTile[tileId].hls.detachMedia();
        Tipboard.chartJsTile[tileId].hls.destroy();
        Tipboard.chartJsTile[tileId].hls = new Hls();
        stream_tile.hls.loadSource(data.url);
        stream_tile.hls.attachMedia(stream_tile.video);
        stream_tile.hls.on(Hls.Events.MEDIA_ATTACHED, function () {
            stream_tile.video.play();
        });
    }
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
 * Control all text_tile update function
 * @param tileData
 * @param dashboard_name
 */
function updateTileTextValue(tileData, dashboard_name) {
    let id = `${dashboard_name}-${tileData["id"]}`;
    switch (tileData["tile_template"]) {
        case "iframe":
            document.getElementById(tileId + "-iframe").src = tileData.data.url;
            return;
        case "stream":
            updateTileStream(id, tileData.data);
            return;
        case "listing":
            updateTileListing(id, tileData.data);
            return;
        case "text":
            updateTileText(id, tileData.data);
            return;
        case "custom":
            updateTileCustomTile(id, tileData.data);
            return;
    }
    hideElementNotPresent(id, tileData.data);
    setDataByKeys(id, tileData.data, "all");
    let body = document.getElementById("body-" + id);
    applyFading(body, tileData.meta["big_value_color"], tileData.meta["fading_background"]);
}
