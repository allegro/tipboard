var myColors = ['red', 'green', 'blue']; // Define your colors


function updateTileCumulJs(tileId, data, meta, tipboard) {

    console.log("cumulative_flowjs::updateTile::start" + tileId);
    var ctx = $('#' + tileId + "-chart");
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data['labels'],
            datasets: data['datasets'],
            borderColor: myColors
        },
        options: meta['options']
    });
    console.log("cumulative_flowjs::updateTile" + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('cumulative_flowjs', updateTileCumulJs);

