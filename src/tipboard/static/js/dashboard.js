function initDashboard3(Tipboard) {
    Tipboard.Dashboard.registerUpdateFunction = function (name, fn) {
        console.log("Registering Functionetion tile:" + name);
        this.updateFunctions[name.toString()] = fn;
    };
    Tipboard.Dashboard.isTileRenderedSuccessful = function (tile) {
        var suc = $(tile).find(".exception-message").length === 0;
        return suc;
    };
    Tipboard.Dashboard.autoAddFlipClasses = function (flippingContainer) {
        $.each($(flippingContainer).find(".tile"), function (idx, elem) {
            if (idx === 0) {
                $(elem).addClass("flippedforward");
            }
            $(elem).addClass("flippable");
        });
    };
    Tipboard.Dashboard.addTilesCounter = function (col) {
        var tilesTotal = $(col).children("div.tile").length;
        if (tilesTotal > 1) {
            $.each($(col).children("div"), function (tileIdx, tile) {
               console.log("Building flip for tile");
               var container = $(tile).find(".tile-header");
                //var title = $(container).children()[0];
                $(container).addClass("flip-tile-counter");
                var counter = (tileIdx + 1) + "/" + tilesTotal;
                $(container).append(counter);
                $(container).append("<div style=\"clear:both\"></div>");
            });
        }
    };
}

function initDashboard2(Tipboard) {
    Tipboard.Dashboard.setDataByKeys = function (tileId, dataToPut, keysToUse) {
        /*
        *keysToUse*: list of keys, or string 'all', if 'all' then all keys used from *dataToPut*
        */
        if (keysToUse === "all") {
            var allKeys = [];
            for (let data in dataToPut) {
                if ({}.hasOwnProperty.call(dataToPut, data)) {
                    allKeys.push(data);
                }
            }
            keysToUse = allKeys;
        }
        var tile = Tipboard.Dashboard.id2node(tileId);
        $.each(keysToUse, function (idx, key) {
            var value = dataToPut[key.toString()];
            if (typeof (value) == "undefined") {
                console.log("WARN: No key \"" + key + "\" in data", dataToPut);
            } else {
                var dstId = "#" + tileId + "-" + key;
                var dst = $(tile).find(dstId)[0];
                if (typeof dst === "undefined") {
                    console.log("WARN: Not found node with id: " + dstId);
                } else {
                    $(dst).text(value);
                }
            }
        });
    };
    Tipboard.Dashboard.updateTile = function (tileId, tileType, data, meta) {
        console.log("Update tile: ", tileId);
        var tile = Tipboard.Dashboard.id2node(tileId);
        // destroy old graph
        var chartObj = Tipboard.Dashboard.chartsIds[tileId.toString()];
        if (typeof chartObj === "object") {
            Tipboard.Dashboard.chartsIds[tileId.toString()].destroy();
        }
        try {
            // its a ptr to function, calling the right update function for the right tile
            Tipboard.Dashboard.getUpdateFunction(tileType)(tileId, data, meta, tileType);
            $.each([".tile-content"], function (idx, klass) {
                var node = $(tile).find(klass);
                if (node.length > 1) {
                    $(node[1]).remove();
                    $(node[0]).show();
                }
            });
        } catch (err) {
            $.each([".tile-content"], function (idx, klass) {
                var nodes = $(tile).find(klass);
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
    Tipboard.Dashboard.getUpdateFunction = function (tileType) {
        // to not duplicate js, and get separation for none tech user
        // we use same the same chartJS widget but different name
        if (tileType === "vbar_chart") {tileType = "bar_chart";}
        else if (tileType === "doughnut_chart") {tileType = "radar_chart";}
        else if (tileType === "cumulative_flow") {tileType = "line_chart";}
        var fn = this.updateFunctions[tileType.toString()];
        if (typeof fn !== "function") {throw new Tipboard.Dashboard.UnknownUpdateFunction(tileType);}
        return fn;
    };
    initDashboard3(Tipboard);
}


/**
 *
 * @param Tipboard
 */
function initDashboard(Tipboard) {
    Tipboard.Dashboard.id2node = function (id) {
        var tile = $("#" + id)[0];
        return tile;
    };
    Tipboard.Dashboard.tile2id = function (tileNode) {
        return $(tileNode).attr("id");
    };
    Tipboard.Dashboard.escapeId = function (id) {
        /*
        the Tipboard application allows user to use eg. '.' in tiles' ids
        jquery requires such chars to be escaped
        */
        // XXX: backslash MUST BE FIRST, otherwise this convertions is
        // broken (escaping chars which meant to be escapers)
        var charsToEscape = "\\!\"#$%&'()*+,./:;<=>?@[]^`{|}~";
        for (var i = 0; i < charsToEscape.length; i++) {
            var _char = charsToEscape[i + ""];
            id = id.replace(_char, "\\" + _char);
        }
        return id;
    };
    initDashboard2(Tipboard);
}
