/**
 *
 * @param tileId
 * @param data
 * @param meta
 * @param tileType
 */
function updateTileRadarjs(tileId, data, meta, tileType) {
    let chart = document.getElementById(tileId + '-chart');
    chart.parentElement.style.paddingBottom = '9%';
    meta['options']['title'] = getTitleForChartJSTitle(data);
    if (chart.className !== 'chartjs-render-monitor') {
        new Chart(chart, {
            type: (tileType === 'doughnut_chart') ? 'doughnut' : 'radar',
            data: data,
            options: meta['options']
        });
    } else {
        console.log("radar_chartjs::type(" + tileType +")::clear previous " + tileId);
        Tipboard.Dashboard.clearChartJsTile(chart);
        console.log("radar_chartjs::type(" + tileType +")::add data " + tileId);
        chart.data.push(data);
        chart.update();
        console.log("radar_chartjs::type(" + tileType +")::update " + tileId);
    }
    console.log("radar_chartjs::type(" + tileType +")::updateTile end " + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('radar_chart', updateTileRadarjs);
