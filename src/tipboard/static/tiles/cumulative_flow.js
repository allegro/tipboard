var myColors = ['red', 'green', 'blue']; // Define your colors


function updateTileCumul(tileId, data, meta, tipboard) {
    console.log("cumulative_flow::updateTile::start" + tileId);
    var ctx = $('#' + tileId + "-chart");
    ctx.height = "86%";
    ctx.width = "98%";
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data['labels'],
            datasets: data['datasets'],
            borderColor: myColors
        },
        options: meta['options']
    });
    console.log("cumulative_flow::updateTile" + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('cumulative_flow', updateTileCumul);

