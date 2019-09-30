function updateTileRadarjs(tileId, data, meta, tipboard) {
    console.log("radar_chartjs::updateTile::start" + tileId);
    var ctx = $('#' + tileId + "-chart");
    console.log(data);
    new Chart(ctx, {
        type: 'radar',
        data: data,
        options: meta
    });
    console.log("radar_chartjs::updateTile end" + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('radar_chart', updateTileRadarjs);
