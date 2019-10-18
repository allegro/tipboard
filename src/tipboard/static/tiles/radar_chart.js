function updateTileRadarjs(tileId, data, meta, tileType) {
    var ctx = $('#' + tileId + "-chart");
    ctx.height = "75%";
    ctx.width = "90%";
    let typeOfTile = 'radar';
    if (tileType === 'doughnut_chart')
        typeOfTile = 'doughnut';
    new Chart(ctx, {
        type: typeOfTile,
        data: data,
        options: meta
    });
    console.log("radar_chartjs::type(" + tileType +")::updateTile end" + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('radar_chart', updateTileRadarjs);
