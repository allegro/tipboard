/**
 * Update normchartJS tile
 * @param tileId
 * @param data
 * @param meta
 * @param tileType
 */
function updateTileNorm(tileId, data, meta, tileType) {
    console.log("norm_chartjs::updateTile::start" + tileId);
    let chart = document.getElementById(tileId + "-chart");
    if (!(tileId + "-chart" in Tipboard.chartJsTile)) {
        console.log("norm_chartjs::updateTile:: create chartJS" + tileId);
        meta.options.title = getTitleForChartJSTitle(data);
        chart.parentElement.style.paddingBottom = "8%";
        Tipboard.chartJsTile[tileId + "-chart"] = new Chart(chart, {
            type: "line",
            data: {
                labels: data.labels,
                datasets: data.datasets,
            },
            options: meta.options
        });
    } else {
        console.log("norm_chartjs::updateTile:: update chartJS" + tileId);
        Tipboard.Dashboard.updateDataOfChartJS(Tipboard.chartJsTile[tileId + "-chart"], data);
    }
    console.log("norm_chart::type(" + tileType + ")::updateTile " + tileId);
}

Tipboard.Dashboard.registerUpdateFunction("norm_chart", updateTileNorm);

