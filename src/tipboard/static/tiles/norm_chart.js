function updateTileNorm(tileId, data, meta, tileType) {
    var ctx = document.getElementById(tileId + '-chart');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data['labels'],
            datasets: data['datasets'],
        },
        options: meta['options']
    });
    console.log("norm_chart::type(" + tileType +")::updateTile" + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('norm_chart', updateTileNorm);

