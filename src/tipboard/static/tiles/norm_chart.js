function updateTileNorm(tileId, data, meta, tileType) {
    meta['options']['title'] = getTitleForChartJSTitle(data);
    new Chart(document.getElementById(tileId + '-chart'), {
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

