/*jslint browser: true, devel: true, evil: true*/
/*global WebSocket: false, Tipboard: false*/

function RendererFactory() { }
RendererFactory.prototype.rendererName2renderObj = {
    // core renderer
    "axistickrenderer": $.jqplot.AxisTickRenderer,
    "canvasgridrenderer": $.jqplot.CanvasGridRenderer,
    "divtitlerenderer": $.jqplot.DivTitleRenderer,
    "linearaxisrenderer": $.jqplot.LinearAxisRenderer,
    "markerrenderer": $.jqplot.MarkerRenderer,
    "shaperenderer": $.jqplot.ShapeRenderer,
    "shadowrenderer": $.jqplot.ShadowRenderer,
    "linerenderer": $.jqplot.LineRenderer,
    "axislabelrenderer": $.jqplot.AxisLabelRenderer,
    // plugins
    "barrenderer": $.jqplot.BarRenderer,
    "blockrenderer": $.jqplot.BlockRenderer,
    "bubblerenderer": $.jqplot.BubbleRenderer,
    "canvasaxislabelrenderer": $.jqplot.CanvasAxisLabelRenderer,
    "canvasaxistickrenderer": $.jqplot.CanvasAxisTickRenderer,
    "categoryaxisrenderer": $.jqplot.CategoryAxisRenderer,
    "dateaxisrenderer": $.jqplot.DateAxisRenderer,
    "donutrenderer": $.jqplot.DonutRenderer,
    "enhancedlegendrenderer": $.jqplot.EnhancedLegendRenderer,
    "funnelrenderer": $.jqplot.FunnelRenderer,
    "logaxisrenderer": $.jqplot.LogAxisRenderer,
    "mekkoaxisrenderer": $.jqplot.MekkoAxisRenderer,
    "mekkorenderer": $.jqplot.MekkoRenderer,
    "metergaugerenderer": $.jqplot.MeterGaugeRenderer,
    "ohlcrenderer": $.jqplot.OHLCRenderer,
    "pierenderer": $.jqplot.PieRenderer,
    // others
    "canvastextrenderer": $.jqplot.CanvasTextRenderer,
    "donutlegendrenderer": $.jqplot.DonutLegendRenderer,
    "pyramidaxisrenderer": $.jqplot.PyramidAxisRenderer,
    "pyramidgridrenderer": $.jqplot.PyramidGridRenderer,
    "pyramidrenderer": $.jqplot.PyramidRenderer
};
RendererFactory.prototype.createRenderer = function (rendererName) {
    var lower = rendererName.toLowerCase();
    var rendererClass = RendererFactory.prototype.rendererName2renderObj[lower];
    if (typeof(rendererClass) === 'undefined') {
        throw new RendererFactory.prototype.UnknownRenderer(rendererName);
    }
    return rendererClass;
};
var UnknownRenderer = function (rendererName) {
    this.name = "UnknownRederer";
    this.message = "Renderer: '" + rendererName + "' not found";
};
UnknownRenderer.prototype = new Error();
UnknownRenderer.prototype.constructor = UnknownRenderer;
RendererFactory.prototype.UnknownRenderer = UnknownRenderer;

function RenderersSwapper() { }
RenderersSwapper.prototype.insertRendererClasses = function(obj, keys) {
    $.each(keys, function (idx, key) {
        var rendererName, rendererClass;
        rendererName = null;
        try {
            rendererName = obj[key];
        } catch (err) {
            console.log('skipped', key);
        }
        if (typeof rendererName === "string") {
            rendererClass = RendererFactory.prototype.createRenderer(rendererName);
            obj[key] = rendererClass;
        }
    });
    return obj;
};

