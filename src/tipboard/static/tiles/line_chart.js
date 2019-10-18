function updateTileLinejs(tileId, data, meta, tileType) {
    console.log("line_chartjs::updateTile::start" + tileId);
    var ctx = document.getElementById(tileId + '-chart');
    ctx.style.height = '100px';
    ctx.style.width = '100px';
    let tileData = {
        labels: data['labels'],
        datasets: data['datasets'],
    };

    if (tileType === 'cumulative_flow') {
        tileData['borderColor'] = ['red', 'green', 'blue'];
    }

    new Chart(ctx, {
        type: 'line',
        data: tileData,
        options: meta['options']
    });
    console.log("linejs::type(" + tileType +")::updateTile" + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('line_chart', updateTileLinejs);

