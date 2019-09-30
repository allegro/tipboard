
function updateTileLinejs(tileId, data, meta, tipboard) {
    console.log("line_chartjs::updateTile::start" + tileId);
    var ctx = $('#' + tileId + "-chart");
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data['labels'],
            datasets: data['datasets'],
        },
        options: meta['options']
    });
    console.log("line_chartjs::updateTile" + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('line_chart', updateTileLinejs);

