
// Definition of the Exception UnknownRenderer
var UnknownRenderer = function (rendererName) {
    this.name = "UnknownRederer";
    this.message = "Renderer: '" + rendererName + "' not found";
};
window.Tipboard = {};
UnknownRenderer.prototype = new Error();
UnknownRenderer.prototype.constructor = UnknownRenderer;

// Define UnknownUpdateFunction exceptions definition
var UnknownUpdateFunction = function (tileType) {
    this.name = "UnknownUpdateFunction";
    this.message = "Couldn't find update function for: " + tileType;
};
UnknownUpdateFunction.prototype = new Error();

function getFlipTime(node) {
    var classStr = $(node).attr("class");
    // TODO: make this flip time CUSTOM
    var flipTime = 4200;
    $.each(classStr.split(" "), function (idx, val) {
        var groups = /flip-time-(\d+)/.exec(val);
        if (Boolean(groups) && groups.length > 1) {
            flipTime = groups[1];
            flipTime = parseInt(flipTime, 10) * 1000;
            return false;
        }
    });
    return flipTime;
}

/**
 *
 * @returns WebSocketManager
 */
function initWebsocketManager() {
    return {

        onClose: function () {
            console.log("Web socket closed. Restarting...");
            setTimeout(Tipboard.WebSocketManager.init.bind(this), 1000);
        },

        onMessage: function (evt) {
            var tileData = JSON.parse(evt.data);
            if (tileData == null) {
                console.log("Web socket received NULL data");
            } else {
                console.log("Web socket received data: ", tileData);
                var tileId = Tipboard.Dashboard.escapeId(tileData.id);
                Tipboard.Dashboard.updateTile(
                    tileId,
                    tileData.tile_template,
                    tileData.data,
                    tileData.meta,
                    tileData.modified);
                }
        },

        onError: function (evt) {
            console.log("WebSocket error: " + evt.data);
        },

        init: function () {
            console.log("Initializing a new Web socket manager.");

            var protocol = window.location.protocol === "https:" ? "wss://" : "ws://";

            var websocket = new WebSocket(protocol + window.location.host + "/communication/websocket");
            websocket.onopen = function (evt) {
                websocket.send("first_connection:" + window.location.pathname);
                console.log("Websocket: " + "first_connection:" + window.location.href)
            };
            websocket.onclose = function (evt) {
                Tipboard.WebSocketManager.onClose(evt);
            };
            websocket.onmessage = function (evt) {
                Tipboard.WebSocketManager.onMessage(evt);
            };
            websocket.onerror = function (evt) {
                Tipboard.WebSocketManager.onError(evt);
            };
        }
    };
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
        try {
        var charsToEscape = "\\!\"#$%&'()*+,./:;<=>?@[]^`{|}~";
        for (var i = 0; i < charsToEscape.length; i++) {
            var _char = charsToEscape[i];
            id = id.replace(_char, "\\" + _char);
        }
        } catch (e) {
            
        }
        return id;
    };

    Tipboard.Dashboard.setDataByKeys = function (tileId, dataToPut, keysToUse) {
        /*
        *keysToUse*: list of keys, or string 'all', if 'all' then all keys used from *dataToPut*
        */
        if (keysToUse === 'all') {
            var allKeys = [];
            for (let data in dataToPut)
                allKeys.push(data);
            keysToUse = allKeys;
        }
        var tile = Tipboard.Dashboard.id2node(tileId);
        $.each(keysToUse, function (idx, key) {
            var value = dataToPut[key];
            if (typeof (value) == 'undefined') {
                console.log('WARN: No key "' + key + '" in data', dataToPut);
            } else {
                var dstId = "#" + tileId + "-" + key;
                var dst = $(tile).find(dstId)[0];
                if (typeof dst === 'undefined') {
                    console.log('WARN: Not found node with id: ' + dstId);
                } else {
                    $(dst).text(value);
                }
            }
        });
    };

    Tipboard.Dashboard.updateTile = function (tileId, tileType, data, meta, lastMod) {
        console.log('Update tile: ', tileId);
        var tile = Tipboard.Dashboard.id2node(tileId);
        // destroy old graph
        var chartObj = Tipboard.Dashboard.chartsIds[tileId];
        if (typeof chartObj === "object") {
            Tipboard.Dashboard.chartsIds[tileId].destroy();
        }
        try {
            // its a ptr to function, calling the right update function for the right tile
            Tipboard.Dashboard.getUpdateFunction(tileType)(tileId, data, meta, tileType);
            $("#" + tileId + "-lastModified").val(lastMod);
            $.each(['.tile-content'], function (idx, klass) {
                var node = $(tile).find(klass);
                if (node.length > 1) {
                    $(node[1]).remove();
                    $(node[0]).show();
                }
            });
        } catch (err) {
            console.log('ERROR: ', tileId, err.toString());
            var msg = [
                "Tile " + tileId + " configuration error:",
                err.name || "error name: n/a",
                err.message || "error message: n/a",
            ].join('<br>');
            $.each(['.tile-content'], function (idx, klass) {
                var nodes = $(tile).find(klass);
                if (nodes.length === 1) {
                    var cloned = $(nodes).clone();
                    $(nodes).hide();
                    $(cloned).insertAfter(nodes);
                    $(cloned).addClass("exception-message");
                    $(cloned).show();
                } else {
                    $(nodes[0]).hide();
                    $(nodes[1]).show();
                }
                nodes = $(tile).find('.tile-content');
                $(nodes[1]).html(msg);
            });
        }
    };

    Tipboard.Dashboard.getUpdateFunction = function (tileType) {
        // to not duplicate js, and get separation for none tech user
        // we use same the same chartJS widget but different name
        if (tileType === 'vbar_chart')
            tileType = 'bar_chart';
        else if (tileType === 'doughnut_chart')
            tileType = 'radar_chart';
        else if (tileType === 'cumulative_flow')
            tileType = 'line_chart';

        var fn = this.updateFunctions[tileType];
        if (typeof fn !== 'function') {
            throw new Tipboard.Dashboard.UnknownUpdateFunction(tileType);
        }
        return fn;
    };

    Tipboard.Dashboard.registerUpdateFunction = function (name, fn) {
        console.log("Registering Functionetion tile:" + name);
        this.updateFunctions[name] = fn;
    };

    Tipboard.Dashboard.isTileRenderedSuccessful = function (tile) {
        var suc = $(tile).find('.exception-message').length === 0;
        return suc;
    };

    Tipboard.Dashboard.autoAddFlipClasses = function (flippingContainer) {
        $.each($(flippingContainer).find('.tile'), function (idx, elem) {
            if (idx === 0) {
                $(elem).addClass('flippedforward');
            }
            $(elem).addClass('flippable');
        });
    };

    Tipboard.Dashboard.addTilesCounter = function (col) {
        var tilesTotal = $(col).children('div.tile').length;
        if (tilesTotal > 1) {
            $.each($(col).children('div'), function (tileIdx, tile) {
               console.log("Building flip for tile");
               var container = $(tile).find('.tile-header');
                //var title = $(container).children()[0];
                $(container).addClass('flip-tile-counter');
                var counter = (tileIdx + 1) + '/' + tilesTotal;
                $(container).append(counter);
                $(container).append('<div style="clear:both"></div>');
            });
        }
    };

}

