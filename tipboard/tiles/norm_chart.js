(function ($) {
    'use strict';

    var NormChartTile;

    NormChartTile = {
        defaultConfig: {
            legend: {
                location: 's',
                renderer: $.jqplot.EnhancedLegendRenderer,
                show: true,
                rendererOptions: {
                    numberColumns: 3
                }
            },
            grid: {
                gridLineWidth: 0,
                gridLineColor: '#4a4d52',
                borderWidth: 0,
                shadow: false
            },
            axes: {
                yaxis: {
                    tickOptions: {
                        textColor: 'white',
                        showMark: false
                    }
                },
                xaxis: {
                    drawMajorGridlines: false,
                    show: false,
                    autoscale: true,
                    tickOptions: {
                        showLabel: false,
                        showMark: false,
                        shadow: false
                    }
                }
            },
            seriesDefaults: {
                trendline: {
                    show: false
                },
                pointLabels: {
                    show: false
                },
                rendererOptions: {
                    smooth: true
                },
                showMarker: false
            },
        },

        isRawNormsSet: function (config) {
            var isSet;
            try {
                isSet = config.canvasOverlay.objects;
                isSet = typeof isSet === "object" ? true : false;
            } catch (e) {
                if (e.name === "TypeError") {
                    isSet = false;
                } else {
                    throw e;
                }
            }
            return isSet;
        },

        hasEasyNorms: function (config) {
            var hasIt = typeof config.easyNorms === 'object' ? true : false;
            return hasIt;
        },

        useEasyNorms: function (config) {
            // config.easyNorms is [[color, y, width], [..]]
            config.canvasOverlay = {
                show: true,
                objects: []
            };

            $.each(config.easyNorms, function (idx, val) {
                var color = (
                    Tipboard.DisplayUtils.replaceFromPalette(val[0]) ||
                    Tipboard.DisplayUtils.paletteAsList()[
                        // wrap colors when out of list
                        idx % Tipboard.DisplayUtils.paletteAsList.length
                    ]);
                config.canvasOverlay.objects.push({
                    horizontalLine: {
                        color: color,
                        y: val[1] || 0,
                        lineWidth: val[2] || 2,
                        shadow: false
                        //lineCap: 'butt',
                        //xOffset: 0
                    }
                });
            });
            delete config.easyNorms;
        },

        setNorms: function (config) {
            if (NormChartTile.isRawNormsSet(config)) {
                delete config.easyNorms;
            } else {
                if (NormChartTile.hasEasyNorms(config)) {
                    NormChartTile.useEasyNorms(config);
                }
            }
        },

        updateTile: function (tileId, data, config) {
            Tipboard.Dashboard.setDataByKeys(
                tileId, data, ['title', 'description']
            );
            var newConfig = $.extend(true, {
                // XXX: it could be set in defaultConfig, but initially palette
                // is undefined
                legend: {
                    border: Tipboard.DisplayUtils.palette.tile_background,
                    background: Tipboard.DisplayUtils.palette.tile_background
                },
                grid: {
                    background: Tipboard.DisplayUtils.palette.tile_background
                }
            }, NormChartTile.defaultConfig, config);
            NormChartTile.setNorms(newConfig);
            renderersSwapper.swap(newConfig);
            var tile = Tipboard.Dashboard.id2node(tileId);
            Tipboard.DisplayUtils.rescaleTile(tile);
            Tipboard.DisplayUtils.createGraph(
                tileId, data.plot_data, newConfig
            );
        }
    };

    window.NormChartTile = NormChartTile;
    Tipboard.Dashboard.registerUpdateFunction(
        'norm_chart', NormChartTile.updateTile
    );

}($));
