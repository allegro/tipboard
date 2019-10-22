function updateBarChartjs(tileId, data, meta, tileType) {
    var ctx = document.getElementById(tileId + '-chart');
    let typeOfTile = 'horizontalBar';
    if (tileType === 'vbar_chart')
        typeOfTile = 'bar';
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
