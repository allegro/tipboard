/**
 * Update Radar & Doughnut chart
 * @param tileId
 * @param data
 * @param meta
 * @param tileType
 */
function updateTileRadarjs(tileId, data, meta, tileType) {
    let chartId = `${tileId}-chart`;
    console.log("radar_chartjs::LANCER");
    if (chartId in Tipboard.chartJsTile) {
        console.log("DATA -> ", data);
        Tipboard.Dashboard.updateDataOfChartJS(Tipboard.chartJsTile[chartId], data);
    } else {
        let chartElement = document.getElementById(chartId);
        chartElement.parentElement.style.paddingBottom = "9%";
        meta.options.title = getTitleForChartJSTitle(data);
        console.log(tileType);
        if (tileType === "half_doughnut_chart") {
            meta.options.rotation = Math.PI;
            meta.options.circumference = Math.PI;
        }
        Tipboard.chartJsTile[chartId] = new Chart(chartElement, {
            type: (tileType === "doughnut_chart" || tileType === "half_doughnut_chart") ? "doughnut" : "radar",
            data: data,
            options: meta.options
        });
    }
    console.log("radar_chartjs::type(" + tileType +")::updateTile end " + tileId);
}

Tipboard.Dashboard.registerUpdateFunction("radar_chart", updateTileRadarjs);
