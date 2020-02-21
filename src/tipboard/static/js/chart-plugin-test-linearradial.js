(function (Chart) {
    "use strict";
    let helpers = Chart.helpers;

    let defaultConfig = {
        id: "gaugescale",
        position: "chartArea",
        fullWidth: true,
        display: true,
        range: {
            startValue: -100,
            endValue: 500
        },
        responsive: true,
        font: {
            fontName: "Arial",
            fontSize: 12
        },
        axisWidth: 6,
        axisColor: "#00f",
        ticks: {
            padding: 5,
            callback: function (tick) {
                return tick.tick.toString();
            }
        },
        padding: {
            top: 10,
            bottom: 10,
            left: 20,
            right: 20
        },
        scaleLabel: {
            display: true
        },
    };

    function parseLineHeight(options) {
        return helpers.options.toLineHeight(
            helpers.valueOrDefault(options.lineHeight, 1.2),
            helpers.valueOrDefault(options.fontSize, defaultConfig.font.fontSize));
    }

    function computeTextSize(context, tick, font) {
        return helpers.isArray(tick) ?
            helpers.longestText(context, font, tick) :
            context.measureText(tick).width;
    }

    const LinearGaugeScale = Chart.Scale.extend({

        textDimention: function (val) {
            let width = 0;
            let height = this.options.font.fontSize;
            let str = val + "";
            width = (height / 1.7) * str.length;
            if (val.substr(0, 1) === "-") width -= height / 3.5;
            return {
                width: width,
                height: height
            };
        },
        setDimensions: function () {
            this.height = this.maxHeight;
            this.width = this.maxWidth;
            this.xCenter = this.left + Math.round(this.width / 2);
            this.yCenter = this.top + Math.round(this.height / 2);

            this.paddingLeft = 0;
            this.paddingTop = 0;
            this.paddingRight = 0;
            this.paddingBottom = 0;
        },
        labelsFromTicks: function (ticks) {
            let labels = [];
            let i, ilen;

            for (i = 0, ilen = ticks.length; i < ilen; ++i) {
                labels.push(ticks[i].label);
            }

            return labels;
        },
        buildTicks: function () {

            let me = this;
            let opts = me.options;
            let tickOpts = opts.ticks;
            let ticks = [];

            //	Prepare values for ticks
            //	Major ticks
            if (typeof (opts.ticks.majorTicks) == "object" && opts.ticks.majorTicks !== null && opts.ticks.majorTicks.interval > 0) {
                let majTicks = [];
                if (typeof opts.ticks.majorTicks.customValues !== "undefined" &&
                    typeof opts.ticks.majorTicks.customValues.length !== "undefined" &&
                    opts.ticks.majorTicks.customValues.length > 0) {
                    majTicks = opts.ticks.majorTicks.customValues;
                } else {
                    let interval = opts.ticks.majorTicks.interval;
                    let numOfMajor = (opts.range.endValue - opts.range.startValue) / interval;
                    for (let i = 0; i < numOfMajor - 1; i++) {
                        majTicks.push(opts.range.startValue + (interval * (i + 1)));
                    }
                }
                this.majTicks = majTicks;
                for (let i in majTicks) ticks.push({type: "major", tick: majTicks[i]});

                //	Setup default settings
                tickOpts.majorTicks.interval = tickOpts.majorTicks.interval || 100;
                tickOpts.majorTicks.customValues = tickOpts.majorTicks.customValues || [];
                tickOpts.majorTicks.width = tickOpts.majorTicks.width || 6;
                tickOpts.majorTicks.height = tickOpts.majorTicks.height || 1;
                tickOpts.majorTicks.offset = tickOpts.majorTicks.offset || 0;
                tickOpts.majorTicks.color = tickOpts.majorTicks.color || "#fff";

            }

            //	Minor ticks
            if (typeof (opts.ticks.minorTicks) == "object" && opts.ticks.minorTicks !== null && opts.ticks.minorTicks.interval > 0) {
                let minTicks = [];
                if (typeof opts.ticks.minorTicks.customValues !== "undefined" &&
                    typeof opts.ticks.minorTicks.customValues.length !== "undefined" &&
                    opts.ticks.minorTicks.customValues.length > 0) {
                    minTicks = opts.ticks.minorTicks.customValues;
                } else {
                    let interval = opts.ticks.minorTicks.interval;
                    let numOfMinor = (opts.range.endValue - opts.range.startValue) / interval;
                    for (let i = 0; i < numOfMinor - 1; i++) {
                        minTicks.push(opts.range.startValue + (interval * (i + 1)));
                    }
                }
                this.minTicks = minTicks;
                for (let i in minTicks) ticks.push({type: "minor", tick: minTicks[i]});

                //	Setup default settings
                tickOpts.minorTicks.interval = tickOpts.minorTicks.interval || 50;
                tickOpts.minorTicks.customValues = tickOpts.minorTicks.customValues || [];
                tickOpts.minorTicks.width = tickOpts.minorTicks.width || 4;
                tickOpts.minorTicks.height = tickOpts.minorTicks.height || 1;
                tickOpts.minorTicks.offset = tickOpts.minorTicks.offset || -2;
                tickOpts.minorTicks.color = tickOpts.minorTicks.color || "#fff";

            }

            return ticks;
        },
        convertTicksToLabels: function (ticks) {

            let me = this;
            let opts = me.options;
            let scaleLabelOpts = opts.scaleLabel;

            //	Labels of ticks
            let labelVals = [];
            if (typeof (scaleLabelOpts) == "object" && scaleLabelOpts !== null && scaleLabelOpts.interval > 0) {

                if (scaleLabelOpts.customValues && scaleLabelOpts.customValues.length > 0) {
                    labelVals = scaleLabelOpts.customValues;
                } else {
                    let interval = scaleLabelOpts.interval;
                    let numOfLabels = ((opts.range.endValue - opts.range.startValue) / interval) + 1;
                    for (let i = 0; i < numOfLabels; i++) {
                        labelVals.push(opts.range.startValue + (interval * i));
                    }
                }
                this.labelVals = labelVals;
            }
            me.tickLabels = labelVals;
            return labelVals;
        },
        calculateTickRotation: helpers.noop,
        getBase: function () {
            let me = this;
            if (typeof me.scalePoint !== "undefined")
                return me.scalePoint(0);
            else return 0;
        },
        fit: function () {
            let me = this;
            // Reset
            let minSize = me.minSize = {
                width: 0,
                height: 0
            };

            let labels = me.labelsFromTicks(me._ticks);

            let opts = me.options;
            let tickOpts = opts.ticks;
            let scaleLabelOpts = opts.scaleLabel;
            let gridLineOpts = opts.gridLines;
            let display = opts.display;
            let isHorizontal = me.isHorizontal();

            let tickFont = opts.font.fontName;
            let tickMarkLength = opts.gridLines.tickMarkLength;

            //	Horizontal orientation
            if (isHorizontal) {
                this.scalePoint = function (val) {
                    let displayW = this.width - opts.padding.left - opts.padding.right;
                    let rangeH = opts.range.endValue - opts.range.startValue;
                    let factor = displayW / rangeH;
                    return Math.round((val * factor) + opts.padding.left + me.left - (opts.range.startValue * factor));
                };

            } else {
                this.scalePoint = function (val) {
                    let displayH = this.height - opts.padding.top - opts.padding.bottom;
                    let rangeH = opts.range.endValue - opts.range.startValue;
                    let factor = displayH / rangeH;
                    return Math.round(this.height - (val * factor - (opts.range.startValue * factor)) - opts.padding.bottom + me.top);
                };

            }
            me.xCenter = this.left + this.width / 2; // center of chart located at the center of canvas
            me.yCenter = this.top + this.height / 2; // center of chart located at the center of canvas

            // Width
            if (isHorizontal) {
                // subtract the margins to line up with the chartArea if we are a full width scale
                minSize.width = me.isFullWidth() ? me.maxWidth - me.margins.left - me.margins.right : me.maxWidth;
            } else {
                minSize.width = display && gridLineOpts.drawTicks ? tickMarkLength : 0;
            }

            // height
            if (isHorizontal) {
                minSize.height = display && gridLineOpts.drawTicks ? tickMarkLength : 0;
            } else {
                minSize.height = me.maxHeight; // fill all the height
            }

            // Are we showing a title for the scale?
            if (scaleLabelOpts.display && display) {
                let scaleLabelLineHeight = parseLineHeight(scaleLabelOpts);
                let scaleLabelPadding = helpers.options.toPadding(scaleLabelOpts.padding);
                let deltaHeight = scaleLabelLineHeight + scaleLabelPadding.height;

                if (isHorizontal) {
                    minSize.height += deltaHeight;
                } else {
                    minSize.width += deltaHeight;
                }
            }

            me.handleMargins();

            me.width = minSize.width;
            me.height = minSize.height;
        },
        draw: function () {
            let me = this;
            let ctx = this.ctx;
            let isHorizontal = this.isHorizontal();
            let opts = this.options;
            let tickOpts = opts.ticks;
            ctx.textBaseline = "alphabetic";
            ctx.textAlign = "start";

            //	Horizontal orientation
            if (isHorizontal) {
                //	Draw scale background
                ctx.beginPath();
                ctx.fillStyle = opts.axisColor;
                ctx.rect(this.xCenter - this.width / 2 + opts.padding.left, this.yCenter - opts.axisWidth / 2,
                    this.width - opts.padding.left - opts.padding.right, opts.axisWidth);
                ctx.fill();
                ctx.closePath();

                //	Draw scale color ranges
                if (typeof (opts.scaleColorRanges) == "object" && opts.scaleColorRanges.length > 0) {
                    helpers.each(opts.scaleColorRanges, function (d, ind) {
                        let width = this.scalePoint(d.end) - this.scalePoint(d.start);
                        let height = opts.axisWidth;
                        ctx.beginPath();
                        ctx.fillStyle = d.color;
                        ctx.rect(
                            this.scalePoint(d.start),
                            this.yCenter - (height / 2),
                            width,
                            height
                        );
                        ctx.fill();

                    }, this);
                }

                //	Draw scale minor ticks
                ctx.beginPath();
                if (typeof (this.minTicks) == "object" && this.minTicks.length > 0) {
                    ctx.fillStyle = tickOpts.minorTicks.color;
                    ctx.strokeStyle = tickOpts.minorTicks.color;
                    ctx.lineWidth = tickOpts.minorTicks.height;
                    for (let v = 0; v < this.minTicks.length; v++) {
                        let val = this.minTicks[v];
                        ctx.moveTo(this.scalePoint(val) - (tickOpts.minorTicks.height / 2),
                            this.yCenter - (tickOpts.minorTicks.width / 2) + tickOpts.minorTicks.offset);
                        ctx.lineTo(this.scalePoint(val) - (tickOpts.minorTicks.height / 2), (this.yCenter - (tickOpts.minorTicks.width / 2) + tickOpts.minorTicks.offset) + tickOpts.minorTicks.width);
                        ctx.stroke();
                    }
                }
                ctx.closePath();

                //	Draw scale major ticks
                ctx.beginPath();
                if (typeof (this.majTicks) == "object" && this.majTicks.length > 0) {
                    ctx.fillStyle = tickOpts.majorTicks.color;
                    ctx.strokeStyle = tickOpts.majorTicks.color;
                    ctx.lineWidth = tickOpts.majorTicks.height;
                    for (let v = 0; v < this.majTicks.length; v++) {
                        let val = this.majTicks[v];
                        ctx.moveTo(this.scalePoint(val) - (tickOpts.majorTicks.height / 2),
                            this.yCenter - (tickOpts.majorTicks.width / 2) + tickOpts.majorTicks.offset);
                        ctx.lineTo(this.scalePoint(val) - (tickOpts.majorTicks.height / 2), (this.yCenter - (tickOpts.majorTicks.width / 2) + tickOpts.majorTicks.offset) + tickOpts.majorTicks.width);
                        ctx.stroke();
                    }
                }
                ctx.closePath();

                //	Draw scale labels
                let labels = me.labelsFromTicks(me._ticks);
                ctx.beginPath();
                if (typeof (labels) == "object" && labels.length > 0) {
                    ctx.fillStyle = opts.scaleLabel.color;
                    ctx.font = opts.font.fontSize + "px " + opts.font.fontName;
                    for (let v = 0; v < labels.length; v++) {
                        let val = labels[v];
                        if (opts.scaleLabel.display) {
                            let text = val + opts.scaleLabel.units;
                            ctx.fillText(text,
                                this.scalePoint(val) - this.textDimention(text).width / 2,
                                this.yCenter + (opts.scaleLabel.offset > 0 ? 0 : this.textDimention(text).height) - opts.scaleLabel.offset
                            );
                        }
                    }
                }
                ctx.closePath();
            } else {
                //	Draw scale background
                ctx.beginPath();
                ctx.fillStyle = opts.axisColor;
                ctx.rect(this.xCenter - opts.axisWidth / 2, this.yCenter - this.height / 2 + opts.padding.top, opts.axisWidth, this.height - opts.padding.top - opts.padding.bottom);
                ctx.fill();
                ctx.closePath();

                //	Draw scale color ranges
                if (typeof (opts.scaleColorRanges) == "object" && opts.scaleColorRanges.length > 0) {
                    helpers.each(opts.scaleColorRanges, function (d, ind) {
                        let width = opts.axisWidth;
                        let height = this.scalePoint(d.start) - this.scalePoint(d.end);
                        ctx.beginPath();
                        ctx.fillStyle = d.color;
                        ctx.rect(
                            this.xCenter - (width / 2),
                            this.scalePoint(d.end),
                            width,
                            height
                        );
                        ctx.fill();

                    }, this);
                }

                //	Draw scale minor ticks
                ctx.beginPath();
                if (typeof (this.minTicks) == "object" && this.minTicks.length > 0) {
                    ctx.fillStyle = tickOpts.minorTicks.color;
                    ctx.strokeStyle = tickOpts.minorTicks.color;
                    ctx.lineWidth = tickOpts.minorTicks.height;
                    for (let v = 0; v < this.minTicks.length; v++) {
                        let val = this.minTicks[v];
                        ctx.moveTo(Math.ceil(this.xCenter - (tickOpts.minorTicks.width / 2) + tickOpts.minorTicks.offset),
                            Math.ceil(this.scalePoint(val)) + 0.5);
                        //this.scalePoint(val) - (tickOpts.minorTicks.height / 2));
                        ctx.lineTo(Math.ceil((this.xCenter - (tickOpts.minorTicks.width / 2) + tickOpts.minorTicks.offset) + tickOpts.minorTicks.width),
                            Math.ceil(this.scalePoint(val)) + 0.5);
                        //this.scalePoint(val) - (tickOpts.minorTicks.height / 2));
                        ctx.stroke();
                    }
                }
                ctx.closePath();

                //	Draw scale major ticks
                ctx.beginPath();
                if (typeof (this.majTicks) == "object" && this.majTicks.length > 0) {
                    ctx.fillStyle = tickOpts.majorTicks.color;
                    ctx.strokeStyle = tickOpts.majorTicks.color;
                    ctx.lineWidth = tickOpts.majorTicks.height;
                    for (let v = 0; v < this.majTicks.length; v++) {
                        let val = this.majTicks[v];
                        ctx.moveTo(Math.ceil(this.xCenter - (tickOpts.majorTicks.width / 2) + tickOpts.majorTicks.offset),
                            Math.ceil(this.scalePoint(val)) + 0.5);
                        //this.scalePoint(val) - (tickOpts.majorTicks.height / 2));
                        ctx.lineTo(Math.ceil((this.xCenter - (tickOpts.majorTicks.width / 2) + tickOpts.majorTicks.offset) + tickOpts.majorTicks.width),
                            Math.ceil(this.scalePoint(val)) + 0.5);
                        //this.scalePoint(val) - (tickOpts.majorTicks.height / 2));
                        ctx.stroke();
                    }
                }
                ctx.closePath();

                //	Draw scale labels
                let labels = me.labelsFromTicks(me._ticks);
                ctx.beginPath();
                if (typeof (labels) == "object" && labels.length > 0) {
                    ctx.fillStyle = opts.scaleLabel.color;
                    ctx.font = opts.font.fontSize + "px " + opts.font.fontName;
                    for (let v = 0; v < labels.length; v++) {
                        let val = parseFloat(labels[v]);
                        if (opts.scaleLabel.display) {
                            let text = val + opts.scaleLabel.units;
                            ctx.fillText(text,
                                this.xCenter - (opts.scaleLabel.offset > 0 ? 0 : this.textDimention(text).width) + opts.scaleLabel.offset,
                                this.scalePoint(val) + this.textDimention(text).height / 4
                            );
                        }
                    }
                }
                ctx.closePath();
            }
        },
        // Shared Methods
        isHorizontal: function () {
            return this.options.position === "top" || this.options.position === "bottom" || this.options.horizontal;
        },

    });
    Chart.scaleService.registerScaleType("linearGauge", LinearGaugeScale, defaultConfig);
}).call(this, Chart);


