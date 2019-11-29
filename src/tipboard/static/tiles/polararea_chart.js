function updateTilePolararea(tileId, data, meta, tileType) {
    meta['options']['title'] = getTitleForChartJSTitle(data);
    let chart = document.getElementById(tileId + '-chart');
    chart.style.paddingBottom = '4%';
    new Chart(chart, {
        type: 'polarArea',
        data: {
            labels: data['labels'],
            datasets: data['datasets']
        },
        options: meta['options']
    });

    console.log("updateTilePolararea::type(" + tileType +")::updateTile end " + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('polararea_chart', updateTilePolararea);
