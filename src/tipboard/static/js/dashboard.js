/**
 * Update the html of tile regarding the key to update
 * @param tileId id of tile in redis
 * @param dataToPut data to update
 * @param keysToUse list of key in tile, to update with dataToPut
 */
let updateKeyOfTiles = function updateKeyOfTiles(tileId, dataToPut, keysToUse) {
    // keysToUse*: list of keys, or string 'all', if 'all' then all keys used from *dataToPut*
    if (keysToUse === "all") {
        let allKeys = [];
        for (let data in dataToPut) {
            if ({}.hasOwnProperty.call(dataToPut, data)) {
                allKeys.push(data);
            }
        }
        keysToUse = allKeys;
    }
    $.each(keysToUse, function (idx, key) {
        let value = dataToPut[key.toString()];
        if (typeof (value) != "undefined") {
            let dstId = "#" + tileId + "-" + key;
            let dst = $(Tipboard.Dashboard.id2node(tileId)).find(dstId)[0];
            if (typeof dst === "undefined") {
                console.log("WARN: Not found node with id: " + dstId);
            } else {
                $(dst).text(value);
                console.log(dstId + ": was updated");
            }
        } else {
            console.log("WARN: No key \"" + key + "\" in data", dataToPut);
        }
    });
};

/**
 * destroy previous tile and create a new to refresh value
 * @param tileId
 * @param tileType
 * @param data
 * @param meta
 */
let updateTile = function (tileId, tileType, data, meta) {
    console.log("Update tile: ", tileId);
    let tile = Tipboard.Dashboard.id2node(tileId);
    // destroy old graph
    let chartObj = Tipboard.Dashboard.chartsIds[tileId.toString()];
    if (typeof chartObj === "object") {
        Tipboard.Dashboard.chartsIds[tileId.toString()].destroy();
    }
    try {
        // its a ptr to function, calling the right update function for the right tile
        Tipboard.Dashboard.getUpdateFunction(tileType)(tileId, data, meta, tileType);
        $.each([".tile-content"], function (idx, klass) {
            let node = $(tile).find(klass);
            if (node.length > 1) {
                $(node[1]).remove();
                $(node[0]).show();
            }
        });
    } catch (err) {
        $.each([".tile-content"], function (idx, klass) {
            let nodes = $(tile).find(klass);
            $(nodes[0]).hide();
            $(nodes[1]).show();
            nodes = $(tile).find(".tile-content");
            $(nodes[1]).html([
                "Tile " + tileId + " configuration error:",
                err.name || "error name: n/a",
                err.message || "error message: n/a",
            ].join("<br>"));
        });
    }
};

/**
 * return the Js func for a specific tile_template
 * @param tileType tile_template name
 * @returns {Function} js func to update html tile
 */
let getUpdateFunction = function getUpdateFunction(tileType) {
    switch (tileType) {
        case "vbar_chart":
            tileType = "bar_chart";
            break;
        case "doughnut_chart":
            tileType = "radar_chart";
            break;
        case "cumulative_flow":
            tileType = "line_chart";
            break;
    }
    let fn = this.updateFunctions[tileType.toString()];
    if (typeof fn !== "function") {
        throw new Tipboard.Dashboard.UnknownUpdateFunction(tileType);
    }
    return fn;
};

let autoAddFlipClasses = function (flippingContainer) {
    $.each($(flippingContainer).find(".tile"), function (idx, elem) {
        if (idx === 0) {
            $(elem).addClass("flippedforward");
        }
        $(elem).addClass("flippable");
    });
};

/**
 * the Tipboard application allows user to use eg. '.' in tiles' ids, jquery requires such chars to be escaped
 * @param id
 * @returns {*}
 */
let escapeId = function (id) {
    let charsToEscape = "\\!\"#$%&'()*+,./:;<=>?@[]^`{|}~";
    for (let i = 0; i < charsToEscape.length; i++) {
        let _char = charsToEscape[i + ""];
        id = id.replace(_char, "\\" + _char);
    }
    return id;
};


function initDashboard(Tipboard) {
    Tipboard.Dashboard.id2node = id => $("#" + id)[0];
    Tipboard.Dashboard.tile2id = tileNode => $(tileNode).attr("id");
    Tipboard.Dashboard.registerUpdateFunction = function (name, fn) {
        this.updateFunctions[name.toString()] = fn;
    };
    Tipboard.Dashboard.escapeId = escapeId;
    Tipboard.Dashboard.setDataByKeys = updateKeyOfTiles;
    Tipboard.Dashboard.updateTile = updateTile;
    Tipboard.Dashboard.getUpdateFunction = getUpdateFunction;
    Tipboard.Dashboard.autoAddFlipClasses = autoAddFlipClasses;


}