(function (Chart) {

    let helpers = Chart.helpers;

    let globalDefaults = Chart.defaults.global;

    Chart.defaults._set("global", {
        elements: {
            gaugerect: {
                backgroundColor: "#0fa",
                borderWidth: 3,
                borderColor: globalDefaults.defaultColor,
                borderCapStyle: "butt",
                fill: true, // do we fill in the area between the line and its base axis
                width: 6,
                height: 6,
                shape: "rect",
                pointer: "bar",
                text: "Pointer Text",
                fontSize: 14,
                fontFamily: "Arial",
                offset: 0,
                rotate: 0,
                color: "#000"
            }
        }
    });

    Chart.elements.Gaugerect = Chart.elements.Rectangle.extend({

        rangeColorImage: null,

        generateImage: function (colors, widths) {
            let width = 0;
            for (let i = 0; i < widths.length; i++)
                width += widths[i];
            let canvas = document.createElement("canvas"),
                c = canvas.getContext("2d");
            //document.body.appendChild(canvas);
            canvas.width = width;
            canvas.height = 1;
            let gw2 = widths[0];
            let grd = c.createLinearGradient(0, 0, width, 0);
            grd.addColorStop(0, colors[0]);
            for (let k = 0; k < colors.length; k++) {
                if ((k + 1) < colors.length) {
                    gw2 += widths[k + 1] / 2;
                    let ks = gw2 / width;
                    if (ks > 1) ks = 1;
                    grd.addColorStop(ks, colors[k + 1]);
                } else grd.addColorStop(1, colors[k]);
                c.closePath();
                if ((k + 1) < colors.length)
                    gw2 += widths[k + 1] / 2;
            }
            c.fillStyle = grd;
            c.fillRect(0, 0, width, 20);
            let imgd = c.getImageData(0, 0, canvas.width, 1);
            return imgd;
        },
        getColor: function (val, scale) {
            let out = 0;
            let rc = 0;
            let gc = 0;
            let bc = 0;
            let ac = 1;
            let opts = this.getMeOptions();
            //	If image data did not filled yet
            if (this.rangeColorImage === null) {
                let colors = [];
                let widths = [];
                //colors.push(startColor);
                helpers.each(opts.colorRanges, function (cl, i) {
                    if (i === 0)
                        widths.push((cl.breakpoint - this._Scale.options.range.startValue) * scale);//this.scaleValue);
                    else
                        widths.push((cl.breakpoint - opts.colorRanges[i - 1].breakpoint) * scale);//this.scaleValue);
                    colors.push(cl.color);

                }, this);
                this.rangeColorImage = this.generateImage(colors, widths);
            }


            let start = this._Scale.options.range.startValue;

            let k = Math.ceil((val - start) * scale);//this.scaleValue);
            rc = this.rangeColorImage.data[k * 4 + 0];
            gc = this.rangeColorImage.data[k * 4 + 1];
            bc = this.rangeColorImage.data[k * 4 + 2];
            ac = this.rangeColorImage.data[k * 4 + 3];

            return "rgba(" + rc + ", " + gc + ", " + bc + ", " + ac / 256 + ")";
        },

        getMeOptions: function () {
            let me = this;
            let i = me._datasetIndex;
            let opts = me._chart.config.data.datasets[i];
            return opts;
        },

        draw: function () {
            let me = this;
            let vm = me._view;
            let ctx = me._chart.ctx;
            let opts = me.getMeOptions();
            let horizontal = me._model.horizontal;
            let defaults = me._chart.options.elements.gaugerect;

            ctx.save();
            if (typeof (opts.colorRanges) == "object" && opts.colorRanges.length > 0) {
                let clr = me.getColor(me._model.value, me._model.scaleValue);
                ctx.fillStyle = clr;
            } else
                ctx.fillStyle = me._model.backgroundColor;


            opts.pointer = opts.pointer ? opts.pointer : defaults.pointer;

            if (typeof opts.img !== "undefined" && opts.img !== null) {
                let imgsrc = opts.img;
                if (typeof opts.imageRanges !== "undefined" && typeof opts.imageRanges.length !== "undefined" && opts.imageRanges.length > 0) {
                    for (let i in opts.imageRanges) {
                        let r = opts.imageRanges[i];
                        if (me._model.value >= r.startpoint && me._model.value < r.breakpoint && typeof r.img !== "undefined" && r.img !== "") {
                            imgsrc = r.img;
                            break;
                        }
                    }
                }
                if (typeof this.imgs === "undefined") this.imgs = [];
                let imbuffer = null;
                for (let i in this.imgs) {
                    if (this.imgs[i].src === imgsrc) imbuffer = this.imgs[i];
                    break;
                }
                if (imbuffer === null) imbuffer = new Image();
                imbuffer.src = imgsrc;
                this.imgs.push(imbuffer);

                let width = me._view.width = opts.width ? opts.width : defaults.width;
                let height = me._view.height = opts.height ? opts.height : defaults.height;
                if (horizontal) {
                    me._view.x = vm.head;
                    let x = vm.head - width / 2;
                    let y = vm.y + height / 2;
                } else {
                    let x = vm.x - width / 2;
                    let y = vm.y - height / 2;
                }
                if (imbuffer.complete) {
                    ctx.beginPath();
                    ctx.drawImage(imbuffer, 0, 0, imbuffer.width, imbuffer.height, x, y, width, height);
                    ctx.restore();
                } else {
                    imbuffer.onload = function () {
                        ctx.beginPath();
                        ctx.drawImage(imbuffer, 0, 0, imbuffer.width, imbuffer.height, x, y, width, height);
                        ctx.restore();
                    }
                }

                return;
            }

            if (typeof opts.pointer === "undefined" || opts.pointer === "bar") {

                // Stroke Line
                ctx.beginPath();

                ctx.rect(
                    vm.x,
                    vm.y,
                    vm.width,
                    vm.height
                );

                ctx.fill();
                ctx.restore();
            }

            if (opts.pointer === "point") {

                let shape = opts.shape ? opts.shape : defaults.shape;
                let width = me._view.width = opts.width ? opts.width : defaults.width;
                let height = me._view.height = opts.height ? opts.height : defaults.height;

                if (shape == "circle") {

                    if (horizontal) {
                        let x = me._view.x = vm.head;
                        let y = vm.y;
                    } else {
                        let x = vm.x;
                        let y = vm.y;
                    }
                    /*
                    this.leftX = x - this.height / 2;
                    this.rightX = x + this.height / 2;
                    this.leftY = y - this.height / 2;
                    this.rightY = y + this.height / 2;
                    ctx.arc(x, y, r, sAngle, eAngle, counterclockwise);
                    */

                    let r = width / 2;
                    let sAngle = 0;
                    let eAngle = Math.PI * 2;
                    let counterclockwise = false;
                    ctx.beginPath();
                    ctx.arc(x, y, r, sAngle, eAngle, counterclockwise);
                    ctx.fill();
                    ctx.restore();
                }
                if (shape == "rect") {
                    if (horizontal) {
                        me._view.x = vm.head;
                        let x = vm.head - width / 2;
                        let y = vm.y - height / 2;
                    } else {
                        let x = vm.x - width / 2;
                        let y = vm.y - height / 2;
                    }

                    ctx.beginPath();
                    ctx.rect(x, y, width, height);
                    ctx.fill();
                    ctx.restore();
                }
                if (shape == "triangle") {

                    if (horizontal) {
                        let x1 = me._view.x = vm.head,
                            y1 = vm.y + height / 2,
                            x2 = x1 - width / 2,
                            y2 = y1 - height,
                            x3 = x2 + width,
                            y3 = y2;
                    } else {
                        let x1 = vm.x - width / 2 + width,
                            y1 = vm.y,
                            x2 = x1 + width,
                            y2 = y1 - height / 2,
                            x3 = x2,
                            y3 = y2 + height;
                    }

                    ctx.beginPath();
                    ctx.moveTo(x1, y1);
                    ctx.lineTo(x2, y2);
                    ctx.lineTo(x3, y3);
                    ctx.fill();
                    ctx.restore();
                }
                if (shape == "inverted-triangle") {

                    if (horizontal) {
                        let x1 = me._view.x = vm.head,
                            y1 = vm.y - height / 2,
                            x2 = x1 - width / 2,
                            y2 = y1 + height,
                            x3 = x2 + width,
                            y3 = y2;
                    } else {
                        let x1 = vm.x + width / 2 + width,
                            y1 = vm.y,
                            x2 = x1 - width,
                            y2 = y1 - height / 2,
                            x3 = x2,
                            y3 = y2 + height;
                    }

                    ctx.beginPath();
                    ctx.moveTo(x1, y1);
                    ctx.lineTo(x2, y2);
                    ctx.lineTo(x3, y3);
                    ctx.fill();
                    ctx.restore();
                }
                if (shape == "bowtie") {
                    if (horizontal) {

                        let x1 = me._view.x = vm.head,
                            y1 = vm.y + width,
                            x2 = x1 - height / 2,
                            y2 = y1 - width / 2,
                            x3 = x2 + height,
                            y3 = y2;

                        let x11 = vm.head,
                            y11 = vm.y + width,
                            x21 = x11 - height / 2,
                            y21 = y11 + width / 2,
                            x31 = x21 + height,
                            y31 = y21;
                    } else {

                        let x1 = vm.x,
                            y1 = vm.y,
                            x2 = x1 + width / 2,
                            y2 = y1 - height / 2,
                            x3 = x2,
                            y3 = y2 + height;

                        let x11 = vm.x,
                            y11 = vm.y,
                            x21 = x11 - width / 2,
                            y21 = y11 - height / 2,
                            x31 = x21,
                            y31 = y21 + height;
                    }

                    ctx.beginPath();
                    ctx.moveTo(x1, y1);
                    ctx.lineTo(x2, y2);
                    ctx.lineTo(x3, y3);
                    ctx.closePath();
                    ctx.fill();
                    ctx.beginPath();
                    ctx.lineTo(x11, y11);
                    ctx.lineTo(x21, y21);
                    ctx.lineTo(x31, y31);
                    ctx.fill();
                    ctx.restore();
                }
                if (shape == "diamond") {
                    if (horizontal) {

                        let x1 = me._view.x = vm.head,
                            y1 = vm.y - width / 2 + width,
                            x2 = x1 - height / 2,
                            y2 = y1 + width / 2 + 0.5,
                            x3 = x2 + height,
                            y3 = y2;

                        let x11 = vm.head,
                            y11 = vm.y + width / 2 + width,
                            x21 = x11 - height / 2,
                            y21 = y11 - width / 2,
                            x31 = x21 + height,
                            y31 = y21;
                    } else {

                        let x1 = vm.x - width / 2,
                            y1 = vm.y,
                            x2 = x1 + width / 2 + 0.5,
                            y2 = y1 - height / 2,
                            x3 = x2,
                            y3 = y2 + height;

                        let x11 = vm.x + width / 2,
                            y11 = vm.y,
                            x21 = x11 - width / 2,
                            y21 = y11 - height / 2,
                            x31 = x21,
                            y31 = y21 + height;
                    }

                    ctx.beginPath();
                    ctx.moveTo(x1, y1);
                    ctx.lineTo(x2, y2);
                    ctx.lineTo(x3, y3);
                    ctx.closePath();
                    ctx.fill();
                    ctx.beginPath();
                    ctx.lineTo(x11, y11);
                    ctx.lineTo(x21, y21);
                    ctx.lineTo(x31, y31);
                    ctx.fill();
                    ctx.restore();
                }


            }

            if (opts.pointer === "text") {
                let rotate = opts.rotate ? opts.rotate : defaults.rotate;
                let text = opts.text ? opts.text : defaults.text;
                let fontSize = opts.fontSize ? opts.fontSize : defaults.fontSize;
                let fontFamily = opts.fontFamily ? opts.fontFamily : defaults.fontFamily;
                let offset = opts.offset ? opts.offset : defaults.offset;
                let color = opts.color ? opts.color : defaults.color;

                if (typeof opts.textRanges !== "undefined" && typeof opts.textRanges.length !== "undefined" && opts.textRanges.length > 0) {
                    for (let i in opts.textRanges) {
                        let r = opts.textRanges[i];
                        if (me._model.value >= r.startpoint && me._model.value < r.breakpoint && typeof r.text !== "undefined" && r.text !== "") {
                            text = r.text;
                            break;
                        }
                    }
                }

                // Stroke Line
                ctx.beginPath();
                ctx.font = fontSize + "px " + fontFamily;
                let arrayOfThings = [];
                arrayOfThings.push(text);
                let tlen = helpers.longestText(ctx, ctx.font, arrayOfThings);
                if (horizontal) vm.x = me._view.x = vm.head;
                if (typeof opts.textPosition !== "undefined" && opts.textPosition === "center") {
                    ctx.translate(vm.x - tlen / 2, vm.y + fontSize / 3);
                } else if (typeof opts.textPosition !== "undefined" && opts.textPosition === "right") {
                    ctx.translate(vm.x - tlen, vm.y + fontSize / 3);
                } else {
                    ctx.translate(vm.x, vm.y + fontSize / 3);
                }

                ctx.rotate(Math.PI * 2 * (rotate / 360));
                //ctx.fillStyle = color;
                //ctx.textAlign = "center";
                ctx.fillText(text, 0, 0);
                ctx.restore();

            }

        },

        tooltipPosition: function () {

            let opts = this.getMeOptions();
            let defaults = this._chart.options.elements.gaugerect;
            let shape = opts.shape ? opts.shape : defaults.shape;

            if (typeof opts.img !== "undefined" && opts.img !== null) {
                let vm = this._view;
                if (this._model.horizontal) {
                    let x = vm.x;
                    let y = vm.y + vm.height / 2;
                } else {
                    let x = vm.x;
                    let y = vm.y - vm.height / 2;
                }

                return {
                    x: x,
                    y: y
                };
            }

            if (this._view && (typeof opts.pointer === "undefined" || opts.pointer === "bar")) {
                let vm = this._view;
                return {
                    x: vm.x + (this._model.horizontal ? vm.width : vm.width / 2),
                    y: vm.y + (this._model.horizontal ? vm.height / 2 : 0),
                };
            }

            if (this._view && typeof opts.pointer !== "undefined" && opts.pointer === "point") {
                let vm = this._view;
                let x = vm.x;
                let y = vm.y;
                if ((shape === "triangle" || shape === "inverted-triangle") && !this._model.horizontal)
                    x = vm.x + vm.width;
                y = vm.y;
                if ((shape === "triangle" || shape === "inverted-triangle") && this._model.horizontal)
                    x = vm.x;
                y = vm.y;
                return {
                    x: x,
                    y: y
                };
            }


        },

        inRange: function (mouseX, mouseY) {
            let inRange = false;
            let opts = this.getMeOptions();
            let defaults = this._chart.options.elements.gaugerect;
            let shape = opts.shape ? opts.shape : defaults.shape;

            if (typeof opts.img !== "undefined" && opts.img !== null) {
                let vm = this._view;
                if (this._model.horizontal)
                    inRange = mouseX >= vm.x - vm.width / 2 && mouseX <= vm.x + vm.width / 2 && mouseY >= vm.y + vm.height / 2 && mouseY <= vm.y + vm.height + vm.height / 2;
                else
                    inRange = mouseX >= vm.x - vm.width / 2 && mouseX <= vm.x + vm.width / 2 && mouseY >= vm.y - vm.height / 2 && mouseY <= vm.y + vm.height / 2;
                return inRange;
            }

            if (this._view && (typeof opts.pointer === "undefined" || opts.pointer === "bar")) {
                let vm = this._view;
                if (vm.width >= 0 && vm.height >= 0)
                    inRange = mouseX >= vm.x && mouseX <= vm.x + vm.width && mouseY >= vm.y && mouseY <= vm.y + vm.height;
                if (vm.width < 0 && vm.height >= 0)
                    inRange = mouseX >= (vm.x + vm.width) && mouseX <= vm.x && mouseY >= vm.y && mouseY <= vm.y + vm.height;
                if (vm.width >= 0 && vm.height < 0)
                    inRange = mouseX >= vm.x && mouseX <= vm.x + vm.width && mouseY >= vm.y + vm.height && mouseY <= vm.y;
                if (vm.width < 0 && vm.height < 0)
                    inRange = mouseX >= (vm.x + vm.width) && mouseX <= vm.x && mouseY >= vm.y + vm.height && mouseY <= vm.y;
            }
            if (this._view && typeof opts.pointer !== "undefined" && opts.pointer === "point") {
                let vm = this._view;
                inRange = mouseX >= vm.x - vm.width / 2 && mouseX <= vm.x + vm.width / 2 && mouseY >= vm.y - vm.height / 2 && mouseY <= vm.y + vm.height / 2;
                if ((shape === "triangle" || shape === "inverted-triangle") && !this._model.horizontal)
                    inRange = mouseX >= vm.x + vm.width / 2 && mouseX <= vm.x + vm.width + vm.width / 2 && mouseY >= vm.y - vm.height / 2 && mouseY <= vm.y + vm.height / 2;
                if ((shape === "triangle" || shape === "inverted-triangle") && this._model.horizontal)
                    inRange = mouseX >= vm.x - vm.width / 2 && mouseX <= vm.x + vm.width / 2 && mouseY >= vm.y - vm.height / 2 && mouseY <= vm.y + vm.height / 2;

            }

            return inRange;
        },

    });

}).call(this, Chart);


