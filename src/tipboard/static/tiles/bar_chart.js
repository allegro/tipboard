
function updateBarChartjs(tileId, data, meta, tipboard) {
    console.log("bar_chartjs::updateTile::start" + tileId);
    var ctx = $('#' + tileId + "-chart");
    new Chart(ctx, {
            type: 'horizontalBar',
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
    console.log("bar_chartjs::updateTile" + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('bar_chart', updateBarChartjs);

