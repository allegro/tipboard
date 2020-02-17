// https://github.com/kluverua/Chartjs-tsgauge/blob/master/Gauge.js
(function () {
	if (!window.Chart) {
		return;
	}
	function GaugeChartHelper() {
	}
	GaugeChartHelper.prototype.setup = function(chart, config) {
		this.chart = chart;
		this.ctx = chart.ctx;
		this.limits = config.data.datasets[0].gaugeLimits;
		this.data = config.data.datasets[0].gaugeData;
		let options = chart.options;
		this.fontSize = options.defaultFontSize;
		this.fontStyle = options.defaultFontFamily;
		this.fontColor = options.defaultFontColor;
		this.ctx.textBaseline = "alphabetic";
		this.arrowAngle = 25 * Math.PI / 180;
		this.arrowColor = config.options.indicatorColor || options.arrowColor;
		this.showMarkers = typeof(config.options.showMarkers) === 'undefined' ? true : config.options.showMarkers;
		if (config.options.markerFormatFn) {
			this.markerFormatFn = config.options.markerFormatFn;
		} else {
			this.markerFormatFn = function(value) {
				return value;
			}
		}
	};
	GaugeChartHelper.prototype.applyGaugeConfig = function(chartConfig) {
		this.calcLimits();
		chartConfig.data.datasets[0].data = this.doughnutData;
		let ctx = this.ctx;
		let labelsWidth = this.limits.map(function(label){
			let text = this.markerFormatFn(label);
			return ctx.measureText(text).width;
		}.bind(this));
		let padding = Math.max.apply(this, labelsWidth) + this.chart.width / 35;
		let heightRatio = this.chart.height / 50;
		chartConfig.options.layout.padding = {
			top: this.fontSize + heightRatio,
			left: padding,
			right: padding,
			bottom: heightRatio * 2
		};
	};
	GaugeChartHelper.prototype.calcLimits = function() {
		let limits = this.limits;
		let data = [];
		let total = 0;
		for (let i = 1, ln = limits.length; i < ln; i++) {
			let dataValue = Math.abs(limits[i] - limits[i - 1]);
			total += dataValue;
			data.push(dataValue);
		}
		this.doughnutData = data;
		let minValue = limits[0];
		let maxValue = limits[limits.length - 1];
		this.isRevers = minValue > maxValue;
		this.minValue = this.isRevers ? maxValue : minValue;
		this.totalValue = total;
	};
	GaugeChartHelper.prototype.updateGaugeDimensions = function() {
		let chartArea = this.chart.chartArea;
		this.gaugeRadius = this.chart.innerRadius;
		this.gaugeCenterX = (chartArea.left + chartArea.right) / 2;
		this.gaugeCenterY = (chartArea.top + chartArea.bottom + this.chart.outerRadius) / 2;
		this.arrowLength = this.chart.radiusLength * 2;
	};
	GaugeChartHelper.prototype.getCoordOnCircle = function(r, alpha) {
		return {
			x: r * Math.cos(alpha),
			y: r * Math.sin(alpha)
		};
	};
	GaugeChartHelper.prototype.getAngleOfValue = function(value) {
		let result = 0;
		let gaugeValue = value - this.minValue;
		if (gaugeValue <= 0) {
			result = 0;
		} else if (gaugeValue >= this.totalValue) {
			result = Math.PI;
		} else {
			result = Math.PI * gaugeValue / this.totalValue;
		}
		if (this.isRevers) {
			return Math.PI - result;
		} else {
			return result;
		}
	};
	GaugeChartHelper.prototype.renderLimitLabel = function(value) {
		let ctx = this.ctx;
		let angle = this.getAngleOfValue(value);
		let coord = this.getCoordOnCircle(this.chart.outerRadius + (this.chart.radiusLength / 2), angle);
		let align;
		let diff = angle - (Math.PI / 2);
		if (diff > 0) {
			align = "left";
		} else if (diff < 0) {
			align = "right";
		} else {
			align = "center";
		}
		ctx.textAlign = align;
		ctx.font = this.fontSize + "px " + this.fontStyle;
		ctx.fillStyle = this.fontColor;
		let text = this.markerFormatFn(value);
		ctx.fillText(text, this.gaugeCenterX - coord.x, this.gaugeCenterY - coord.y);
	};
	GaugeChartHelper.prototype.renderLimits = function() {
		for (let i = 0, ln = this.limits.length; i < ln; i++) {
			this.renderLimitLabel(this.limits[i]);
		}
	};
	GaugeChartHelper.prototype.renderValueLabel = function() {
		let label = this.data.value.toString();
		let ctx = this.ctx;
		ctx.font = "30px " + this.fontStyle;
		let stringWidth = ctx.measureText(label).width;
		let elementWidth = 0.75 * this.gaugeRadius * 2;
		let widthRatio = elementWidth / stringWidth;
		let newFontSize = Math.floor(30 * widthRatio);
		let fontSizeToUse = Math.min(newFontSize, this.gaugeRadius);
		ctx.textAlign = "center";
		ctx.font = fontSizeToUse + "px " + this.fontStyle;
		ctx.fillStyle = this.data.valueColor || this.fontColor;
		ctx.fillText(label, this.gaugeCenterX, this.gaugeCenterY);
	};
	GaugeChartHelper.prototype.renderValueArrow = function(value) {
		let angle = this.getAngleOfValue(typeof value === "number" ? value : this.data.value);
		this.ctx.globalCompositeOperation = "source-over";
		this.renderArrow(this.gaugeRadius, angle, this.arrowLength, this.arrowAngle, this.arrowColor);
	};
	GaugeChartHelper.prototype.renderSmallValueArrow = function(value) {
		let angle = this.getAngleOfValue(value);
		this.ctx.globalCompositeOperation = "source-over";
		this.renderArrow(this.gaugeRadius - 1, angle, this.arrowLength - 1, this.arrowAngle, this.arrowColor);
	};
	GaugeChartHelper.prototype.clearValueArrow = function(value) {
		let angle = this.getAngleOfValue(value);
		this.ctx.lineWidth = 2;
		this.ctx.globalCompositeOperation = "destination-out";
		this.renderArrow(this.gaugeRadius - 1, angle, this.arrowLength + 1, this.arrowAngle, "#FFFFFF");
		this.ctx.stroke();
	};
	GaugeChartHelper.prototype.renderArrow = function(radius, angle, arrowLength, arrowAngle, arrowColor) {
		let coord = this.getCoordOnCircle(radius, angle);
		let arrowPoint = {
			x: this.gaugeCenterX - coord.x,
			y: this.gaugeCenterY - coord.y
		};
		let ctx = this.ctx;
		ctx.fillStyle = arrowColor;
		ctx.beginPath();
		ctx.moveTo(arrowPoint.x, arrowPoint.y);
		coord = this.getCoordOnCircle(arrowLength, angle + arrowAngle);
		ctx.lineTo(arrowPoint.x + coord.x, arrowPoint.y + coord.y);
		coord = this.getCoordOnCircle(arrowLength, angle - arrowAngle);
		ctx.lineTo(arrowPoint.x + coord.x, arrowPoint.y + coord.y);
		ctx.closePath();
		ctx.fill();
	};
	GaugeChartHelper.prototype.animateArrow = function() {
		let stepCount = 30;
		let animateTimeout = 300;
		let gaugeValue = this.data.value - this.minValue;
		let step = gaugeValue / stepCount;
		let i = 0;
		let currentValue = this.minValue;
		let interval = setInterval(function() {
			i++;
			this.clearValueArrow(currentValue);
			if (i > stepCount) {
				clearInterval(interval);
				this.renderValueArrow();
			} else {
				currentValue += step;
				this.renderSmallValueArrow(currentValue);
			}
		}.bind(this), animateTimeout / stepCount);
	};
	Chart.defaults.tsgauge = {
		animation: {
			animateRotate: true,
			animateScale: false
		},
		cutoutPercentage: 95,
		rotation: Math.PI,
		circumference: Math.PI,
		legend: {
			display: false
		},
		scales: {},
		arrowColor: "#444"
	};
	Chart.controllers.tsgauge = Chart.controllers.doughnut.extend({
		initialize: function(chart) {
			let gaugeHelper = this.gaugeHelper = new GaugeChartHelper();
			gaugeHelper.setup(chart, chart.config);
			gaugeHelper.applyGaugeConfig(chart.config);
			chart.config.options.animation.onComplete = function(chartElement) {
				gaugeHelper.updateGaugeDimensions();
				gaugeHelper.animateArrow();
			};
			Chart.controllers.doughnut.prototype.initialize.apply(this, arguments);
		},
		draw: function() {
			Chart.controllers.doughnut.prototype.draw.apply(this, arguments);
			let gaugeHelper = this.gaugeHelper;
			gaugeHelper.updateGaugeDimensions();
			gaugeHelper.renderValueLabel();
			if (gaugeHelper.showMarkers) {
				gaugeHelper.renderLimits();
			}
			gaugeHelper.renderSmallValueArrow(gaugeHelper.minValue);
		}
	});
})();
