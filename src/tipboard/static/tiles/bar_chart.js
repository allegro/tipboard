function updateBarChartjs(tileId, data, meta, tileType) {
    let typeOfTile = 'horizontalBar';
    if (tileType === 'vbar_chart')
        typeOfTile = 'bar';
    meta['options']['title'] = getTitleForChartJSTitle(data);
    new Chart(document.getElementById(tileId + '-chart'), {
            type: typeOfTile,
            data: {
                labels: data['labels'],
                datasets: data['datasets'],
            },
            options: meta['options']
    });
    console.log("bar_chartjs::type(" + tileType +")::updateTile::start" + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('bar_chart', updateBarChartjs);
