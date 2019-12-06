function updateTileNorm(tileId, data, meta, tileType) {
    let chart = document.getElementById(tileId + '-chart');
    meta['options']['title'] = getTitleForChartJSTitle(data);
    chart.parentElement.style.paddingBottom = '8%';
    new Chart(chart, {
        type: 'line',
        data: {
            labels: data['labels'],
            datasets: data['datasets'],
        },
        options: meta['options']
    });
    console.log("norm_chart::type(" + tileType +")::updateTile " + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('norm_chart', updateTileNorm);

