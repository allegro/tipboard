/**
 * Update for tile cumulative_flow & line_chartjs
 * @param data
 * @param tileType fillDataset = True || False => CumulativeFlow
 * @returns
 */
function updateDatasetLine(data, tileType) {
    const predefinedLabel = ["label1", "label2", "label3", "label4", "label5"];
    const predefinedSeries = ["serie1", "serie2", "serie3", "serie4", "serie5"];
    let listOfDataset = [];
    let rcx = 0;
    $.each(data.datasets, function (index, dataset) {
        let datasetTmp = {
            label: ("label" in dataset) ? dataset.label : predefinedLabel[rcx],
            data: ("data" in dataset) ? dataset.data : [],
            fill: (tileType === "cumulative_flow"),
            backgroundColor: dataset.backgroundColor,
            borderColor: dataset.backgroundColor
        };
        if (tileType === "cumulative_flow") {
            datasetTmp.trendlineLinear = {"lineStyle": "dotted", "width": 2}
        } else {
            delete datasetTmp.backgroundColor
        }
        listOfDataset.push(datasetTmp);
    });
    let tile = {
        labels: ("labels" in data) ? data.labels : predefinedSeries,
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


/**
 * update the line_chart tile & the cummulative_flow tile
 * @param tileId
 * @param data
 * @param meta
 * @param tileType
 */
function updateTileLinejs(tileId, data, meta, tileType) {
    console.log("line_chartjs::updateTile::start" + tileId);
    let chartId = `${tileId}-chart`;
    if (chartId in Tipboard.chartJsTile) {
        Tipboard.Dashboard.updateDataOfChartJS(Tipboard.chartJsTile[chartId],
            updateDatasetLine(data, tileType), meta);
    } else {
        let chart = document.getElementById(chartId);
        meta.options.title = getTitleForChartJSTitle(data);
        chart.parentElement.style.paddingBottom = "8%";
        Tipboard.chartJsTile[chartId] = new Chart(chart, {
            type: "line",
            data: updateDatasetLine(data, tileType),
            options: meta.options
        });
    }
    console.log("linejs::type(" + tileType + ")::updateTile " + tileId);
}

Tipboard.Dashboard.registerUpdateFunction("line_chart", updateTileLinejs);
