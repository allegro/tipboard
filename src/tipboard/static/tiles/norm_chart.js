var myColors = ['red', 'green', 'blue']; // Define your colors


function updateTileNormJs(tileId, data, meta, tipboard) {

    console.log("norm_chartjs::updateTile::start" + tileId);
    var ctx = $('#' + tileId + "-chart");
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data['labels'],
            datasets: data['datasets'],
        },
        options: meta['options']
    });
    console.log("norm_chartjs::updateTile" + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('norm_chart', updateTileNormJs);

