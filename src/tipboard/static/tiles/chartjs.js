/**
 * PieChart Plugin to see % inside the pie
 * @returns {{formatter: (function(*, *): string)}}
 * @constructor
 */
function pieChartPluginPercentge() {
    return {
        formatter: (value, ctx) => {
            let sum = 0;
            let dataArr = ctx.chart.data.datasets[0].data;
            dataArr.map((data) => {
                sum += data;
            });
            return (value * 100 / sum).toFixed(2) + "%";
        }
    };
}

/**
 * Update for tile cumulative_flow & line_chartjs
 * @param data
 * @param tileType fillDataset = True || False => CumulativeFlow
 * @returns
 */
function updateDatasetLine(data, tileType) {
    let listOfDataset = [];
    $.each(data.datasets, function (index, dataset) {
        let datasetTmp = {
            label: dataset.label,
            data: dataset.data,
            fill: (tileType === "cumulative_flow"),
            backgroundColor: dataset.backgroundColor,
            borderColor: dataset.backgroundColor
        };
        if (tileType === "cumulative_flow") {
            datasetTmp.trendlineLinear = {"lineStyle": "dotted", "width": 2};
        } else {
            delete datasetTmp.backgroundColor;
        }
        listOfDataset.push(datasetTmp);
    });
    let tile = {
        labels: data.labels,
        datasets: listOfDataset,
    };
    if ("title" in data) {
        tile.title = data.title;
    }
    if ("legend" in data) {
        tile.legend = data.legend;
    }
    return tile;
}

function updateDataset(chart, newDict) {
    let rcx = 0;
    for (; rcx < newDict.datasets.length; rcx++) {
        for (let keyDataset in newDict.datasets[rcx]) {
            if ({}.hasOwnProperty.call(newDict.datasets[rcx], keyDataset)) {
                if (chart.data.datasets.length <= rcx) {
                    chart.data.datasets.push({});
                }
                keyDataset = keyDataset.toString();
                chart.data.datasets[rcx][keyDataset.toString()] = newDict.datasets[rcx][keyDataset.toString()];
            }
        }
    }
    if (chart.data.datasets.length > newDict.datasets.length) {
        chart.data.datasets.splice(rcx, chart.data.datasets.length); // delete previous dataset
    }
}

/**
 * Update all data inside chart object
 * @param chart
 * @param chartNewValue
 */
function updateData(chart, chartNewValue) {
    for (let key in chartNewValue) {
        if ({}.hasOwnProperty.call(chartNewValue, key)) {
            key = key.toString();
            if (key === "datasets") {
                updateDataset(chart, chartNewValue);
            } else if (key === "title" || key === "legend") {
                chart.options[key.toString()] = chartNewValue[key.toString()];
            } else {
                chart.data[key.toString()] = chartNewValue[key.toString()];
            }
        }
    }
}

/**
 * Update all option(also called meta) inside chart object
 * @param actualOptions
 * @param newOptions
 */
function updateOptions(actualOptions, newOptions) {
    for (let key in newOptions) {
        if ({}.hasOwnProperty.call(newOptions, key)) {
            if (newOptions[key.toString()].constructor === Object && key.toString() in actualOptions) {
                updateOptions(actualOptions[key.toString()], newOptions[key.toString()]);
            } else {
                if (Array.isArray(actualOptions[key.toString()])) {
                    for (let rcx = 0; rcx < actualOptions[key.toString()].length; rcx++) {
                        updateOptions(actualOptions[key.toString()][rcx], newOptions[key.toString()][rcx]);
                    }
                } else {
                    actualOptions[key.toString()] = newOptions[key.toString()];
                }
            }
        }
    }
}

/**
 *
 * @param chart
 * @param data
 * @param meta
 */
function updateDataOfChartJS(chart, data, meta) {
    if ("labels" in chart.data) {
        chart.data.labels = [];
    }
    updateData(chart, data);
    if (meta !== "undefined") {
        updateOptions(chart.config.options, meta);
   }
   chart.update();
}

/**
 *
 * @param tileType
 * @returns {string}
 */
function getTypeOfChartJS(tileType) {
    switch (tileType) {
        case "pie_chart":
            return "pie";
        case "doughnut_chart":
        case "half_doughnut_chart":
            return "doughnut";
        case "polararea_chart":
            return "polarArea";
        case "radar_chart":
            return "radar";
        case "line_chart":
        case "norm_chart":
        case "cumulative_flow":
            return "line";
        case "bar_chart":
            return "horizontalBar";
        case "vbar_chart":
            return "bar";
        case "gauge_chart":
            return "tsgauge";
        case "radial_gauge_chart":
            return "radialGauge";
        case "linear_gauge_chart":
            return "linearGauge";
    }
}

/**
 * build the meta respecting speficity of all chart
 * @param tileType
 * @param meta
 * @returns {*}
 */
function buildMeta(tileType, meta) {
    switch (tileType) {
        case "pie_chart":
            meta.datalabels = pieChartPluginPercentge();
            break;
        case "half_doughnut_chart":
            meta.rotation = Math.PI;
            meta.circumference = Math.PI;
            break;
    }
    return meta;
}

/**
 * build the data respecting speficity of all chart
 * @param tileType
 * @param data
 * @returns
 */
function buildData(tileType, data) {
    if (tileType === "line_chart") {
        return updateDatasetLine(data, tileType);
    }
    return data;// tileType === "line_chart" ? updateDatasetLine(data, tileType) : data;
}

/**
 * Create or Update bar & vbar tile
 */
function updateChartjs(tileData, dashboardname) {
    let data = tileData["data"];
    let chartId = `${dashboardname}-${tileData["id"]}-chart`;
    if (!(chartId in Tipboard.chartJsTile)) {// tile not present in Tipboard cache
        if ("options" in tileData["meta"]) {
            tileData["meta"] = tileData["meta"]["options"];
        }
        let chart = document.getElementById(chartId);// in htlm la div id ne dépend pas des dashboard, elle sont générique
        chart.parentElement.style.paddingBottom = "9%";
        chart.height = "80%";
        Tipboard.chartJsTile[chartId] = new Chart(chart, {
            type: getTypeOfChartJS(tileData["tile_template"]),
            data: buildData(tileData["tile_template"], data),
            options: buildMeta(tileData["tile_template"], tileData["meta"]),
        });
    } else {
        if (tileData["tile_template"] === "line_chart") {
            data = updateDatasetLine(data, tileData["tile_template"]);
          }
       updateDataOfChartJS(Tipboard.chartJsTile[chartId], data, tileData["meta"]);
    }
}
