function updateBarChartjs(tileId, data, meta, tileType) {
    var ctx = document.getElementById(tileId + '-chart');
    ctx.style.height = '100px';
    ctx.style.width = '100px';
    let typeOfTile = '';
    if (tileType === 'vbar_chart')
        typeOfTile = 'bar';
    else
        typeOfTile = 'horizontalBar';
    new Chart(ctx, {
            type: typeOfTile,
            data: {
                labels: data['labels'],
                datasets: [{
                    label: data['label'],
                    data: data['data'],
                    backgroundColor: meta['backgroundColor'],
                }]
            },
            options: meta['options']
    });
    console.log("bar_chartjs::type(" + tileType +")::updateTile::start" + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('bar_chart', updateBarChartjs);
