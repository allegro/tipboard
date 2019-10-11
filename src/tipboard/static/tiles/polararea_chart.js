function updateTilePolararea(tileId, data, meta, tipboard) {
    console.log("updateTilePolararea::updateTile::start" + tileId);
    var ctx = $('#' + tileId + "-chart");
    console.log(data);
    console.log(meta);
    ctx.height = "75%";
    ctx.width = "90%";
    new Chart(ctx, {
        type: 'polarArea',
        data: {
            labels: data['labels'],
            datasets: data['datasets']
        },
        options: meta['options']
    });

    console.log("updateTilePolararea::updateTile end" + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('polararea_chart', updateTilePolararea);
