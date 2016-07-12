/*jslint browser: true, devel: true*/
/*global WebSocket: false, Tipboard: false*/

function simplifyLineData(series_data, user_config) {
    var config = {
        tolerancy: 10,
        data_points_limit: 50, // we will TRY to achieve lower number of data points than this
        max_simplifying_steps: 5,
        simplify_step_multiplicator: 1.5
        };

    $.extend(config, user_config);
    
    var simplify_data = new Array();
    var return_data = new Array();

    for(var series = 0; series < series_data.length; series++) {
        simplify_data[series] = new Array();
        return_data[series] = new Array();

        // converting data to format acceptable by simplify.js library
        if(typeof series_data[series][0] === typeof []) {
            for(var tick = 0; tick < series_data[series].length; tick++) {
                simplify_data[series].push({
                    x: tick,
                    y: series_data[series][tick][1],
                    key: series_data[series][tick][0]
                });
            }
        } else {
            for(var tick = 0; tick < series_data[series].length; tick++) {
                simplify_data[series].push({
                    x: tick,
                    y: series_data[series][tick],
                    key: null
                });
            }
        }

        var current_tolerance = config.tolerancy;
        for(var i = 0; i < config.max_simplifying_steps; i++) {
            simplify_data[series] = simplify(simplify_data[series], current_tolerance);
            if(simplify_data[series].length < config.data_points_limit) break;
            current_tolerance = Math.floor(current_tolerance * config.simplify_step_multiplicator);
        }

        // prepare in data format understandable by jqplot
        for(var tick = 0; tick < simplify_data[series].length; tick++) {
            if(simplify_data[series][tick].key != null)
                return_data[series][tick] = [
                    simplify_data[series][tick].key,
                    simplify_data[series][tick].y
                ];
            else
                return_data[series][simplify_data[series][tick].x] = simplify_data[series][tick].y;
        }

        // fill all created gaps with null for jqplot
	for(var i = 0; i < return_data[series].length; i++) {
            if(!return_data[series][i])
                return_data[series][i] = null;
        }
    }

    return return_data;
}

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

    if(config.simplify) data.series_list = simplifyLineData(data.series_list, config.simplify);

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
