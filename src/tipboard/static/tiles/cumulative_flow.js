var myColors = ['red', 'green', 'blue']; // Define your colors


function updateTileCumul(tileId, data, meta, tileType) {
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
    console.log("cumulative_flow::type(" + tileType +")::updateTile" + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('cumulative_flow', updateTileCumul);

