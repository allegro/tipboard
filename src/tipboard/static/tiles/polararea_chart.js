function updateTilePolararea(tileId, data, meta, tileType) {
    meta['options']['title'] = getTitleForChartJSTitle(data);
    new Chart(document.getElementById(tileId + '-chart'), {
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
