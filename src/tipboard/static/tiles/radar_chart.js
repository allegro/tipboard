function updateTileRadarjs(tileId, data, meta, tileType) {
    let typeOfTile = 'radar';
    if (tileType === 'doughnut_chart')
        typeOfTile = 'doughnut';
    meta['options']['title'] = getTitleForChartJSTitle(data);
    new Chart(document.getElementById(tileId + '-chart'), {
        type: typeOfTile,
        data: data,
        options: meta['options']
    });
    console.log("radar_chartjs::type(" + tileType +")::updateTile end" + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('radar_chart', updateTileRadarjs);