function initTilesFliping() {
    // flipping tiles
    var flipContainers = $('div[id*="flip-time-"]');
    $.each(flipContainers, function (idx, flippingContainer) {
        Tipboard.Dashboard.autoAddFlipClasses(flippingContainer);
        var flipInterval = getFlipTime(flippingContainer);
        var flipIntervalId = setInterval(function () {
            var nextFlipIdx;
            var containerFlips = $(flippingContainer).find('.flippable');
            $(containerFlips).each(function (index, tile) {
                if ($(tile).hasClass("flippedforward")) {
                    nextFlipIdx = (index + 1) % containerFlips.length;
                    $(tile).removeClass("flippedforward");
                    return false; // break
                }
            });
            if (typeof (nextFlipIdx) !== 'undefined') {
                var tileToFlip = containerFlips[nextFlipIdx];
                $(tileToFlip).addClass("flippedforward");
            }
        }, flipInterval);
        Tipboard.Dashboard.flipIds.push(flipIntervalId);
    });
}



function initTiles() {
    initTilesFliping()
    $.each($("body > div"), function (rowIdx, row) {
        // show tiles number (like: 1/3)
        $.each($(row).children('div'), function (colIdx, col) {
            Tipboard.Dashboard.addTilesCounter(col);
        });
    });
}

var addEvent = function(object, type, callback) {
    if (object == null || typeof(object) == 'undefined') return;
    if (object.addEventListener) {
        object.addEventListener(type, callback, false);
    } else if (object.attachEvent) {
        object.attachEvent("on" + type, callback);
    } else {
        object["on"+type] = callback;
    }
};

/**
 *  Main function of tipboard.js
 *  Define the Palette object used for custom color
 *  Define the WebsocketClient connection (how to update tile by websocket)
 *  Define the Dashboard object behavior (flip time, register tiles func, etc)
 *  Define the $(document).ready(function()
 */
(function ($) {
    'use strict';

    addEvent(window, "resize", function(event) {
      location.href = location.href; // location.reload(); is not working on firefox...
    });
    Tipboard.Dashboard = {
        wsSocketTimeout: 900000,
        flipIds: [],
        updateFunctions: {},
        chartsIds: {},
    };
    Tipboard.Dashboard.UnknownUpdateFunction = UnknownUpdateFunction;
    Tipboard.WebSocketManager = initWebsocketManager();
    initDashboard(Tipboard);
    Chart.defaults.global.defaultFontColor = 'rgba(255, 255, 255, 0.83)';
    $(document).ready(function () {
        console.log('Tipboard starting');
        //TODO: resize event
        Tipboard.WebSocketManager.init();
        setInterval(Tipboard.WebSocketManager.init.bind(Tipboard.WebSocketManager), Tipboard.Dashboard.wsSocketTimeout);
        initTiles()
    });
}($));

