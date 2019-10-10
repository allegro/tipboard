function updateTileDoughnutjs(tileId, data, meta, tipboard) {
    console.log("doughnut_chartjs::updateTile::start" + tileId);
    var ctx = $('#' + tileId + "-chart");
    ctx.height = "75%";
    ctx.width = "90%";
    console.log(data);
    new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: meta
    });
    console.log("doughnut_chartjs::updateTile end" + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('doughnut_chart', updateTileDoughnutjs);
