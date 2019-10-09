
function updatevBarChartjs(tileId, data, meta, tipboard) {
    console.log("vbar_chartjs::updateTile::start" + tileId);
    var ctx = $('#' + tileId + "-chart");
    ctx.height = "88%";
    ctx.width = "100%";
    new Chart(ctx, {
            type: 'bar',
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
    console.log("vbar_chartjs::updateTile" + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('vbar_chart', updatevBarChartjs);

