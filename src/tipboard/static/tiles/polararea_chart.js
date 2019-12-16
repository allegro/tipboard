/**
 * Pas tester depuis la refonte chart dans TipBoard.chartJStile
 * @param tileId
 * @param data
 * @param meta
 * @param tileType
 */
function updateTilePolararea(tileId, data, meta, tileType) {
    meta.options.title = getTitleForChartJSTitle(data);
    if (!(tileId + "-chart" in Tipboard.chartJsTile)) {
        let chart = document.getElementById(tileId + "-chart");
        chart.parentElement.style.paddingBottom = "10%";
        Tipboard.chartJsTile[tileId + "-chart"] = new Chart(chart, {
            type: "polarArea",
            data: {
                labels: data.labels,
                datasets: data.datasets
            },
            options: meta.options
        });
    } else {
        let chart = Tipboard.chartJsTile[tileId + "-chart"];
        chart.data.datasets[0].labels = data.labels;
        chart.data.datasets[0].data = data.data;
        Tipboard.chartJsTile[tileId + "-chart"].update();
    }
    console.log("updateTilePolararea::type(" + tileType + ")::updateTile end " + tileId);
}

Tipboard.Dashboard.registerUpdateFunction("polararea_chart", updateTilePolararea);
