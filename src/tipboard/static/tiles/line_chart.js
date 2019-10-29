function updateTileLinejs(tileId, data, meta, tileType) {
    console.log("line_chartjs::updateTile::start" + tileId);
    let tileData = {
        labels: data['labels'],
        datasets: data['datasets'],
    };
    if (tileType === 'cumulative_flow') {
        tileData['borderColor'] = ['red', 'green', 'blue'];
    }
    meta['options']['title'] = getTitleForChartJSTitle(data);
    new Chart(document.getElementById(tileId + '-chart'), {
        type: 'line',
        data: tileData,
        options: meta['options']
    });
    console.log("linejs::type(" + tileType +")::updateTile" + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('line_chart', updateTileLinejs);

