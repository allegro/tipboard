/**
 * Update Radar & Doughnut chart
 * @param tileId
 * @param data
 * @param meta
 * @param tileType
 */
function updateTileRadarjs(tileId, data, meta, tileType) {
    let chartId = `${tileId}-chart`;
    if (chartId in Tipboard.chartJsTile) {
        Tipboard.Dashboard.updateDataOfChartJS(Tipboard.chartJsTile[chartId], data);
    } else {
        let chartElement = document.getElementById(chartId);
        chartElement.parentElement.style.paddingBottom = "9%";
        meta.options.title = getTitleForChartJSTitle(data);
        Tipboard.chartJsTile[chartId] = new Chart(chartElement, {
            type: (tileType === "doughnut_chart") ? "doughnut" : "radar",
            data: data,
            options: meta.options
        });
    }
    console.log("radar_chartjs::type(" + tileType +")::updateTile end " + tileId);
}

Tipboard.Dashboard.registerUpdateFunction("radar_chart", updateTileRadarjs);