RenderersSwapper.prototype.swap = function (config) {
    /*
    jqplot config gets renderers under these paths:
    simple:
        config.legend.renderer
        config.title.renderer
        config.grid.renderer
        config.axesDefaults.<axisRenderer>
        config.seriesDefaults.<seriesRenderer>
    nested:
        config.axes.<axis>.<axisRenderer>
        <axis> can be these keys:
            xaxis, x2axis, yaxis, y2axis, .. , y9axis
        config.series.<series>.<seriesRenderer>
            <series>: array

    <axisRenderer> can be these keys:
        - tickRenderer, labelRenderer, renderer
    <seriesRenderer> can be these keys:
        - markerRenderer, renderer
    */
    var simple, complex;
    simple = {
        'legend': ['renderer'],
        'title': ['renderer'],
        'grid': ['renderer'],
        'axesDefaults': ["tickRenderer", "labelRenderer", "renderer"],
        'seriesDefaults': ["markerRenderer", "renderer"]
    };
    $.each(simple, function (key, rendererTypes) {
        if (config[key]) {
            config[key] = RenderersSwapper.prototype.insertRendererClasses(
              config[key], rendererTypes
            );
        }
    });
    complex = {
        'axes': simple.axesDefaults,
        'series': simple.seriesDefaults
    };
    $.each(complex, function (key, rendererTypes) {
        if (config[key]) {
            $.each(config[key], function (subkey, values) {
                config[key][subkey] = RenderersSwapper.prototype.insertRendererClasses(
                  config[key][subkey], rendererTypes
                );
            });
        }
    });
    return config;
};

function getFlipTime(node) {
    // TODO: make it Tipboard.Dashboard member
    var classStr = $(node).attr('class');
    var flipTime = 20000;
    $.each(classStr.split(' '), function(idx, val) {
        var groups = /flip-time-(\d+)/.exec(val);
        if (Boolean(groups) && groups.length > 1) {
            flipTime = groups[1];
            flipTime = parseInt(flipTime, 10) * 1000;
            return false;
        }
    });
    return flipTime;
}

function verboseLog(level, msg) {
    /*
    This function is: DEPRECATED.

    Available levels:
    1: silent
    2: debug
    */
    var threshold = 1;
    if (level > threshold) {
        console.log(msg);
    }
}

var renderersSwapper = new RenderersSwapper();

