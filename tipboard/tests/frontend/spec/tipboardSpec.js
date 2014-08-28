describe("Tipboard flip-tile mechanism", function() {
    var getFlipTimeNodes = function() {
        var flipTimeNodes = $('body > div:first-child > div');
        return flipTimeNodes;
    };

    it("finds flip-time correctly", function() {
        var expectedTimes = [3, 5, 20];
        var flippingConatainers = getFlipTimeNodes();
        $.each(expectedTimes, function(idx, expectedTime) {
            var flippingContainer = flippingConatainers[idx];
            console.log('flippingContainer', flippingContainer);
            var foundTime = getFlipTime(flippingContainer);
            expect(foundTime).toBe(expectedTime*1000);
        });
    });

    it("adds classes (flippedforward, flipped) automatically", function() {
        var flipTimeNodes = getFlipTimeNodes();
        var noFlipNode = flipTimeNodes.splice(2,1);
        expect(flipTimeNodes.length).toBe(3);
        expect(noFlipNode.length).toBe(1);
        expect($(noFlipNode[0]).hasClass('flippedforward')).toBe(false);
        expect($(noFlipNode[0]).hasClass('flippable')).toBe(false);

        console.log('flipTimeNodes', flipTimeNodes);
        $.each(flipTimeNodes, function(idx, flipContainer) {
            var containedTiles = $(flipContainer).find('div.tile');
            expect(containedTiles.length).toBe(2);

            $.each(containedTiles, function(tileIdx, tile) {
                console.log('tile', tile);
                if (tileIdx === 0) {
                    expect($(tile).hasClass('flippedforward')).toBe(true);
                    expect($(tile).hasClass('flippable')).toBe(true);
                } else {
                    expect($(tile).hasClass('flippedforward')).toBe(false);
                    expect($(tile).hasClass('flippable')).toBe(true);
                }
            });
        });
    });

    it("appends correct tiles counter", function() {
        var flipTimeNodes = getFlipTimeNodes();
        var noFlipNode = flipTimeNodes.splice(2,1);
        Tipboard.Dashboard.addTilesCounter(noFlipNode);
        expect(
            $(noFlipNode).find('span.tile-counter').length
        ).toBe(0);

        $.each(flipTimeNodes, function(idx, flipContainer) {
            var containedTiles = $(flipContainer).find('div.tile');
            $.each(containedTiles, function(tileIdx, tile) {
                console.log('tile-couter tile check', tile);
                var counterSpans = $(tile).find('span.tile-counter');
                expect(counterSpans.length).toBe(1);
                var expected = [tileIdx + 1, containedTiles.length].join('/');
                var foundText = $(counterSpans[0]).text();
                expect(foundText).toBe(expected);
            });
        });
    });

});

describe("Tipboard RenderersSwapper", function() {

    var aRendererClass = $.jqplot.AxisTickRenderer;
    var aRendererClassName = "AXISTICKRENDERER";

    var getObjectAtPath = function(object, path) {
        path = path.replace(/\[(\w+)\]/g, '.$1'); // convert indexes to properties
        path = path.replace(/^\./, '');           // strip a leading dot
        var steps = path.split('.');
        while (steps.length) {
            var step = steps.shift();
            if (step in object) {
                object = object[step];
            } else {
                return;
            }
        }
        return object;
    };

    var configWithRendererOnPossiblePaths = function(renderer) {
        var simpleRenderer = {renderer: renderer};
        var axisWithRenderer = {
            tickRenderer: renderer,
            labelRenderer: renderer,
            renderer: renderer
        };
        var seriesWithRenderer = {
            markerRenderer: renderer,
            renderer: renderer
        };
        var config = {
            'legend': simpleRenderer,
            'title': simpleRenderer,
            'grid': simpleRenderer,
            'axesDefaults': axisWithRenderer,
            'axes': {
                'xaxis': axisWithRenderer,
                'x2axis': axisWithRenderer,
                'yaxis': axisWithRenderer,
                'y2axis': axisWithRenderer,
                // ..
                'y9axis': axisWithRenderer,
            },
            'seriesDefaults': seriesWithRenderer,
            'series': [
                seriesWithRenderer,
                seriesWithRenderer
                //..
            ]
        };
        return config;
    };

    it("has correct references to renderer classes", function() {
        $.each(
            RendererFactory.prototype.rendererName2renderObj,
            function(rendererName, rendererClass) {
                var rendererClassType = typeof rendererClass;
                expect(rendererClassType).toBe("function");
            }
        );
    });

    it("replaces renderer case insensitively", function() {
        var config = {
            'title': {
                'renderer': aRendererClassName
            }
        };
        renderersSwapper.swap(config);
        expect(config.title.renderer).toBe(aRendererClass);
    });

    it("replaces all defined renderers", function() {
        var config = {
            'title': {
                'renderer': undefined,
            }
        };
        var allRenderers = RendererFactory.prototype.rendererName2renderObj;
        $.each(allRenderers, function(rendererName, rendererClass) {
            config.title.renderer = rendererName;
            renderersSwapper.swap(config);
            expect(config.title.renderer).toBe(rendererClass);
        });
    });

    it("replaces renderers on every possible path", function() {
        var goodConfig = configWithRendererOnPossiblePaths(
            aRendererClass
        );
        goodConfig = JSON.stringify(goodConfig);

        var configToSwap = configWithRendererOnPossiblePaths(
            aRendererClassName
        );
        renderersSwapper.swap(configToSwap);
        var swappedConfig = JSON.stringify(configToSwap);
        expect(swappedConfig).toBe(goodConfig);
    });

    it("raises error on undefined renderer name", function() {
        var invalidRendererName = "invalidRendererName";
        var configToSwap = configWithRendererOnPossiblePaths(
            invalidRendererName
        );
        expect(
            renderersSwapper.swap.bind(null, configToSwap)
        ).toThrow(
            new RendererFactory.prototype.UnknownRenderer(invalidRendererName)
        );
    });

});

