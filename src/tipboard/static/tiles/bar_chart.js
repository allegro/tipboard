function updateBarChartjs(tileId, data, meta, tipboard) {
    console.log("bar_chartjs::updateTile::start" + tileId);
    var ctx = $('#' + tileId + "-chart");
    ctx.height = "88%";
    ctx.width = "100%";
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
}

Tipboard.Dashboard.registerUpdateFunction('bar_chart', updateBarChartjs);

