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
        Tipboard.chartJsTile[chartId] = new Chart(chart, {
            type: (tileType === "vbar_chart") ? "bar" : "horizontalBar",
            data: data,
            options: meta,
        });
    }
}

Tipboard.Dashboard.registerUpdateFunction("bar_chart", updateBarChartjs);
