/*jslint browser: true, devel: true*/
/*global WebSocket: false, Tipboard: false*/


function updateTileLine(tileId, data, meta, tipboard) {
    var tile = Tipboard.Dashboard.id2node(tileId);
    Tipboard.Dashboard.setDataByKeys(tileId, data, ['subtitle', 'description']);
    // config creation
    renderersSwapper = new RenderersSwapper();
    renderersSwapper.swap(meta);
    var graphColors = {
        grid: {
            background: tipboard.color.tile_background,
            gridLineColor: tipboard.color.tile_background
        },
        series: Tipboard.DisplayUtils.paletteAsSeriesColors()
    };
    var config = $.extend(true, {}, DEFAULT_LINE_CHART_CONFIG, graphColors, meta);

    // autoscale required nodes and plot
    // TODO use Tipboard.Dashboard.buildChart
    Tipboard.DisplayUtils.expandLastChild(tile);
    Tipboard.DisplayUtils.expandLastChild($(tile).find('.tile-content')[0]);
    Tipboard.Dashboard.chartsIds[tileId] = $.jqplot(
        tileId + '-chart', data.series_list, config
    );
}

Tipboard.Dashboard.registerUpdateFunction('line_chart', updateTileLine);

var DEFAULT_LINE_CHART_CONFIG  = {
    legend: {
        show: false,
        location: 's',
        border: '#232526',
        background: '#232526'
    },
    title: {
        show: false
    },
    grid: {
        drawGridLines: false,
        borderWidth: 0,
        shadow: false
    },
    axes: {
        xaxis: {
            renderer: $.jqplot.CategoryAxisRenderer,
            show: true,
            tickOptions: {
                showLabel: true,
                showMark: false,
                shadow: false
            }
        },
        yaxis: {
            show: true,
            autoscale: true,
            tickOptions: {
                showLabel: false,
                showMark: false,
                shadow: false
            }
        }
    },
    seriesDefaults: {
        showMarker: true,
        lineWidth: 3,
        shadow: false,
        trendline: {
            lineWidth: 3
        },
        pointLabels: {
            color: '#ffffff',
            xpadding: 10,
            ypadding: 10,
            location: 'sw'
        },
        markerRenderer: $.jqplot.MarkerRenderer,
        markerOptions: {
            show: true,
            style: 'filledCircle',
            lineWidth: 2,
            size: 9,
            shadow: true,
            shadowAngle: 45,
            shadowOffset: 1,
            shadowDepth: 3,
            shadowAlpha: 0.07
        }
    }
};
