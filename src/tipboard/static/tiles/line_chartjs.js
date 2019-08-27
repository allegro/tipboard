
function updateTileLinejs(tileId, data, meta, tipboard) {
    console.log("line_chartjs::updateTile::start" + tileId);
    var ctx = $('#' + tileId + "-chart");
    var chart = new Chart(ctx, {
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
    console.log("line_chartjs::updateTile" + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('line_chartjs', updateTileLinejs);

