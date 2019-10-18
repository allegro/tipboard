function updateTilePolararea(tileId, data, meta, tileType) {
    var ctx = document.getElementById(tileId + '-chart');
    ctx.style.height = '100px';
    ctx.style.width = '100px';
    new Chart(ctx, {
        type: 'polarArea',
        data: {
            labels: data['labels'],
            datasets: data['datasets']
        },
        options: meta['options']
    });

    console.log("updateTilePolararea::type(" + tileType +")::updateTile end" + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('polararea_chart', updateTilePolararea);
