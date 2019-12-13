/**
 * @param tileId
 * @param data
 * @param meta
 * @param tileType
 */
function updateTileRadarjs(tileId, data, meta, tileType) {
    meta['options']['title'] = getTitleForChartJSTitle(data);
    if (!(tileId + '-chart' in Tipboard.chartJsTile)) {
        console.log("radar_chartjs::type(" + tileType +")::create ChartJS" + tileId);
        let chartElement = document.getElementById(tileId + '-chart');
        chartElement.parentElement.style.paddingBottom = '9%';
        Tipboard.chartJsTile[tileId + '-chart'] = new Chart(chartElement, {
            type: (tileType === 'doughnut_chart') ? 'doughnut' : 'radar',
            data: data,
            options: meta['options']
        });
    } else {
        Tipboard.Dashboard.clearChartJsTile(Tipboard.chartJsTile[tileId + '-chart']);
        Tipboard.chartJsTile[tileId + '-chart'].data = data;
        Tipboard.chartJsTile[tileId + '-chart'].update();
    }
    console.log("radar_chartjs::type(" + tileType +")::updateTile end " + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('radar_chart', updateTileRadarjs);
