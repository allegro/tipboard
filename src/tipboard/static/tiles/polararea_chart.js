/**
 * Pas tester depuis la refonte chart dans TipBoard.chartJStile
 * @param tileId
 * @param data
 * @param meta
 * @param tileType
 */
function updateTilePolararea(tileId, data, meta, tileType) {
    meta.options.title = getTitleForChartJSTitle(data);
    let chartId = `${tileId}-chart`;
    if (tileId + "-chart" in Tipboard.chartJsTile) {
        Tipboard.Dashboard.updateDataOfChartJS(Tipboard.chartJsTile[chartId], data);
    } else {
        let chart = document.getElementById(chartId);
        chart.parentElement.style.paddingBottom = "10%";
        Tipboard.chartJsTile[chartId] = new Chart(chart, {
            type: "polarArea",
            data: {
                labels: data.labels,
                datasets: data.datasets
            },
            options: meta.options
        });
    }
    console.log("updateTilePolararea::type(" + tileType + ")::updateTile end " + tileId);
}

Tipboard.Dashboard.registerUpdateFunction("polararea_chart", updateTilePolararea);
