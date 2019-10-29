function updateTileRadarjs(tileId, data, meta, tileType) {
    meta['options']['title'] = getTitleForChartJSTitle(data);
    new Chart(document.getElementById(tileId + '-chart'), {
        type: (tileType === 'doughnut_chart') ? 'doughnut' : 'radar',
        data: data,
        options: meta['options']
    });
    console.log("radar_chartjs::type(" + tileType +")::updateTile end " + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('radar_chart', updateTileRadarjs);
