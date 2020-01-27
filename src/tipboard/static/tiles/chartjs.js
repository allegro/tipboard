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

function getTypeOfChartJS(tileType) {
    switch (tileType) {
        case "pie_chart":
            return "pie";
        case "doughnut_chart":
            return "doughnut";
        case "half_doughnut_chart":
            return "doughnut";
        case "polararea_chart":
            return "polarArea";
        case "radar_chart":
            return "radar";
        case "line_chart":
            return "line";
        case "norm_chart":
            return "line";
        case "cumulative_flow":
            return "line";
        case "bar_chart":
            return "horizontalBar";
        case "vbar_chart":
            return "bar";
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
    console.log("DATA TILE:", data);
    return data;
}

/**
 * Update or Create bar & vbar tile
 * @param tileId
 * @param data
 * @param meta
 * @param tileType
 */
function updateChartjs(tileId, data, meta, tileType) {
    let chartId = `${tileId}-chart`;
    if (chartId in Tipboard.chartJsTile) {
        if (tileType === "line_chart") {
            data = updateDatasetLine(data, tileType);
        }
        Tipboard.Dashboard.updateDataOfChartJS(Tipboard.chartJsTile[chartId], data, meta);
    } else {
        let chart = document.getElementById(chartId);
        chart.parentElement.style.paddingBottom = "9%";
        chart.height = "80%";
        let op = buildMeta(tileType, meta);
        Tipboard.chartJsTile[chartId] = new Chart(chart, {
            type: getTypeOfChartJS(tileType),
            data: buildData(tileType, data),
            options: op,
        });
    }
}

Tipboard.Dashboard.registerUpdateFunction("bar_chart", updateChartjs);
Tipboard.Dashboard.registerUpdateFunction("polararea_chart", updateChartjs);
Tipboard.Dashboard.registerUpdateFunction("pie_chart", updateChartjs);
Tipboard.Dashboard.registerUpdateFunction("norm_chart", updateChartjs);
Tipboard.Dashboard.registerUpdateFunction("radar_chart", updateChartjs);
Tipboard.Dashboard.registerUpdateFunction("line_chart", updateChartjs);