describe("Tipboard palette functions", function() {

    it("return palette as non-empty list", function() {
        var paletteAsList = Tipboard.DisplayUtils.paletteAsList();
        expect(paletteAsList.length).toBeGreaterThan(0);
        var paletteType = Object.prototype.toString.call(paletteAsList);
        expect(paletteType).toBe("[object Array]");
    });

    it("return the same color when color is not from palette", function() {
        var notpaletteColors = ['#123456', 'pink', ''];
        $.each(notpaletteColors, function(idx, rightColor) {
            testingColor = Tipboard.DisplayUtils.replaceFromPalette(
                rightColor
            );
            expect(testingColor).toBe(rightColor);
        });
    });

    it("return the palette color when color is from palette", function() {
        $.each(Tipboard.DisplayUtils.palette, function(colorName, goodColor) {
            var testingColor = Tipboard.DisplayUtils.replaceFromPalette(
                colorName
            );
            expect(testingColor).toBe(goodColor);
        });
    });

    it("return palette for jqplot seriesColor", function() {
        var seriesColors = Tipboard.DisplayUtils.paletteAsSeriesColors();
        expect(seriesColors.length).toBeGreaterThan(0);
        var seriesColorsType = Object.prototype.toString.call(seriesColors);
        expect(seriesColorsType).toBe("[object Array]");
        var childType = Object.prototype.toString.call(seriesColors[0]);
        expect(childType).toBe("[object Object]");
    });
});

