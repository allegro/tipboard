function updateTileBarChart(tileId, data, meta, tipboard) {
    Tipboard.Dashboard.setDataByKeys(tileId, data, ['title', 'subtitle']);
    renderersSwapper = new RenderersSwapper();
    renderersSwapper.swap(meta);
    var config = jQuery.extend(true, {}, DEFAULT_BAR_CHART_CONFIG, {
      'grid': {
        'background': tipboard.color.tile_background,
        'gridLineColor': tipboard.color.tile_background
      },
      'series': Tipboard.DisplayUtils.paletteAsSeriesColors()
    }, meta);
    if (Boolean(data.ticks)) {
      // ticks from *data* are more important than ticks from *config*
      config.axes.yaxis.ticks = data.ticks;
    }
    var tile = Tipboard.Dashboard.id2node(tileId);
    // TODO replace it with Tipboard.Dashboard.rescaleTile
    Tipboard.DisplayUtils.expandLastChild(tile);
    Tipboard.DisplayUtils.expandLastChild($(tile).find('.tile-content')[0]);
    Tipboard.Dashboard.chartsIds[tileId] = $.jqplot(
        tileId + '-chart', data.series_list, config
    );
}

Tipboard.Dashboard.registerUpdateFunction('bar_chart', updateTileBarChart);

var DEFAULT_BAR_CHART_CONFIG  = {
    title: {
        show: false
    },
    grid: {
        borderWidth: 0,
        shadow: false
    },
    showMarker: false,
    axes: {
        xaxis: {
            tickOptions: {
                showLabel: false,
                showMark: false,
                shadow: false
            }
        },
        yaxis: {
            renderer: $.jqplot.CategoryAxisRenderer,
            tickRenderer: $.jqplot.CanvasAxisTickRenderer,
            tickOptions: {
                shadow: false,
                textColor: '#a4a4a4',
                markSize: 0
            }
        }
    },
    seriesDefaults: {
        pointLabels: {
            show: true
        },
        renderer: $.jqplot.BarRenderer,
        rendererOptions: {
            barWidth: 25,
            barPadding: 3,
            shadowAlpha: 0,
            barDirection: 'horizontal'
        },
        trendline: {
            show: false
        }
    }
};
