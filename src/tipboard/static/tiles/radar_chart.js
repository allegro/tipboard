let chartElement = null;
let chart = null;

/**
 * @param tileId
 * @param data
 * @param meta
 * @param tileType
 */
function updateTileRadarjs(tileId, data, meta, tileType) {
    meta['options']['title'] = getTitleForChartJSTitle(data);
    if (chartElement == null) {
        chartElement = document.getElementById(tileId + '-chart');
        chartElement.parentElement.style.paddingBottom = '9%';
        chart = new Chart(chartElement, {
            type: (tileType === 'doughnut_chart') ? 'doughnut' : 'radar',
            data: data,
            options: meta['options']
        });
    } else {
        Tipboard.Dashboard.clearChartJsTile(chart);
        chart.data = data;
        chart.update();
    }
    console.log("radar_chartjs::type(" + tileType +")::updateTile end " + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('radar_chart', updateTileRadarjs);
