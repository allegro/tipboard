function initDashboard3(Tipboard) {
    Tipboard.Dashboard.registerUpdateFunction = function (name, fn) {
        console.log("Registering Functionetion tile:" + name);
        this.updateFunctions[name.toString()] = fn;
    };
    Tipboard.Dashboard.autoAddFlipClasses = function (flippingContainer) {
        $.each($(flippingContainer).find(".tile"), function (idx, elem) {
            if (idx === 0) {
                $(elem).addClass("flippedforward");
            }
            $(elem).addClass("flippable");
        });
    };
}

function initDashboard2(Tipboard) {
    Tipboard.Dashboard.setDataByKeys = function (tileId, dataToPut, keysToUse) {
        /*
        *keysToUse*: list of keys, or string 'all', if 'all' then all keys used from *dataToPut*
        */
        console.log(tileId + ".setDataByKeys => ");
        if (keysToUse === "all") {
            var allKeys = [];
            for (let data in dataToPut) {
                if ({}.hasOwnProperty.call(dataToPut, data)) {
                    allKeys.push(data);
                }
            }
            keysToUse = allKeys;
        }
        console.log(tileId + ".setDataByKeys => ");
        let tile = Tipboard.Dashboard.id2node(tileId);
        $.each(keysToUse, function (idx, key) {
            console.log("key=>" + key);
            let value = dataToPut[key.toString()];
            if (typeof (value) == "undefined") {
                console.log("WARN: No key \"" + key + "\" in data", dataToPut);
            } else {
                let dstId = "#" + tileId + "-" + key;
                let dst = $(tile).find(dstId)[0];
                if (typeof dst === "undefined") {
                    console.log("WARN: Not found node with id: " + dstId);
                } else {
                    $(dst).text(value);
                    console.log(dstId + ": was updated");
                }
            }
        });
    };
    Tipboard.Dashboard.updateTile = function (tileId, tileType, data, meta) {
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
    Tipboard.Dashboard.getUpdateFunction = function (tileType) {
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
    initDashboard3(Tipboard);
}


/**
 *
 * @param Tipboard
 */
function initDashboard(Tipboard) {
    Tipboard.Dashboard.id2node = function (id) {
        return $("#" + id)[0];
    };
    Tipboard.Dashboard.tile2id = function (tileNode) {
        return $(tileNode).attr("id");
    };
    Tipboard.Dashboard.escapeId = function (id) {
        /*
        the Tipboard application allows user to use eg. '.' in tiles' ids
        jquery requires such chars to be escaped
        XXX: backslash MUST BE FIRST, otherwise this convertions is
        broken (escaping chars which meant to be escapers)
        */
        let charsToEscape = "\\!\"#$%&'()*+,./:;<=>?@[]^`{|}~";
        for (let i = 0; i < charsToEscape.length; i++) {
            let _char = charsToEscape[i + ""];
            id = id.replace(_char, "\\" + _char);
        }
        return id;
    };
    initDashboard2(Tipboard);
}
