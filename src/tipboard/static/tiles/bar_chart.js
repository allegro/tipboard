/**
 *
 * @param data
 * @returns {[]}
 */
function buildDatasets(data) {
    let listOfDataset = [];
    $.each(data["datasets"], function (index, dataset) {
        let datasetTmp = {
            label: ("label" in dataset) ? dataset["label"] : "",
            data: ("data" in dataset) ? dataset["data"] : [],
            backgroundColor: ("backgroundColor" in dataset) ?
                dataset["backgroundColor"] : Tipboard.Palette.tabColor[index]
        };
        listOfDataset.push(datasetTmp);
    });
    return listOfDataset;
}

/**
 * Build Grid options
 * @param meta
 */
function buildMeta(meta) {
    return {
        options: {
            scale: {
                gridLines: {
                    color: ["#525252", "#525252", "#525252", "#525252", "#525252", "#525252", "#525252"]
                },
                angleLines: {color: "#525252"},
                ticks: {display: true}
            },
            legend: {
                display: false,
                position: "bottom"
            },
            tooltips: {
                callbacks: {
                    label: function (tooltipItem) {
                        return tooltipItem.yLabel;
                    }
                }
            },
            responsive: true,
            maintainAspectRatio: false,
        }
    }
}



/**
 * Update bar & vbar tile
 * @param tileId
 * @param data
 * @param meta
 * @param tileType
 */
function updateBarChartjs(tileId, data, meta, tileType) {
    let chartId = `${tileId}-chart`;
    if (chartId in Tipboard.chartJsTile) {
        Tipboard.Dashboard.updateDataOfChartJS(Tipboard.chartJsTile[chartId], data);
    } else {
        let chart = document.getElementById(chartId);
        chart.parentElement.style.paddingBottom = "9%";
        chart.height = "80%";
        chart.widget = "100%";
        new Chart(chart, {
            type: (tileType === "vbar_chart") ? "bar" : "horizontalBar",
            data: {
                labels: data["labels"],
                datasets: buildDatasets(data),
            },
            options: buildMeta(meta)
        });
    }
}

Tipboard.Dashboard.registerUpdateFunction("bar_chart", updateBarChartjs);
// les configs de bar chart ne fonctionne pas