(function($) {
    'use strict';

    if (!window.console) {
        window.console = {
            log: function() {}
        };
    }

    window.Tipboard = {};

    Tipboard.DisplayUtils = {

        pallet: {
            'black':            '#000000',
            'white':            '#FFFFFF',
            'tile_background':  '#25282d',
            'red':              '#DC5945',
            'yellow':           '#FF9618',
            'green':            '#94C140',
            'blue':             '#12B0C5',
            'violet':           '#9C4274',
            'orange':           '#EC663C',
            'naval':            '#54C5C0',
        },

        getPalette: function(colors) {
            // DEPRECATED, use paletteAsList instead
            var palette = [];
            $.each(colors, function(name) {
                if (['black', 'white', 'tile_background'].indexOf(name) < 0) {
                    palette.push(colors[name]);
                }
            });
            return palette;
        },

        paletteAsList: function() {
            var paletteList = [];
            $.each(Tipboard.DisplayUtils.palette, function(name, value) {
                if (['black', 'white', 'tile_background'].indexOf(name) < 0) {
                    paletteList.push(value);
                }
            });
            return paletteList;
        },

        replaceFromPalette: function(color) {
            $.each(this.palette, function(colorName, colorValue) {
                if (color === colorName) {
                    color = colorValue;
                    return false;
                }
            });
            return color;
        },

        paletteAsSeriesColors: function() {
          var seriesColors = [];
          $.each(
              Tipboard.DisplayUtils.getPalette(Tipboard.DisplayUtils.palette),
              function(idx, color) {
                  seriesColors.push({'color': color});
              }
          );
          return seriesColors;
        },

        expandLastChild: function(container) {
            /*
            Autogrow height of node *body* in *container* node respecting of *header*
            height.

            container:
                item1
                [..]
                itemLast
            */
            var siblingsHeight = 0;
            var len = $(container).children().length;
            $.each($(container).children(), function(index, element) {
                if (index == len - 1) {
                    return false;
                }
                siblingsHeight += $(element).outerHeight(true);
            });
            if (len - 1 < 0) {
                console.log('expanding stopped - container has no elements');
                return false;
            }
            var body = $(container).children()[len - 1];
            var border = $(body).outerHeight(true) - $(body).height();
            var bodyHeight = $(container).height() - siblingsHeight - border;
            $(body).height(bodyHeight);
        },

        showTileData: function (tile) {
          $.each(['.tile-content'], function(idx, klass) {
            var node = $(tile).find(klass);
            if (node.length > 1) {
              $(node[1]).remove();
              $(node[0]).show();
            }
          });
        },
        showExcMsg: function (tile, msg) {
          $.each(['.tile-content'], function(idx, klass) {
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
        },

        createGraph: function (tileId, plotData, config) {
            var containerId, plot;
            containerId = tileId + '-chart';
            plot = $.jqplot(containerId, plotData, config);
            Tipboard.Dashboard.chartsIds[tileId] = plot;
        },

        rescaleTile: function (tile) {
            /* <tile>: DOM element representing tile */
            Tipboard.DisplayUtils.expandLastChild(tile);
            Tipboard.DisplayUtils.expandLastChild($(tile).find('.tile-content')[0]);
        },

        applyHighlighterConfig: function (highlighterNode, color, fading) {
            if (typeof color === "undefined" && typeof fading === "undefined") {
                // clear settings
                $(highlighterNode).css('background-color', 'rgba(0, 0, 0, 0)');
                highlighterNode.removeClass('fading-background-color');
            } else {
                if (typeof color === "undefined") {
                    color = $(highlighterNode).css('background-color', color);
                }
                color = Tipboard.DisplayUtils.replaceFromPalette(color);
                $(highlighterNode).css('background-color', color);

                if (fading === true) {
                    highlighterNode.addClass('fading-background-color');
                }
                if (fading === false) {
                    highlighterNode.removeClass('fading-background-color');
                }
            }
            highlighterNode.before(highlighterNode.clone(true)).remove();
        },

        highlightAsOk: function(element) {
            $(element).addClass('highlighted-green');
            $(element).removeClass('highlighted-red');
        },

        highlightAsFail: function(element) {
            $(element).removeClass('highlighted-green');
            $(element).addClass('highlighted-red');
        },

        arrowUp: function(element) {
            $(element).addClass('arrow-up');
            $(element).removeClass('arrow-down');
        },

        arrowDown: function(element) {
            $(element).removeClass('arrow-up');
            $(element).addClass('arrow-down');
        },

        changeFontSize: function() {
            var windowHeight = $(window).height();
            if (windowHeight > $(window).width()) {
                windowHeight = $(window).width();
            }
            if (windowHeight <= 768) {
                return;
            }
            var newFontSize = Math.max(Math.floor(12 * windowHeight / 768) + 1, 12);
            $('body').css({
                'font-size': newFontSize
            });
            console.log('Changed font size to ' + newFontSize + '.');
        },

        makeTilesMargins: function() {
            console.log('Updating tile sizes.');
            $('.tile').each(function() {
                var tileWidth = $(this).parent().width() - 20;
                var tileHeight = $(this).parent().height() - 20;
                $(this).css({
                    'width': tileWidth,
                    'height': tileHeight,
                    'top': 10,
                    'left': 10
                });
            });
        },

        changeChartsSize: function() {
            console.log('Updating chart sizes.');
            $('.chart').each(function() {
                var tileHeaderHeight = $(this).parents('.tile').find('.tile-header').height();
                var tileContentHeight = 32;

                function increaseContentHeight() {
                    if ($(this).hasClass('small-padding')) {
                        tileContentHeight += $(this).height() * 1.5;
                    } else {
                        tileContentHeight += $(this).height();
                    }
                }
                if (!$(this).hasClass('chart-only')) {
                    $(this).parents('.tile').find('.tile-content .result').each(increaseContentHeight);
                    $(this).parents('.tile').find('.tile-content h2').each(increaseContentHeight);
                }
                var chartHeight = $(this).parents('.tile').height() - tileHeaderHeight - tileContentHeight;
                $(this).css({
                    height: chartHeight
                });
                // replot
                var tileId = $(this).parents('div.tile').attr('id');
                var plot = Tipboard.Dashboard.chartsIds[tileId];
                if (Boolean(plot)) {
                    plot.replot( { resetAxes: true } );
                }
            });
        },

        resizeWindowEvent: function() {
            this.makeTilesMargins();
            this.changeFontSize();
            this.changeChartsSize();
        },

        flipFlippablesIn: function(container) {
            /*
             * pass class *flippedforward* to next node with class
             * *flippable* within *container*, if last element then wrap it
             * and pass *flippedforward* to the first element with class
             * *flippable* within the *container*
             */
            var nextFlipIdx;
            var containerFlips = $(container).find('.flippable');
            $(containerFlips).each(function(index, tile) {
                if ($(tile).hasClass("flippedforward")) {
                    nextFlipIdx = (index + 1) % containerFlips.length;
                    $(tile).removeClass("flippedforward");
                    return false; // break
                }
            });
            if (typeof(nextFlipIdx) !== 'undefined') {
                var tileToFlip = containerFlips[nextFlipIdx];
                $(tileToFlip).addClass("flippedforward");
            }
        },

        reloadPage: function() {
            var http = new XMLHttpRequest();
            http.open('HEAD', window.location.href);
            http.onreadystatechange = function() {
                if (this.readyState === this.DONE && this.status === 200) {
                    window.location.reload();
                }
            };
            http.send();
        }
    };

    Tipboard.TileDisplayDecorator = {
        fitTile: function(tile) {
            Tipboard.DisplayUtils.expandLastChild(tile);
        },
        highlightResult: function(tile) {
            $(tile).find('.highlighted-result [data-source-key]').each(function() {
                var elementValue = parseInt($(this).html(), 10);
                var parentContainer = $(this).parent('.highlighted-result');
                var threshold = $(this).attr('data-threshold');
                var isOK = false;
                var thresholdFloat = parseFloat(threshold, 10);
                if (!isNaN(thresholdFloat)) {
                    isOK = elementValue > thresholdFloat;
                } else {
                    try {
                        isOK = eval(threshold);
                    } catch (TypeError) {
                        isOK = elementValue > 50;
                    }
                }
                if (isOK) {
                    Tipboard.DisplayUtils.highlightAsOk(parentContainer);
                } else {
                    Tipboard.DisplayUtils.highlightAsFail(parentContainer);
                }
            });
        },

        drawArrow: function(tile) {
            $(tile).find('.with-arrow-result [data-source-key]').each(function() {
                var elementValue = parseInt($(this).html(), 10);
                var parentContainer = $(this).parent('.with-arrow-result');
                var arrowContainer = $(parentContainer).find('span.arrow');
                if (elementValue < 0) {
                    Tipboard.DisplayUtils.arrowDown(arrowContainer);
                } else {
                    Tipboard.DisplayUtils.arrowUp(arrowContainer);
                }
            });
        },

        runAllDecorators: function(tile) {
            var item = void 0;
            for (item in Tipboard.TileDisplayDecorator) {
                if (typeof Tipboard.TileDisplayDecorator[item] === "function" && item !== "runAllDecorators") {
                    Tipboard.TileDisplayDecorator[item](tile);
                }
            }
        }
    };

    Tipboard.WebSocketManager = {
        onOpen: function(evt) {
            console.log("Web socket opened.");
            this.websocket.send("update");
        },

        onClose: function(evt) {
            console.log("Web socket closed. Restarting...");
            this.websocket = void 0;
            setTimeout(Tipboard.WebSocketManager.init.bind(this), 1000);
        },

        onMessage: function(evt) {
            var tileData = JSON.parse(evt.data);
            console.log("Web socket received data: ", tileData);
            // FIXME: pass colors in more suitable place
            Tipboard.DisplayUtils.palette = $.extend(
                true, this.palette, tileData.tipboard.color
            );
            var tileId = Tipboard.Dashboard.escapeId(tileData.id);
            Tipboard.Dashboard.updateTile(
                tileId,
                tileData.tile_template,
                tileData.data,
                tileData.meta,
                tileData.tipboard,
                tileData.modified
            );
        },

        onError: function(evt) {
            console.log("WebSocket error: " + evt.data);
        },

        init: function() {
            if ((typeof(this.websocket) !== 'undefined') && !(this.websocket.readyState === WebSocket.CLOSED || this.websocket.readyState === WebSocket.CLOSING)) {
                console.log("Closing outdated Web socket.");
                this.websocket.close();
                return; // the rest will be handled in onClose()
            }
            console.log("Initializing a new Web socket manager.");

            var protocol = window.location.protocol === "https:" ? "wss://" : "ws://";

            this.websocket = new WebSocket(
                protocol + window.location.host + "/communication/websocket"
            );
            this.websocket.onopen = function(evt) {
                Tipboard.WebSocketManager.onOpen(evt);
            };
            this.websocket.onclose = function(evt) {
                Tipboard.WebSocketManager.onClose(evt);
            };
            this.websocket.onmessage = function(evt) {
                Tipboard.WebSocketManager.onMessage(evt);
            };
            this.websocket.onerror = function(evt) {
                Tipboard.WebSocketManager.onError(evt);
            };
        }
    };

    Tipboard.Dashboard = {
        webSocketResetInterval: 900000,
        flipIds: [],
        updateFunctions: {},
        chartsIds: {},
    };

    // exceptions definition
    var TimeoutBadFormat = function (timeout) {
        this.name = "TimeoutBadFormat";
        this.message = "Timeout consists non-digits: '" + timeout + "'";
    };
    TimeoutBadFormat.prototype = new Error();
    TimeoutBadFormat.prototype.constructor = TimeoutBadFormat;
    Tipboard.Dashboard.TimeoutBadFormat = TimeoutBadFormat;

    var UnknownUpdateFunction = function (tileType) {
        this.name = "UnknownUpdateFunction";
        this.message = "Couldn't find update function for: " + tileType;
    };
    UnknownUpdateFunction.prototype = new Error();
    UnknownUpdateFunction.prototype.constructor = UnknownUpdateFunction;
    Tipboard.Dashboard.UnknownUpdateFunction = UnknownUpdateFunction;

    Tipboard.Dashboard.id2node = function(id) {
        var tile = $('#' + id)[0];
        return tile;
    };

    Tipboard.Dashboard.tile2id = function(tileNode) {
        return $(tileNode).attr('id');
    };

    Tipboard.Dashboard.escapeId = function(id) {
        /*
        the Tipboard application allows user to use eg. '.' in tiles' ids
        jquery requires such chars to be escaped
        */
        // XXX: backslash MUST BE FIRST, otherwise this convertions is
        // broken (escaping chars which meant to be escapers)
        var charsToEscape = "\\!\"#$%&'()*+,./:;<=>?@[]^`{|}~";
        for(var i=0; i<charsToEscape.length; i++) {
            var _char = charsToEscape[i];
            id = id.replace(_char, '\\' + _char);
        }
        return id;
    };

    Tipboard.Dashboard.setDataByKeys = function(
        tileId, dataToPut, keysToUse
    ) {
        /*
        *keysToUse*: list of keys, or string 'all', if 'all' then all keys
            used from *dataToPut*
        */
        if (keysToUse === 'all') {
            var allKeys = [];
            for(var k in dataToPut) allKeys.push(k);
            keysToUse = allKeys;
        }
        var tile = Tipboard.Dashboard.id2node(tileId);
        $.each(keysToUse, function(idx, key) {
            var value = dataToPut[key];
            if (typeof(value) === 'undefined') {
                var msg = 'WARN: No key "' + key + '" in data'
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

    Tipboard.Dashboard.updateTile = function(
        tileId, tileType, data, meta, tipboard, lastMod
    ) {
        console.log('Update tile: ', tileId);
        var tile = Tipboard.Dashboard.id2node(tileId);
        // destroy old graph
        var chartObj = Tipboard.Dashboard.chartsIds[tileId];
        if (typeof chartObj === "object") {
            Tipboard.Dashboard.chartsIds[tileId].destroy();
        }
        try {
            var fn = Tipboard.Dashboard.getUpdateFunction(tileType);
            fn(tileId, data, meta, tipboard);
            $('#' + tileId + '-lastModified').val(lastMod);
            Tipboard.DisplayUtils.showTileData(tile);
        } catch (err) {
            console.log('ERROR: ', tileId, err);
            var msg = [
                'Tile ' + tileId + ' configuration error:',
                err.name || 'error name: n/a',
                err.message || 'error message: n/a',
            ].join('<br>');
            Tipboard.DisplayUtils.showExcMsg(tile, msg);
        }
    };

    Tipboard.Dashboard.getUpdateFunction = function(tileType) {
        var fn = this.updateFunctions[tileType];
        if (typeof fn !== 'function') {
            throw new Tipboard.Dashboard.UnknownUpdateFunction(tileType);
        }
        return fn;
    };

    Tipboard.Dashboard.registerUpdateFunction = function(name, fn) {
        this.updateFunctions[name] = fn;
    };

    Tipboard.Dashboard.isTileRenderedSuccessful = function(tile) {
        var suc = $(tile).find('.exception-message').length === 0 ? true : false;
        return suc;
    };

    Tipboard.Dashboard.isValidDatetimeFormat = function(dateString) {
        // valid dateString should be in ISO-8601 format, e.g.:
        // "2014-01-10T15:27:34+02:00"
        var regex = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$/;
        var valid = regex.test(dateString);
        return valid;
    };

    Tipboard.Dashboard.isDataExpired = function(lastMod, timeout) {
        var reason = "";
        if (timeout === "") {
            // backward compability, no timeout then skip checking
            return;
        }
        if (!/^\d+$/.test(timeout)) {
            throw new Tipboard.Dashboard.TimeoutBadFormat(timeout);
        }
        if (lastMod === "") {
            reason = [
                'Could not find the timestamp.',
                '(maybe your data is stalled?)'
            ].join('<br>');
        } else {
            if (Tipboard.Dashboard.isValidDatetimeFormat(lastMod)) {
                var now = new Date();
                var lastDateTime = new Date(lastMod);
                var dataAge = (now - lastDateTime)/1000;  // dataAge is in seconds
                if (dataAge >= timeout) {
                    reason = "Tile's data EXPIRED.";
                }
            } else {
                reason = [
                    'Timestamp found has bad format.',
                    'found: ' + lastMod,
                    'vs.',
                    'expected: "yyyy-mm-dd hh:mm:ss"',
                ].join('<br>');
            }
        }
        return reason;
    };

    Tipboard.Dashboard.autoAddFlipClasses = function(flippingContainer) {
        $.each($(flippingContainer).find('.tile'), function(idx, elem) {
            if (idx === 0) {
                $(elem).addClass('flippedforward');
            }
            $(elem).addClass('flippable');
        });
    };

    Tipboard.Dashboard.addTilesCounter = function(col) {
        var tilesTotal = $(col).children('div.tile').length;
        if (tilesTotal > 1) {
            $.each($(col).children('div'), function(tileIdx, tile) {
                var container = $(tile).find('.tile-header');
                var title = $(container).children()[0];
                $(title).addClass('flip-tile-counter');
                var counter = (tileIdx + 1) + '/' + tilesTotal;
                $(container).append('<span class="tile-counter">' + counter + '</span>');
                $(container).append('<div style="clear:both"></div>');
            });
        }
    };

    $(document).ready(function() {
        $.jqplot.config.enablePlugins = true;
        // resize events
        $(window).bind("resize fullscreen-off", function() {
            Tipboard.DisplayUtils.resizeWindowEvent();
        });
        // websocket management
        Tipboard.WebSocketManager.init();
        setInterval(
            Tipboard.WebSocketManager.init.bind(Tipboard.WebSocketManager),
            Tipboard.Dashboard.webSocketResetInterval
        );
        // flipping tiles
        var flipContainers = $('div[class*="flip-time-"]');
        $.each(flipContainers, function(idx, flippingContainer) {
            Tipboard.Dashboard.autoAddFlipClasses(flippingContainer);
            var flipInterval = getFlipTime(flippingContainer);
            var flipIntervalId = setInterval(function() {
                Tipboard.DisplayUtils.flipFlippablesIn(flippingContainer);
            }, flipInterval);
            Tipboard.Dashboard.flipIds.push(flipIntervalId);
        });
        $.each($("body > div"), function(rowIdx, row) {
            // show tiles number (like: 1/3)
            $.each($(row).children('div'), function(colIdx, col) {
                Tipboard.Dashboard.addTilesCounter(col);
            });
        });
        // watchdog
        setInterval(Tipboard.DisplayUtils.reloadPage, 3600000);

        // check if all tiles have fresh data
        setInterval(function() {
            var tiles = $('.tile');
            $.each(tiles, function(idx, tile) {
                if (Tipboard.Dashboard.isTileRenderedSuccessful(tile)) {
                    var tileId = Tipboard.Dashboard.tile2id(tile);
                    var lastMod = $('#' + tileId + '-lastModified').val();
                    var timeout = $('#' + tileId + '-timeout').val();
                    var reason = Tipboard.Dashboard.isDataExpired(
                        lastMod, timeout
                    );
                    if (reason) {
                        Tipboard.DisplayUtils.showExcMsg(tile, reason);
                    } else {
                        Tipboard.DisplayUtils.showTileData(tile);
                    }
                }
            });
        }, 5000);
        Tipboard.DisplayUtils.resizeWindowEvent();
    });
}($));
