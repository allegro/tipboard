function updateTileRadarjs(tileId, data, meta, tileType) {
    var ctx = document.getElementById(tileId + '-chart');
    let typeOfTile = 'radar';
    if (tileType === 'doughnut_chart')
        typeOfTile = 'doughnut';
    new Chart(ctx, {
        type: typeOfTile,
        data: data,
        options: meta
    });
    console.log("radar_chartjs::type(" + tileType +")::updateTile end" + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('radar_chart', updateTileRadarjs);
