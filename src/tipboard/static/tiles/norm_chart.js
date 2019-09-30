function updateTileNorm(tileId, data, meta, tipboard) {

    console.log("norm_chart::updateTile::start" + tileId);
    var ctx = $('#' + tileId + "-chart");
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data['labels'],
            datasets: data['datasets'],
        },
        options: meta['options']
    });
    console.log("norm_chart::updateTile" + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('norm_chart', updateTileNorm);

