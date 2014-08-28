function updateTilePie(tileId, data, config, tipboard) {
    Tipboard.Dashboard.setDataByKeys(tileId, data, ['title', 'description']);
    renderersSwapper = new RenderersSwapper();
    renderersSwapper.swap(config);
    var config = jQuery.extend(true, DEFAULT_PIE_CHART_CONFIG, {
      legend: {
        border: Tipboard.DisplayUtils.palette.tile_background,
        background: Tipboard.DisplayUtils.palette.tile_background
      },
      grid: {
        background: Tipboard.DisplayUtils.palette.tile_background
      }
    }, config);
    // colors from palette
    if (config.seriesColors) {
        $.each(config.seriesColors, function (idx, color) {
            config.seriesColors[idx] = Tipboard.DisplayUtils.replaceFromPalette(color);
        });
    } else {
        config.seriesColors = Tipboard.DisplayUtils.getPalette(
            tipboard.color
        );
    }
    // autoscale required nodes and plot
    // TODO: use buildFittedChart
    var tile = Tipboard.Dashboard.id2node(tileId);
    Tipboard.DisplayUtils.expandLastChild(tile);
    Tipboard.DisplayUtils.expandLastChild($(tile).find('.tile-content')[0]);
    Tipboard.Dashboard.chartsIds[tileId] = $.jqplot(
        tileId + '-chart', [data.pie_data], config
    );
}
Tipboard.Dashboard.registerUpdateFunction('pie_chart', updateTilePie);

var DEFAULT_PIE_CHART_CONFIG  = {
  title: false,
  legend: {
      textColor: 'white',
      renderer: $.jqplot.DonutLegendRenderer,
      location: 's',
      show: true,
      border: '0',
      //placement: "outside",
      rendererOptions: {
          numberColumns: 3
      }
  },
  grid: {
      drawGridLines: false,
      borderWidth: 0,
      shadow: false
  },
  seriesDefaults: {
      renderer: $.jqplot.DonutRenderer,
      rendererOptions: {
          padding: 0,
          shadowAlpha: 0,
          sliceMargin: 0,
          innerDiameter: 60,
          showDataLabels: true,
          startAngle: -90
      }
  }
};