(function (Chart) {
    let helpers = Chart.helpers;
    let plugins = Chart.plugins;
    Chart.defaults.global.animation.duration = 1000;


    Chart.defaults._set("linearGauge", {
        scale: {
            type: "linearGauge",
            horizontal: false,
            range: {
                startValue: -100,
                endValue: 500
            },
            responsive: true,
            font: {
                fontName: "Arial",
                fontSize: 12
            },
            axisWidth: 6,
            ticks: {
                majorTicks: {
                    interval: 100,
                    height: 1,
                }
            },
            scaleLabel: {
                display: true,
                interval: 100,
                units: "",
                customValues: [],
                offset: -10,
                color: "#777b80"
            }
        },
        padding: {
            top: 0,
            bottom: 0,
            left: 0,
            right: 0
        },
        tooltips: {
            callbacks: {
                label: function (tooltipItem, data) {
                    let label = data.datasets[tooltipItem.datasetIndex].label || "";

                    if (label) {
                        label += ": ";
                    }
                    label += Math.round(data.datasets[tooltipItem.datasetIndex].data[0] * 100) / 100;
                    return label;
                }
            }
        },
        legend: {
            display: true,
            labels: {
                fontColor: "rgb(0, 0, 0)"
            },
            position: "bottom"
        }
    });

    Chart.controllers.linearGauge = Chart.DatasetController.extend({

        dataElementType: Chart.elements.Gaugerect,

        initialize: function () {
            let me = this;
            let meta;

            Chart.DatasetController.prototype.initialize.apply(me, arguments);

            meta = me.getMeta();

        },

        linkScales: helpers.noop,

        update: function (reset) {
            let me = this;
            let rects = me.getMeta().data;
            let i, ilen;
            me.datashifts = 0;

            for (i = 0, ilen = rects.length; i < ilen; ++i) {
                me.updateElement(rects[i], i, me.datashifts);
                me.datashifts += 10;
            }
        },

        updateElement: function (rectangle, index, reset) {
            let me = this;
            let chart = me.chart;
            let meta = me.getMeta();
            let dataset = me.getDataset();

            let custom = rectangle.custom || {};
            let rectangleOptions = chart.options.elements.rectangle;
            let gaugeOptions = chart.options.elements.gaugerect;
            rectangle._Scale = me.getScaleForId(chart.options.scale.id || "gaugescale");
            rectangle._datasetIndex = me.index;
            rectangle._index = index;
            rectangle.rangeColorImage = null;

            //	Init element model
            rectangle._model = {
                datasetLabel: dataset.label,
                label: chart.data.labels[index],
                borderSkipped: custom.borderSkipped ? custom.borderSkipped : rectangleOptions.borderSkipped,
                backgroundColor: custom.backgroundColor ? custom.backgroundColor : helpers.valueAtIndexOrDefault(dataset.backgroundColor, index, gaugeOptions.backgroundColor),
                borderColor: custom.borderColor ? custom.borderColor : helpers.valueAtIndexOrDefault(dataset.borderColor, index, rectangleOptions.borderColor),
                borderWidth: custom.borderWidth ? custom.borderWidth : helpers.valueAtIndexOrDefault(dataset.borderWidth, index, rectangleOptions.borderWidth)
            };

            //	Set empty view as start point for animation
            if (typeof rectangle._view === "undefined") rectangle._view = {};

            me.updateElementGeometry(rectangle, index, reset);

        },

        updateElementGeometry: function (rectangle, index, reset) {
            let me = this;
            let model = rectangle._model;
            let start = rectangle._view;
            let dataset = me.getDataset().data;
            let dopt = me.getDataset();
            let chart = me.chart;
            let datasets = chart.data.datasets;
            let gaugeOptions = chart.options.elements.gaugerect;
            let vscale = me.getScaleForId(chart.options.scale.id || "gaugescale");
            //let base = vscale.getBasePixel();
            let base = vscale.getBase();
            let horizontal = rectangle._Scale.isHorizontal();
            //let ruler = me._ruler || me.getRuler();
            let vpixels = me.calculateBarValuePixels(me.index, index, horizontal);

            model.horizontal = horizontal;
            model.base = base;
            model.head = vpixels.head;
            model.x = horizontal ? vpixels.base : vpixels.offset;
            model.y = horizontal ? (vpixels.offset - (dopt.width || gaugeOptions.width)) : vpixels.head;
            model.height = horizontal ? (dopt.width || gaugeOptions.width) : (vpixels.base - vpixels.head);
            model.width = horizontal ? (vpixels.head - vpixels.base) : (dopt.width || gaugeOptions.width);
            model.value = vscale.getRightValue(datasets[me.index].data[index]);

            model.scaleValue = 0;
            if (horizontal) {
                model.scaleValue = vscale.width / (vscale.options.range.endValue - vscale.options.range.startValue);
            } else {
                model.scaleValue = vscale.height / (vscale.options.range.endValue - vscale.options.range.startValue);
            }

            if (typeof start.x === "undefined" && typeof start.y === "undefined") {
                if (horizontal) {
                    start.x = vpixels.base;
                    start.width = 0;
                } else {
                    start.y = vpixels.base;
                    start.height = 0;
                }
            }

        },

        calculateBarValuePixels: function (datasetIndex, index, horizontal) {
            let me = this;
            let chart = me.chart;
            let scale = me.getScaleForId(chart.options.scale.id || "gaugescale");
            let datasets = chart.data.datasets;
            let dopt = datasets[datasetIndex];
            let value = scale.getRightValue(datasets[datasetIndex].data[index]);
            let stacked = scale.options.stacked;
            let start = 0;
            let i, imeta, ivalue, base, head, size, offset;

            base = scale.scalePoint(start);
            head = scale.scalePoint(start + value);
            size = (head - base) / 2;
            offset = horizontal ? scale.yCenter - dopt.offset : scale.xCenter + dopt.offset;

            return {
                size: size,
                base: base,
                head: head,
                center: head + size / 2,
                offset: offset
            };
        },

        draw: function () {
            let me = this;
            let chart = me.chart;
            let rects = me.getMeta().data;
            let dataset = me.getDataset();
            let ilen = rects.length;
            let i = 0;

            helpers.canvas.clipArea(chart.ctx, chart.chartArea);

            for (; i < ilen; ++i) {
                if (!isNaN(dataset.data[i])) {
                    rects[i].draw();
                }
            }

            helpers.canvas.unclipArea(chart.ctx);
        },

        setHoverStyle: function (rectangle) {
            let dataset = this.chart.data.datasets[rectangle._datasetIndex];
            let index = rectangle._index;
            let custom = rectangle.custom || {};
            let model = rectangle._model;

            model.backgroundColor = custom.hoverBackgroundColor ? custom.hoverBackgroundColor : helpers.valueAtIndexOrDefault(dataset.hoverBackgroundColor, index, helpers.getHoverColor(model.backgroundColor));
            model.borderColor = custom.hoverBorderColor ? custom.hoverBorderColor : helpers.valueAtIndexOrDefault(dataset.hoverBorderColor, index, helpers.getHoverColor(model.borderColor));
            model.borderWidth = custom.hoverBorderWidth ? custom.hoverBorderWidth : helpers.valueAtIndexOrDefault(dataset.hoverBorderWidth, index, model.borderWidth);
        },

        removeHoverStyle: function (rectangle) {
            let dataset = this.chart.data.datasets[rectangle._datasetIndex];
            let index = rectangle._index;
            let custom = rectangle.custom || {};
            let model = rectangle._model;
            let rectangleElementOptions = this.chart.options.elements.gaugerect;

            model.backgroundColor = custom.backgroundColor ? custom.backgroundColor : helpers.valueAtIndexOrDefault(dataset.backgroundColor, index, rectangleElementOptions.backgroundColor);
            model.borderColor = custom.borderColor ? custom.borderColor : helpers.valueAtIndexOrDefault(dataset.borderColor, index, rectangleElementOptions.borderColor);
            model.borderWidth = custom.borderWidth ? custom.borderWidth : helpers.valueAtIndexOrDefault(dataset.borderWidth, index, rectangleElementOptions.borderWidth);
        }

    });
}).call(this, Chart);
