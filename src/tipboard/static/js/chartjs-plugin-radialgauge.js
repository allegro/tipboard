// https://github.com/pandameister/chartjs-chart-radial-gauge
// MIT License
//
// Copyright (c) 2018 Patrice Pominville
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory(require('chart.js')) :
  typeof define === 'function' && define.amd ? define(['chart.js'], factory) :
  (global.ChartjsRadialGauge = factory(global.Chart));
}(this, (function (Chart) { 'use strict';

  var Chart__default = 'default' in Chart ? Chart['default'] : Chart;

  /**
   * An arc element that supports rounded corners
   */
  Chart.elements.RoundedArc = Chart.elements.Arc.extend({
    draw: function draw() {
      var ctx = this._chart.ctx;
      var vm = this._view;
      var startAngle = vm.startAngle,
          endAngle = vm.endAngle;

      var cornerRadius = (vm.outerRadius - vm.innerRadius) / 2;
      var cornerX = (vm.outerRadius + vm.innerRadius) / 2;

      // translate + rotate to make drawing the corners simpler
      ctx.translate(vm.x, vm.y);
      ctx.rotate(startAngle);
      var angle = endAngle - startAngle;
      ctx.beginPath();
      if (vm.roundedCorners) {
        ctx.arc(cornerX, 0, cornerRadius, Math.PI, 0);
      }
      ctx.arc(0, 0, vm.outerRadius, 0, angle);

      var x = cornerX * Math.cos(angle);
      var y = cornerX * Math.sin(angle);

      if (vm.roundedCorners) {
        ctx.arc(x, y, cornerRadius, angle, angle + Math.PI);
      }

      ctx.arc(0, 0, vm.innerRadius, angle, 0, true);
      ctx.closePath();
      ctx.rotate(-startAngle);
      ctx.translate(-vm.x, -vm.y);

      ctx.strokeStyle = vm.borderColor;
      ctx.lineWidth = vm.borderWidth;
      ctx.fillStyle = vm.backgroundColor;

      ctx.fill();
      ctx.lineJoin = 'bevel';

      if (vm.borderWidth) {
        ctx.stroke();
      }
    }
  });

  Chart.elements.RoundedArc;

  var slicedToArray = function () {
    function sliceIterator(arr, i) {
      var _arr = [];
      var _n = true;
      var _d = false;
      var _e = undefined;

      try {
        for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) {
          _arr.push(_s.value);

          if (i && _arr.length === i) break;
        }
      } catch (err) {
        _d = true;
        _e = err;
      } finally {
        try {
          if (!_n && _i["return"]) _i["return"]();
        } finally {
          if (_d) throw _e;
        }
      }

      return _arr;
    }

    return function (arr, i) {
      if (Array.isArray(arr)) {
        return arr;
      } else if (Symbol.iterator in Object(arr)) {
        return sliceIterator(arr, i);
      } else {
        throw new TypeError("Invalid attempt to destructure non-iterable instance");
      }
    };
  }();

  var helpers = Chart__default.helpers;

  /**
   * Controller for the radialGauge chart type
   */

  Chart__default.defaults._set('radialGauge', {
    animation: {
      // Boolean - Whether we animate the rotation of the radialGauge
      animateRotate: true,
      // Boolean - Whether we animate scaling the radialGauge from the centre
      animateScale: true
    },

    // The percentage of the chart that is the center area
    centerPercentage: 80,

    // The rotation for the start of the metric's arc
    rotation: -Math.PI / 2,

    // the color of the radial gauge's track
    trackColor: 'rgb(204, 221, 238)',

    // whether arc for the gauge should have rounded corners
    roundedCorners: true,

    // center value options
    centerArea: {
      // whether to display the center text value
      displayText: true,
      // font for the center text
      fontFamily: null,
      // color of the center text
      fontColor: null,
      // the size of the center text
      fontSize: null,
      // padding around the center area
      padding: 4,
      // an image to use for the center background
      backgroundImage: null,
      // a color to use for the center background
      backgroundColor: null,
      // the text to display in the center
      // this could be a string or a callback that returns a string
      // if a callback is provided it will be called with (value, options)
      text: null
    },

    hover: {
      mode: 'single'
    },

    legend: {
      display: false
    },

    // the domain of the metric
    domain: [0, 100],

    tooltips: {
      callbacks: {
        title: function title() {
          return '';
        },
        label: function label(tooltipItem, data) {
          var dataLabel = data.labels[tooltipItem.index];
          var value = ': ' + data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];

          dataLabel += value;

          return dataLabel;
        }
      }
    }
  });

  // eslint-disable-next-line no-shadow
  var RadialGaugeController = (function (Chart$$1) {
    Chart$$1.controllers.radialGauge = Chart$$1.DatasetController.extend({
      dataElementType: Chart$$1.elements.RoundedArc,

      linkScales: helpers.noop,

      draw: function draw() {
        this.drawTrack();

        this.drawCenterArea();

        for (var _len = arguments.length, args = Array(_len), _key = 0; _key < _len; _key++) {
          args[_key] = arguments[_key];
        }

        Chart$$1.DatasetController.prototype.draw.apply(this, args);
      },
      drawTrack: function drawTrack() {
        new Chart$$1.elements.Arc({
          _view: {
            backgroundColor: this.chart.options.trackColor,
            borderColor: this.chart.options.trackColor,
            startAngle: 0,
            endAngle: Math.PI * 2,
            x: this.centerX,
            y: this.centerY,
            innerRadius: this.innerRadius,
            outerRadius: this.outerRadius,
            borderWidth: this.borderWidth
          },
          _chart: this.chart
        }).draw();
      },
      drawCenterArea: function drawCenterArea() {
        var ctx = this.chart.ctx;
        var drawInfo = {
          ctx: ctx,
          value: Math.ceil(this.getMeta().data[0]._view.value),
          radius: this.innerRadius,
          options: this.chart.options.centerArea
        };

        ctx.save();

        try {
          ctx.translate(this.centerX, this.centerY);
          if (drawInfo.options.draw) {
            drawInfo.options.draw(drawInfo);
            return;
          }

          if (drawInfo.options.backgroundColor) {
            this.drawCenterBackground(drawInfo);
          }

          if (drawInfo.options.backgroundImage) {
            this.drawCenterImage(drawInfo);
          }

          if (drawInfo.options.displayText) {
            this.drawCenterText(drawInfo);
          }
        } finally {
          ctx.restore();
        }
      },
      drawCenterBackground: function drawCenterBackground(_ref) {
        var options = _ref.options,
            radius = _ref.radius,
            ctx = _ref.ctx;

        var bgRadius = radius - options.padding;
        ctx.beginPath();
        ctx.arc(0, 0, bgRadius, 0, Math.PI * 2);
        ctx.closePath();
        ctx.fillStyle = options.backgroundColor;
        ctx.fill();
      },
      drawCenterImage: function drawCenterImage(_ref2) {
        var radius = _ref2.radius,
            options = _ref2.options,
            ctx = _ref2.ctx;

        var imageRadius = radius - options.padding;
        ctx.beginPath();
        ctx.arc(0, 0, imageRadius, 0, Math.PI * 2, true);
        ctx.closePath();
        ctx.clip();
        ctx.drawImage(options.backgroundImage, -imageRadius, -imageRadius, 2 * imageRadius, 2 * imageRadius);
      },
      drawCenterText: function drawCenterText(_ref3) {
        var options = _ref3.options,
            value = _ref3.value;

        var fontSize = options.fontSize || (this.innerRadius / 50).toFixed(2) + 'em';
        var fontFamily = options.fontFamily || Chart$$1.defaults.global.defaultFontFamily;
        var color = options.fontColor || Chart$$1.defaults.global.defaultFontColor;

        var text = typeof options.text === 'function' ? options.text(value, options) : options.text;
        text = text || '' + value;
        this.chart.ctx.font = fontSize + ' ' + fontFamily;
        this.chart.ctx.fillStyle = color;
        this.chart.ctx.textBaseline = 'middle';
        var textWidth = this.chart.ctx.measureText(text).width;
        var textX = Math.round(-textWidth / 2);

        // only display the text if it fits
        if (textWidth < 2 * this.innerRadius * 0.8) {
          this.chart.ctx.fillText(text, textX, 0);
        }
      },
      update: function update(reset) {
        var _this = this;

        var chart = this.chart;
        var chartArea = chart.chartArea;
        var opts = chart.options;
        var arcOpts = opts.elements.arc;
        var availableWidth = chartArea.right - chartArea.left - arcOpts.borderWidth;
        var availableHeight = chartArea.bottom - chartArea.top - arcOpts.borderWidth;
        var availableSize = Math.min(availableWidth, availableHeight);

        var meta = this.getMeta();
        var centerPercentage = opts.centerPercentage;

        this.borderWidth = this.getMaxBorderWidth(meta.data);
        this.outerRadius = Math.max((availableSize - this.borderWidth) / 2, 0);
        this.innerRadius = Math.max(centerPercentage ? this.outerRadius / 100 * centerPercentage : 0, 0);

        meta.total = this.getMetricValue();
        this.centerX = (chartArea.left + chartArea.right) / 2;
        this.centerY = (chartArea.top + chartArea.bottom) / 2;

        helpers.each(meta.data, function (arc, index) {
          _this.updateElement(arc, index, reset);
        });
      },
      updateElement: function updateElement(arc, index, reset) {
        var chart = this.chart;
        var chartArea = chart.chartArea;
        var opts = chart.options;
        var animationOpts = opts.animation;
        var centerX = (chartArea.left + chartArea.right) / 2;
        var centerY = (chartArea.top + chartArea.bottom) / 2;
        var startAngle = opts.rotation; // non reset case handled later
        var dataset = this.getDataset();
        var arcAngle = reset && animationOpts.animateRotate ? 0 : this.calculateArcAngle(dataset.data[index]);
        var value = reset && animationOpts.animateScale ? 0 : this.getMetricValue();
        var endAngle = startAngle + arcAngle;
        var innerRadius = this.innerRadius;
        var outerRadius = this.outerRadius;
        var valueAtIndexOrDefault = helpers.valueAtIndexOrDefault;

        helpers.extend(arc, {
          // Utility
          _datasetIndex: this.index,
          _index: index,

          // Desired view properties
          _model: {
            x: centerX,
            y: centerY,
            startAngle: startAngle,
            endAngle: endAngle,
            outerRadius: outerRadius,
            innerRadius: innerRadius,
            label: valueAtIndexOrDefault(dataset.label, index, chart.data.labels[index]),
            roundedCorners: opts.roundedCorners,
            value: value
          }
        });

        var model = arc._model;

        // Resets the visual styles
        var custom = arc.custom || {};
        var valueOrDefault = helpers.valueAtIndexOrDefault;
        var elementOpts = this.chart.options.elements.arc;
        model.backgroundColor = custom.backgroundColor ? custom.backgroundColor : valueOrDefault(dataset.backgroundColor, index, elementOpts.backgroundColor);
        model.borderColor = custom.borderColor ? custom.borderColor : valueOrDefault(dataset.borderColor, index, elementOpts.borderColor);
        model.borderWidth = custom.borderWidth ? custom.borderWidth : valueOrDefault(dataset.borderWidth, index, elementOpts.borderWidth);

        arc.pivot();
      },
      getMetricValue: function getMetricValue() {
        var value = this.getDataset().data[0];
        if (value == null) {
          value = this.chart.options.domain[0];
        }

        return value;
      },
      getDomain: function getDomain() {
        return this.chart.options.domain;
      },
      calculateArcAngle: function calculateArcAngle() {
        var _getDomain = this.getDomain(),
            _getDomain2 = slicedToArray(_getDomain, 2),
            domainStart = _getDomain2[0],
            domainEnd = _getDomain2[1];

        var value = this.getMetricValue();
        var domainSize = domainEnd - domainStart;

        return domainSize > 0 ? Math.PI * 2.0 * (Math.abs(value - domainStart) / domainSize) : 0;
      },


      // gets the max border or hover width to properly scale pie charts
      getMaxBorderWidth: function getMaxBorderWidth(arcs) {
        var max = 0;
        var index = this.index;
        var length = arcs.length;
        var borderWidth = void 0;
        var hoverWidth = void 0;

        for (var i = 0; i < length; i++) {
          borderWidth = arcs[i]._model ? arcs[i]._model.borderWidth : 0;
          hoverWidth = arcs[i]._chart ? arcs[i]._chart.config.data.datasets[index].hoverBorderWidth : 0;

          max = borderWidth > max ? borderWidth : max;
          max = hoverWidth > max ? hoverWidth : max;
        }
        return max;
      }
    });
  });

  var RadialGaugeChart = (function (Chart$$1) {
    Chart$$1.RadialGauge = function (context, config) {
      config.type = 'radialGauge';

      return new Chart$$1(context, config);
    };
  });

  RadialGaugeController(Chart__default);
  RadialGaugeChart(Chart__default);

  return RadialGaugeChart;

})));
