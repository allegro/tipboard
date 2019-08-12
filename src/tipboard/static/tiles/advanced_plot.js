(function($) {
    'use strict';

    var AdvancedPlotTile;

    AdvancedPlotTile = {
        buildChart: function (tileId, plotData, config) {
            // DEPRECATED fn, use Tipboard.Dashboard.createGraph
            var containerId, plot;
            containerId = tileId + '-chart';
            plot = $.jqplot(containerId, plotData, config);
            Tipboard.Dashboard.chartsIds[tileId] = plot;
        },
        setDataByKeys: function (tileId, data, keys) {
            Tipboard.Dashboard.setDataByKeys(tileId, data, keys);
        },
        rescaleContainers: function (tile) {
            Tipboard.DisplayUtils.expandLastChild(tile);
            Tipboard.DisplayUtils.expandLastChild($(tile).find('.tile-content')[0]);
        }
    };

    function updateTileAdvancedPlot(tileId, data, meta) {
        var tile, newMeta;
        tile = Tipboard.Dashboard.id2node(tileId);
        AdvancedPlotTile.setDataByKeys(tileId, data, ['title', 'description']);
        newMeta = $.extend(true, {}, meta);
        var renderersSwapper = new RenderersSwapper();
        renderersSwapper.swap(newMeta);
        AdvancedPlotTile.rescaleContainers(tile);
        AdvancedPlotTile.buildChart(tileId, data.plot_data, newMeta);
    }

    Tipboard.Dashboard.registerUpdateFunction('advanced_plot', updateTileAdvancedPlot);
}($));
