const predefinedLabel = ["label1", "label2", "label3", "label4", "label5"];
const predefinedSeries = ["serie1", "serie2", "serie3", "serie4", "serie5"];

/**
 * Update for tile cumulative_flow & line_chartjs
 * @param data
 * @param tileType fillDataset = True || False => CumulativeFlow
 * @returns
 */
function updateDataset(data, tileType) {
    let listOfDataset = [];
    let rcx = 0;
    $.each(data.datasets, function (index, dataset) {
        let datasetTmp = {
            label: ("label" in dataset) ? dataset.label : predefinedLabel[rcx],
            data: ("data" in dataset) ? dataset.data : [],
            fill: (tileType === "cumulative_flow"),
            backgroundColor: ("backgroundColor" in dataset) ?
                dataset.backgroundColor : Tipboard.Palette.tabColor[rcx],
            borderColor: ("backgroundColor" in dataset) ?
                dataset.backgroundColor : Tipboard.Palette.tabColor[rcx],
        };
        if (tileType === "cumulative_flow") {
            datasetTmp.trendlineLinear = {"lineStyle": "dotted", "width": 2}
        } else {
            delete datasetTmp.backgroundColor
        }
        listOfDataset.push(datasetTmp);
        rcx = rcx + 1;
    });
    console.log(listOfDataset);
    return {
        labels: ("labels" in data) ? data.labels : predefinedSeries,
        datasets: listOfDataset,
        borderColor: ["red", "green", "blue"]
    };
}


function updateData(oldDict, newDict) {
    for (let key in newDict) {
        if (key === "datasets") {
            console.log("Update dataset");
            let rcx = 0;
            for (; rcx < oldDict.datasets.length; rcx++) {
                for (let keyDataset in newDict.datasets[rcx]) {
                    console.log("Update key:[" + keyDataset + "] with " + newDict.datasets[rcx]);
                    oldDict.datasets[rcx][keyDataset] = newDict.datasets[rcx][keyDataset];
                }
            }
            oldDict.datasets.splice(rcx, oldDict.datasets.length); // delete previous data
            console.log("Update dataset over");
        } else {
            console.log("Update key:[" + key + "] with " + newDict[key]);
            oldDict[key] = newDict[key];
        }
    }
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
    if (!(tileId + "-chart" in Tipboard.chartJsTile)) {
        let chart = document.getElementById(tileId + "-chart");
        meta.options.title = getTitleForChartJSTitle(data);
        chart.parentElement.style.paddingBottom = "8%";
        Tipboard.chartJsTile[tileId + "-chart"] = new Chart(chart, {
            type: "line",
            data: updateDataset(data, tileType),
            options: meta.options
        });
    } else {
        Tipboard.Dashboard.updateDataOfChartJS(Tipboard.chartJsTile[tileId + "-chart"], data);
    }
    console.log("linejs::type(" + tileType + ")::updateTile " + tileId);
}

Tipboard.Dashboard.registerUpdateFunction("line_chart", updateTileLinejs);
