
// Definition of the Exception UnknownRenderer
var UnknownRenderer = function (rendererName) {
    this.name = "UnknownRederer";
    this.message = "Renderer: '" + rendererName + "' not found";
};
UnknownRenderer.prototype = new Error();
UnknownRenderer.prototype.constructor = UnknownRenderer;

// Define UnknownUpdateFunction exceptions definition
var UnknownUpdateFunction = function (tileType) {
    this.name = "UnknownUpdateFunction";
    this.message = "Couldn't find update function for: " + tileType;
};
UnknownUpdateFunction.prototype = new Error();

function getFlipTime(node) {
    // TODO: make it Tipboard.Dashboard member
    var classStr = $(node).attr('class');
    var flipTime = 20000;
    $.each(classStr.split(' '), function (idx, val) {
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

        onClose: function (evt) {
            console.log("Web socket closed. Restarting...");
          //  this.websocket = void 0;
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
        var tile = $('#' + id)[0];
        return tile;
    };

    Tipboard.Dashboard.tile2id = function (tileNode) {
        return $(tileNode).attr('id');
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
            var _char = charsToEscape[i];
            id = id.replace(_char, '\\' + _char);
        }
        return id;
    };

    Tipboard.Dashboard.setDataByKeys = function (tileId, dataToPut, keysToUse) {
        /*
        *keysToUse*: list of keys, or string 'all', if 'all' then all keys used from *dataToPut*
        */
        if (keysToUse === 'all') {
            var allKeys = [];
            for (var k in dataToPut) allKeys.push(k);
            keysToUse = allKeys;
        }
        var tile = Tipboard.Dashboard.id2node(tileId);
        $.each(keysToUse, function (idx, key) {
            var value = dataToPut[key];
            if (typeof (value) === 'undefined') {
                var msg = 'WARN: No key "' + key + '" in data';
                console.log(msg, dataToPut);
            } else {
                var dstId = '#' + tileId + '-' + key;
                var dst = $(tile).find(dstId)[0];
                if (typeof dst === 'undefined') {
                    var msg = 'WARN: Not found node with id: ' + dstId;
                    console.log(msg);
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
            // Call update tile function on the right tile
            Tipboard.Dashboard.getUpdateFunction(tileType)(tileId, data, meta);
            $('#' + tileId + '-lastModified').val(lastMod);
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
                'Tile ' + tileId + ' configuration error:',
                err.name || 'error name: n/a',
                err.message || 'error message: n/a',
            ].join('<br>');
            $.each(['.tile-content'], function (idx, klass) {
                var nodes = $(tile).find(klass);
                if (nodes.length === 1) {
                    var cloned = $(nodes).clone();
                    $(nodes).hide();
                    $(cloned).insertAfter(nodes);
                    $(cloned).addClass('exception-message');
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
                var title = $(container).children()[0];
                $(container).addClass('flip-tile-counter');
                var counter = (tileIdx + 1) + '/' + tilesTotal;
                $(container).append(counter);
                $(container).append('<div style="clear:both"></div>');
            });
        }
    };

}



/**
 *  Main function of tipboard.js
 *  Define the Palette object used for custom color
 *  Define the WebsocketClient connection (how to update tile by websocket)
 *  Define the Dashboard object behavior (flip time, register tiles func, etc)
 *  Define the $(document).ready(function()
 */
(function ($) {
    'use strict';

    if (!window.console) {// wtf is that ?
        window.console = {
            log: function () {
            }
        };
    }

    window.Tipboard = {};
    Tipboard.Dashboard = {
        webSocketResetInterval: 900000,
        flipIds: [],
        updateFunctions: {},
        chartsIds: {},
    };
    Tipboard.Dashboard.UnknownUpdateFunction = UnknownUpdateFunction;
    Tipboard.WebSocketManager = initWebsocketManager();
    initDashboard(Tipboard);

    $(document).ready(function () {
        console.log('Tipboard starting');
        //TODO: resize event
        Tipboard.WebSocketManager.init();
        setInterval(Tipboard.WebSocketManager.init.bind(Tipboard.WebSocketManager),
            Tipboard.Dashboard.webSocketResetInterval);
        // flipping tiles
        var flipContainers = $('div[id*="flip-time-"]');
        $.each(flipContainers, function (idx, flippingContainer) {
            Tipboard.Dashboard.autoAddFlipClasses(flippingContainer);
            var flipInterval = getFlipTime(flippingContainer);
            var flipIntervalId = setInterval(function () {
                /*
                 * pass class *flippedforward* to next node with class
                 * *flippable* within *container*, if last element then wrap it
                 * and pass *flippedforward* to the first element with class
                 * *flippable* within the *container*
                 */
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
        $.each($("body > div"), function (rowIdx, row) {
            // show tiles number (like: 1/3)
            $.each($(row).children('div'), function (colIdx, col) {
                Tipboard.Dashboard.addTilesCounter(col);
            });
        });
    });
}($));

