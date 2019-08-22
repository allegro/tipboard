/**
 * Render Factory to deliver Jqplot object regarding the tile needs
 * @constructor
 */
function RendererFactory() { }
// Define a dict to list all chart available in jqplot
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
// Define a ptr to function, based on rendererName2renderObj, if undefined throw UnknownRenderer
RendererFactory.prototype.createRenderer = function (rendererName) {
    var lower = rendererName.toLowerCase();
    var rendererClass = RendererFactory.prototype.rendererName2renderObj[lower];
    if (typeof(rendererClass) === 'undefined') {
        throw new RendererFactory.prototype.UnknownRenderer(rendererName);
    }
    return rendererClass;
};
// Definition of the Exception UnknownRenderer
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

var renderersSwapper = new RenderersSwapper();
