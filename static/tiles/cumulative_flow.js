/*jslint browser: true, devel: true*/
/*global WebSocket: false, Tipboard: false*/

function updateTileCumulativeFlow(id, data, meta, tipboard) {
    if (data.series_list.length > 7) {
        console.log('ERROR: more then 7 series passed - RENDERING STOPPED')
        return;
    }
    var tile = $('#' + id)[0];
    $('#' + id + '-title').html(data['title']);
    var config = jQuery.extend(true, {}, DEFAULT_CUMULATIVE_FLOW_CHART_CONFIG);
    config['axes']['xaxis']['ticks'] = Boolean(meta.ticks) ? meta.ticks : [];
    config['grid']['background'] = tipboard.color.tile_background;
    config['grid']['gridLineColor'] = tipboard.color.tile_background;
    var palette = Tipboard.DisplayUtils.getPalette(tipboard.color);
    var seriesForJqplot = [];
    // clear html labels before inserting
    $($(tile).find('.plot-labels')[0]).find('div').remove()
    for (idx in data.series_list) {
        // unpack series for jqplot
        var seriesData = data.series_list[idx];
        var series = seriesData['series'];
        seriesForJqplot.push(series);
        // update plots labels and colors
        config['series'][idx] = {
            'label': data.series_list[idx]['label'],
            'color': palette[idx]
        };
        // insert labels to html
        var lastValue = series[series.length - 1];
        appendHtmlLabels(
            $(tile).find('.plot-labels')[0],
            config['series'][idx]['label'],
            lastValue,
            config['series'][idx]['color']
        );
    }
    var plot = $.jqplot(id + '-chart', seriesForJqplot, config);
    Tipboard.Dashboard.chartsIds[id] = plot;
    Tipboard.TileDisplayDecorator.runAllDecorators($("#" + id)[0]);
}

Tipboard.Dashboard.registerUpdateFunction('cumulative_flow', updateTileCumulativeFlow);

var DEFAULT_CUMULATIVE_FLOW_CHART_CONFIG  = {
    grid: {
        drawGridLines: false,
        background: '#232526',
        gridLineColor: '#232526',
        borderWidth: 0,
        shadow: false
    },
    stackSeries: true,
    seriesDefaults: {
        fill: true,
        pointLabels: {
            show: false
        },
        trendline: {
            show: false
        },
        showMarker: false
    },
    series: [],
    legend: {
        show: false
    },
    axes: {
        xaxis: {
            ticks: [],
            tickRenderer: $.jqplot.CanvasAxisTickRenderer,
            tickOptions: {
                angle: - 90
            },
            drawMajorGridlines: false
        },
        yaxis: {
            min: 0,
            tickOptions: {
                showLabel: true,
                showMark: false,
                shadow: false
            }
        }
    }
}

function appendHtmlLabels(container, label, value, color) {
    var htmlLabel = [
        '<div class="result bugs-count-result medium-result">',
        '<span style="float:left" class="issue-stats-bugs-number">',
        label,
        '</span>',
        '<span style="float:right" class="issue-stats-bugs-number float-right">',
        value,
        '</span>',
        '<div style="clear:both"></div>',
        '</div>'
    ].join('\n');
    $(container).append(htmlLabel);
    $(container).find('span').last().css('color', color);
}

