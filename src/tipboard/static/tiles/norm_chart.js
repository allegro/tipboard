/**
 * Update normchartJS tile
 * @param tileId
 * @param data
 * @param meta
 * @param tileType
 */
function updateTileNorm(tileId, data, meta, tileType) {
    let chartId = `${tileId}-chart`;
    let chart = document.getElementById(chartId);
    if (chartId in Tipboard.chartJsTile) {
        Tipboard.Dashboard.updateDataOfChartJS(Tipboard.chartJsTile[chartId], data);
        Tipboard.chartJsTile[chartId].update();
    } else {
        meta.options.title = getTitleForChartJSTitle(data);
        chart.parentElement.style.paddingBottom = "8%";
        Tipboard.chartJsTile[chartId] = new Chart(chart, {
            type: "line",
            data: {
                labels: data.labels,
                datasets: data.datasets,
            },
            options: meta.options
        });
    }
    console.log("norm_chart::type(" + tileType + ")::updateTile " + tileId);
}

Tipboard.Dashboard.registerUpdateFunction("norm_chart", updateTileNorm);