describe("Tipboard isDataExpired function", function() {

    describe("works correctly when arg", function() {

        describe("lastMod is", function() {

            _date2format = function(datetime) {
                // toISOString returns UTC time, hence we need to convert it
                // to user's timezone, e.g. "2014-01-10T15:27:34+02:00"
                var date = datetime.toISOString().split('T')[0];
                var time = datetime.toTimeString().split(' ')[0];
                var tz = datetime.toTimeString().split(' ')[1].slice(-5);
                tz = [tz.slice(0, 3), tz.slice(3)].join(':');
                var formatted = [date, [time, tz].join('')].join('T');
                return formatted;
            };

            it("empty string", function() {
                var lastMod = "";
                var timeout = 5;
                var reason = Tipboard.Dashboard.isDataExpired(
                    lastMod, timeout
                );
                expect(reason).toMatch(/Could not find the timestamp./);
            });

            it("invalid format", function() {
                var lastMod = new Date();
                lastMod = 'fadfasdfdas';
                var timeout = 5;
                var reason = Tipboard.Dashboard.isDataExpired(
                    lastMod, timeout
                );
                expect(reason).toMatch(/Timestamp found has bad format./);
            });

            it("expired", function(){
                var lastMod = new Date();
                lastMod.setYear(lastMod.getYear() - 1);
                lastMod = _date2format(lastMod);
                var timeout = 10;
                var reason = Tipboard.Dashboard.isDataExpired(
                    lastMod, timeout
                );
                expect(reason).toMatch(/Tile's data EXPIRED./);
            });

            it("not expired", function() {
                var lastMod = new Date();
                lastMod = _date2format(lastMod);
                var timeout = 1000;
                var reason = Tipboard.Dashboard.isDataExpired(
                    lastMod, timeout
                );
                expect(reason).toBe("");
            });

        });

        describe("timout", function() {

            it("is empty string", function() {
                var lastMod = new Date();
                var timeout = "";
                var reason = Tipboard.Dashboard.isDataExpired(
                    lastMod, timeout
                );
                expect(reason).toBe(undefined);
            });

            it("contains non-digit", function() {
                var lastMod = new Date();
                var timeout = "5a";
                expect(
                    Tipboard.Dashboard.isDataExpired.bind(null, lastMod, timeout)
                ).toThrow(
                    new Tipboard.Dashboard.TimeoutBadFormat(timeout)
                );
            });
        });
    });

});

describe("Tipboard show-error mechanism", function() {

    var getFirstTile = function() {
        // XXX: html dom is not visible on *describe* level, so call it on
        // each *it* as a function (then html dom is visible)
        return $('.tile')[0];
    };

    var checkIfTileIsShown = function(tile) {
        var tileHeader = tile.children[0];
        console.log('tile.children', tile.children);
        expect(tile.children.length).toBe(2);
        var msgContainer = $(tile).children()[1];
        var isError = $(msgContainer).hasClass('exception-message');
        expect(isError).toBe(false);
        var display = $(msgContainer).css('display');
        expect(display).not.toBe('none');
    };

    var checkIfErrorIsShown = function(tile) {
        var tileHeader = tile.children[0];
        console.log('tile.children', tile.children);
        expect(tile.children.length).toBe(3);

        var msgContainer = $(tile).children()[1];
        var isError = $(msgContainer).hasClass('exception-message');
        expect(isError).toBe(false);
        var display = $(msgContainer).css('display');
        expect(display).toBe('none');

        var errorContainer = $(tile).children()[2];
        isError = $(errorContainer).hasClass('exception-message');
        expect(isError).toBe(true);
        display = $(errorContainer).css('display');
        expect(display).not.toBe('none');
    };

    it("change tile to tile", function() {
        var tile = getFirstTile();
        Tipboard.DisplayUtils.showTileData(tile);
        checkIfTileIsShown(tile);
    });

    it("change tile to error", function() {
        var tile = getFirstTile();
        Tipboard.DisplayUtils.showExcMsg(tile, "aMessage");
        checkIfErrorIsShown(tile);
    });

    it("change error to error", function() {
        var tile = getFirstTile();
        Tipboard.DisplayUtils.showExcMsg(tile, "aMessage");
        Tipboard.DisplayUtils.showExcMsg(tile, "aMessage");
        checkIfErrorIsShown(tile);
    });

    it("change error to tile", function() {
        var tile = getFirstTile();
        Tipboard.DisplayUtils.showExcMsg(tile, "aMessage");
        Tipboard.DisplayUtils.showTileData(tile);
        checkIfTileIsShown(tile);
    });

});

describe("Tipboard tiles API", function() {

    var tileType = 'tileType';
    var fnToRegister = function() {};
    var registering = function() {
        Tipboard.Dashboard.registerUpdateFunction(tileType, fnToRegister);
    };

    beforeEach(function() {
        Tipboard.Dashboard.updateFunctions = {};
    });


    it("allows registering update-tile function", function() {
        expect(registering).not.toThrow();
    });

    it("return registered update-tile function", function() {
        registering();
        var returnedFn = Tipboard.Dashboard.getUpdateFunction(tileType);
        expect(returnedFn).toBe(fnToRegister);
    });

    it(
        "raise exception when getting not registered update-tile function",
        function() {
            expect(
                Tipboard.Dashboard.getUpdateFunction.bind(
                    Tipboard.Dashboard, tileType
                )
            ).toThrow(new Tipboard.Dashboard.UnknownUpdateFunction(tileType));
        }
    );

    it("escapes tile id according to jquery-id restriction", function() {
        var idToEscape = "\\!\"#$%&'()*+,./:;<=>?@[]^`{|}~";
        var escaped = Tipboard.Dashboard.escapeId(idToEscape);
        expect(escaped.length).toBe(idToEscape.length*2);
        var idNotToEscape = "anExampleTileIdNotToEscape1234567890";
        escaped = Tipboard.Dashboard.escapeId(idNotToEscape);
        expect(escaped).toBe(idNotToEscape);
    });

    describe("applyHighlighterConfig function", function() {
        var tileId = 'example_simple_percentage';
        var _getHightlighterNode = function () {
            var highlighterNode = $('#' + tileId + '-big_value').parent();
            return highlighterNode;
        };

        it("sets color correctly", function() {
            var highlighterNode = _getHightlighterNode();
            var transparentColor = $(highlighterNode).parent().css(
                'background-color'
            );
            var DataToCheck = [{
                'colorToSet': undefined,
                'initColor': transparentColor,
                'correct': transparentColor
            }, {
                'colorToSet': undefined,
                'initColor': 'rgb(18, 176, 197)',
                'correct': 'rgb(18, 176, 197)'
            }, {
                'colorToSet': 'blue',
                'initColor': transparentColor,
                'correct': 'rgb(18, 176, 197)'
            }, {
                'colorToSet': 'blue',
                'initColor': 'rgb(18, 176, 197)',
                'correct': 'rgb(18, 176, 197)'
            }];
            $.each(DataToCheck, function(idx, data) {
                $(highlighterNode).css('background-color', data.initColor);
                Tipboard.DisplayUtils.applyHighlighterConfig(
                    highlighterNode, data.colorToSet, false
                );
                var foundColor = $(highlighterNode).css('background-color');
                console.log("found vs correct", foundColor, data.correct);
                expect(foundColor).toBe(data.correct);
            });
        });

        it("sets folding correctly", function() {
            var highlighterNode = _getHightlighterNode();
            var okResults = [
                [false, false, true],
                [true, false, true]
            ];
            $.each([false, true], function(initStateIdx, initState) {
                $.each(["undefined", false, true], function(fadingIdx, fading) {
                    if (initState === true) {
                        highlighterNode.addClass('fading-background-color');
                    }
                    if (initState === false) {
                        highlighterNode.removeClass('fading-background-color');
                    }

                    Tipboard.DisplayUtils.applyHighlighterConfig(
                        highlighterNode, 'blue', fading
                    );
                    var hasClass = $(highlighterNode).hasClass(
                        'fading-background-color'
                    );
                    var expected = okResults[initStateIdx][fadingIdx];
                    expect(hasClass).toBe(expected);
                });
            });
        });

        it("cleans highlighting no color and no fading", function() {
            var highlighterNode = _getHightlighterNode();
            var transparentColor = $(highlighterNode).parent().css(
                'background-color'
            );
            Tipboard.DisplayUtils.applyHighlighterConfig(highlighterNode);

            var foundColor = $(highlighterNode).css('background-color');
            expect(foundColor).toBe(transparentColor);

            var hasClass = $(highlighterNode).hasClass(
                'fading-background-color'
            );
            expect(hasClass).toBe(false);
        });

    });

    describe("setDataByKeys function", function() {
        var _checkFields = function() {
            $.each(dataToSet, function(fieldName, fieldVal) {
                var fieldId = '#' + tileId + '-' + fieldName;
                var got = $(fieldId).text();
                console.log(got, '===', fieldName);
                expect(got).toBe(fieldName);
            });
        };
        var tileId = 'example_simple_percentage';
        var fieldNames = [
            'title', 'subtitle', 'big_value', 'left_label', 'left_value',
            'right_label', 'right_value'
        ];
        var dataToSet = {};
        $.each(fieldNames, function(idx, fieldName) {
            dataToSet[fieldName] = fieldName;
        });

        afterEach(function() {
            // reset fields texts
            $.each(fieldNames, function(idx, fieldName) {
                var fieldId = ['#' + tileId, fieldName].join('-');
                $(fieldId).text('');
            });
        });

        it("works with 'all' arg", function() {
            Tipboard.Dashboard.setDataByKeys(
                tileId, dataToSet, 'all'
            );
            _checkFields();
        });

        it("works when keys list passed", function() {
            Tipboard.Dashboard.setDataByKeys(
                tileId, dataToSet, fieldNames
            );
            _checkFields();
        });

    });

});

describe("Tipboard tile", function() {

    describe("norm_chart", function() {

        it("checks correclty if isRawNormsSet", function() {
            var config = {};
            result = NormChartTile.isRawNormsSet(config);
            expect(result).toBe(false);

            config.canvasOverlay = {
                objects: {},
            };
            result = NormChartTile.isRawNormsSet(config);
            expect(result).toBe(true);

            config.canvasOverlay = {
                objects: 'notObject',
            };
            result = NormChartTile.isRawNormsSet(config);
            expect(result).toBe(false);
        });

        it("creates correctly raw config", function() {
            var easyNorms = [
                ['blue', 0, 1],
                ['red', 5, 3]
            ];
            var colorMap = {
                'blue': '#12B0C5',
                'red': '#DC5945'
            };
            var config = {
                easyNorms: easyNorms
            };
            NormChartTile.useEasyNorms(config);
            expect(isRawNormSet).not.toBe(true);
            var isRawNormSet = NormChartTile.isRawNormsSet(config);
            expect(isRawNormSet).toBe(true);
            $.each(config.canvasOverlay.objects, function(idx, data) {
                var lineData = data.horizontalLine;
                expect(lineData.color).toBe(colorMap[easyNorms[idx][0]]);
                expect(lineData.y).toBe(easyNorms[idx][1]);
                expect(lineData.lineWidth).toBe(easyNorms[idx][2]);
            });
        });

    });

    describe("fancy_listing", function() {
        var getFancyTile = function() {
            return $('#example_fancy_listing');
        };
        var data = [
            {label: 'l1', text: 't1', description: 'd1'},
            {label: 'l2', text: 't2', description: 'd2'},
            {label: 'l3', text: 't3', description: 'd3'},
        ];

        afterEach(function() {
            var tile = getFancyTile();
            $(tile).find('.fancy-listing-item').slice(1).remove();
        });

        describe("initContainer", function() {

            it("returns node to clone", function() {
                var fancyTile = getFancyTile();
                var nodeToClone = FancyListing.initContainer(fancyTile);
                expect(typeof nodeToClone).toBe("object");
                expect(nodeToClone.className).toBe("fancy-listing-item");
            });

            it("removes children beside first", function() {
                var fancyTile = getFancyTile();
                var itemContainer = $(fancyTile).find('.tile-content');
                var nodeToClone = $(itemContainer).children()[0];
                FancyListing.populateItems(fancyTile, nodeToClone, data);
                expect(itemContainer.children().length).toBe(1 + data.length);
                nodeToClone = FancyListing.initContainer(fancyTile);
                var items = $(itemContainer).children();
                expect(items.length).toBe(1);
            });

        });

        xit("centers content vertically", function() {
            // replace centering with css class instead of js, then do test
        });

        it("data is replaced correctly", function() {
            var fancyTile = getFancyTile();
            var itemContainer = $(fancyTile).find('.tile-content');
            var nodeToClone = $(itemContainer).children()[0];
            FancyListing.populateItems(fancyTile, nodeToClone, data);
            var items = $(itemContainer).children().slice(1);
            $.each(items, function(idx, item) {
                itemLabel = $(item).find('.fancy-listing-label-inside').text();
                itemTerm = $(item).find('.fancy-listing-term').text();
                itemDesc = $(item).find('.fancy-listing-desc').text();
                expect(itemLabel).toBe(data[idx].label);
                expect(itemTerm).toBe(data[idx].text);
                expect(itemDesc).toBe(data[idx].description);
            });
        });

        it("applies items config correctly", function() {
            var config = {
                1: { label_color: 'rgb(0, 0, 255)', center: true },
                2: { label_color: 'rgb(0, 0, 255)' },
                3: { center: true }
            };
            var fancyTile = getFancyTile();
            var itemContainer = $(fancyTile).find('.tile-content');
            var nodeToClone = $(itemContainer).children()[0];
            FancyListing.populateItems(fancyTile, nodeToClone, data);
            FancyListing.applyConfig(fancyTile, config);

            var items = $(itemContainer).children().slice(1);
            $.each(items, function(idx, item) {
                var expectedColor, expectedAlign;
                var configColor = config[idx + 1].label_color;
                if (typeof configColor !== "undefined") {
                    expectedColor = configColor;
                } else {
                    expectedColor = $(nodeToClone).css('background-color');
                }
                var itemColor = $(item).find('.fancy-listing-label').css(
                    'background-color'
                );
                expect(itemColor).toBe(expectedColor);

                var configAlign = config[idx + 1].center;
                if (typeof configAlign !== "undefined") {
                    expectedAlign = configAlign;
                } else {
                    expectedAlign = false;
                }
                var itemAlign = $(item).find('.fancy-listing-def').css(
                    'text-align'
                );
                itemAlign = itemAlign === 'center' ? true : false;
                expect(itemAlign).toBe(expectedAlign);
            });
        });

    });

});

describe("Flipboard", function() {

    it("path cycling works correctly", function() {
        var paths = ['a', 'b', 'c'];
        var okPaths = paths.slice();
        okPaths.push(paths[0]);
        Flipboard.init(paths);
        $.each(okPaths, function(idx, okPath) {
            var returnedPath = Flipboard.getNextDashboardPath();
            expect(returnedPath).toBe(okPath);
        });
    });
});

